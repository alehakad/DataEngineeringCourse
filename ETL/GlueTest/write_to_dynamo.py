import logging
import uuid

import boto3
from awsglue.context import GlueContext
from pyspark.context import SparkContext
from pyspark.sql import functions as F
from pyspark.sql.types import StringType

# Initialize Spark & Glue Context
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

# AWS Config
BUCKET_NAME = "etls-spotify-bucket"
AWS_REGION = "eu-north-1"

DATASETS = {
    "country_hours_distribution": {
        "s3_path": "processed/country_hours_distribution.csv",
        "table_name": "country_hours_distribution",
        "partition_key": "id"
    },
    "age_genre_distribution": {
        "s3_path": "processed/genres_age_distribution.csv",
        "table_name": "age_genre_distribution",
        "partition_key": "id"
    }
}

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize DynamoDB Client
dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)


def read_csv_from_s3(s3_path):
    """Reads a CSV file from S3 into a PySpark DataFrame"""
    full_path = f"s3://{BUCKET_NAME}/{s3_path}"
    logger.info(f"Reading CSV from {full_path}")

    df = spark.read.csv(full_path, header=True, inferSchema=True)
    df = df.withColumn("id", F.udf(lambda: str(uuid.uuid4()), StringType())())  # Generate Unique ID
    df.show(3)

    return df


def write_to_dynamodb(df, table_name):
    """Writes DataFrame records to DynamoDB"""
    table = dynamodb.Table(table_name)
    records = df.toPandas().to_dict(orient="records")

    logger.info(f"Writing {len(records)} records to DynamoDB table: {table_name}")
    with table.batch_writer() as batch:
        for record in records:
            batch.put_item(Item=record)

    logger.info(f"Successfully inserted {len(records)} records into {table_name}.")


if __name__ == "__main__":
    for dataset, config in DATASETS.items():
        df = read_csv_from_s3(config["s3_path"])
        write_to_dynamodb(df, config["table_name"])
