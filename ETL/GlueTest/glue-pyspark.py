import logging

from awsglue.context import GlueContext
from pyspark.context import SparkContext
from pyspark.sql import functions as F
from pyspark.sql.functions import col

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Spark & Glue
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

BUCKET_NAME = "etls-spotify-bucket"
RAW_DATA_FOLDER = "data"
PROCESSED_DATA_FOLDER = "processed"


def read_csv_files():
    logger.info("Reading CSV files from S3...")

    s3_path = f"s3://{BUCKET_NAME}/{RAW_DATA_FOLDER}"
    try:
        users_df = spark.read.csv(f"{s3_path}/users.csv", header=True, inferSchema=True)
        songs_df = spark.read.csv(f"{s3_path}/songs.csv", header=True, inferSchema=True)
        streams_df = spark.read.csv(f"{s3_path}/streams1.csv", header=True, inferSchema=True)

        logger.info("Successfully read CSV files from S3.")
    except Exception as e:
        logger.error(f"Error reading CSV files from S3: {e}")
        raise e

    return users_df, songs_df, streams_df


# def read_csv_files():
#     # to read local files
#     logger.info("Reading CSV files...")
#     csv_files_path = "/home/glue_user/data/csv"
#
#     try:
#         users_df = spark.read.csv(f"{csv_files_path}/users.csv", header=True, inferSchema=True)
#         songs_df = spark.read.csv(f"{csv_files_path}/songs.csv", header=True, inferSchema=True)
#         streams_df = spark.read.csv(f"{csv_files_path}/streams1.csv", header=True, inferSchema=True)
#         logger.info("Successfully read CSV files.")
#     except Exception as e:
#         logger.error(f"Error reading CSV files: {e}")
#         raise e
#
#     return users_df, songs_df, streams_df


def validate_songs_df(songs_df):
    logger.info("Validating songs DataFrame...")

    # check columns
    if 'track_id' not in songs_df.columns:
        logger.error("Missing column 'track_id' in songs_df")
        raise ValueError("Missing column 'track_id' in songs_df")

    try:

        # Drop rows with missing critical values
        songs_df = songs_df.dropna(subset=["popularity", "track_id", "artists", "track_name", "duration_ms"])

        # Fill NaN values with 0
        songs_df = songs_df.fillna(0)

        # Drop duplicate rows
        songs_df = songs_df.dropDuplicates()

        # Validate the range for numerical columns
        songs_df = songs_df.filter(col("duration_ms") > 0)  # duration_ms must be positive
        songs_df = songs_df.filter(col("danceability").between(0, 1))  # between 0 and 1
        songs_df = songs_df.filter(col("energy").between(0, 1))
        songs_df = songs_df.filter(col("loudness").between(-80, 5))  # loudness should be in a reasonable range
        songs_df = songs_df.filter(col("mode").isin([1, 0]))  # mode or 0 or 1
        songs_df = songs_df.filter(col("speechiness").between(0, 1))
        songs_df = songs_df.filter(col("acousticness").between(0, 1))
        songs_df = songs_df.filter(col("instrumentalness").between(0, 1))
        songs_df = songs_df.filter(col("liveness").between(0, 1))
        songs_df = songs_df.filter(col("valence").between(0, 1))
        songs_df = songs_df.filter(col("tempo") > 0)  # tempo must be positive

        logger.info("Songs DataFrame validation completed.")
    except Exception as e:
        logger.error(f"Error during validation of songs DataFrame: {e}")
        raise e

    return songs_df


def validate_users_df(users_df):
    logger.info("Validating users DataFrame...")

    # check columns
    if 'user_id' not in users_df.columns:
        logger.error("Missing column 'track_id' in songs_df")
        raise ValueError("Missing column 'track_id' in songs_df")

    try:
        # Drop rows with missing critical values
        users_df = users_df.dropna(subset=["user_id", "user_name"])

        # Fill NaN values with 0
        users_df = users_df.fillna(0)

        # Drop duplicates
        users_df = users_df.dropDuplicates(subset=["user_id"])

        logger.info("Users DataFrame validation completed.")
    except Exception as e:
        logger.error(f"Error during validation of users DataFrame: {e}")
        raise e

    return users_df


def validate_streams_df(streams_df, songs_df, users_df):
    logger.info("Validating streams DataFrame...")

    # check columns
    if 'user_id' not in streams_df.columns or 'track_id' not in streams_df.columns:
        logger.error("Missing column 'track_id' in songs_df")
        raise ValueError("Missing column 'track_id' in songs_df")

    try:
        # Get valid track_ids and user_ids
        valid_streams_df = streams_df.join(songs_df.select("track_id"), on="track_id", how="left_semi") \
            .join(users_df.select("user_id"), on="user_id", how="left_semi")

        logger.info("Streams DataFrame validation completed.")
    except Exception as e:
        logger.error(f"Error during validation of streams DataFrame: {e}")
        raise e

    return valid_streams_df


def calculate_genres_age_distribution(users_df, songs_df, streams_total_df):
    logger.info("Calculating genres by age distribution...")

    try:
        # Create age bins and labels
        age_bins = [0, 18, 25, 35, 45, 100]
        age_labels = ["Under 18", "18-25", "26-35", "36-45", "46+"]

        # Use Spark's `when` and `otherwise` to create the age group column
        users_df = users_df.withColumn(
            "age_group",
            F.when((users_df["user_age"] >= age_bins[0]) & (users_df["user_age"] < age_bins[1]), age_labels[0])
            .when((users_df["user_age"] >= age_bins[1]) & (users_df["user_age"] < age_bins[2]), age_labels[1])
            .when((users_df["user_age"] >= age_bins[2]) & (users_df["user_age"] < age_bins[3]), age_labels[2])
            .when((users_df["user_age"] >= age_bins[3]) & (users_df["user_age"] < age_bins[4]), age_labels[3])
            .otherwise(age_labels[4])
        )

        # Join the DataFrames: streams_total_df -> users_df -> songs_df
        merged_df = streams_total_df.join(users_df, "user_id", "inner") \
            .join(songs_df, "track_id", "inner")

        # Group by age_group and track_genre, and count the number of streams
        count_streams = merged_df.groupBy("age_group", "track_genre").count().withColumnRenamed("count", "stream_count")

        logger.info("Genres by age distribution calculation completed.")
    except Exception as e:
        logger.error(f"Error during genres by age distribution calculation: {e}")
        raise e

    return count_streams


def calculate_country_hours_distribution(songs_df, users_df, streams_total_df):
    logger.info("Calculating country hours distribution...")

    try:
        # Join the DataFrames: streams_total_df -> users_df
        merged_df = streams_total_df.join(users_df, "user_id", "inner") \
            .join(songs_df, "track_id", "inner")

        # Extract the hour from the listen_time column and group by hour and user_country
        hours_country_df = merged_df.withColumn("hour", F.hour(merged_df["listen_time"])) \
            .groupBy("hour", "user_country") \
            .count().withColumnRenamed("count", "stream_count")

        logger.info("Country hours distribution calculation completed.")
    except Exception as e:
        logger.error(f"Error during country hours distribution calculation: {e}")
        raise e

    return hours_country_df


def write_to_s3(processed_df, filename):
    s3_output_file = f"s3://{BUCKET_NAME}/{PROCESSED_DATA_FOLDER}"

    try:
        processed_df.write.mode("overwrite").csv(f"{s3_output_file}/{filename}")
        logger.info(f"Successfully wrote {filename} to S3.")
    except Exception as e:
        logger.error(f"Error writing {filename} to S3: {e}")
        raise e


def process_csv_files():
    logger.info("Starting the ETL process...")

    try:
        # Read data from CSV files
        users_df, songs_df, streams_df = read_csv_files()

        # Validate the songs, users, and streams data
        songs_df = validate_songs_df(songs_df)
        users_df = validate_users_df(users_df)
        streams_df = validate_streams_df(streams_df, songs_df, users_df)

        if users_df.count() == 0:
            logger.warning("No users data found.")
        if songs_df.count() == 0:
            logger.warning("No songs data found.")
        if streams_df.count() == 0:
            logger.warning("No streams data found.")

        # Transform data
        genres_age_distribution_df = calculate_genres_age_distribution(users_df, songs_df, streams_df)
        country_hours_distribution_df = calculate_country_hours_distribution(songs_df, users_df, streams_df)

        # Write result dfs to s3
        write_to_s3(genres_age_distribution_df, "genres_age_distribution.csv")
        write_to_s3(country_hours_distribution_df, "country_hours_distribution.csv")

        # Show result for test
        # genres_age_distribution_df.show(n=3)
        # country_hours_distribution_df.show(n=3)

        logger.info("ETL process completed successfully.")
    except Exception as e:
        logger.error(f"Error during the ETL process: {e}")
        raise e


if __name__ == "__main__":
    process_csv_files()
