import logging
from io import StringIO

import sys
import os
import pandas as pd
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.providers.amazon.aws.hooks.redshift_sql import RedshiftSQLHook
from airflow.utils.dates import days_ago

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.validators import validate_songs_df, validate_users_df, validate_streams_df
from utils.queries import CREATE_TABLES_QUERIES
from utils.metrics import (
    calculate_genres_age_distribution,
    calculate_country_hours_distribution,
)

# Constants
BUCKET_NAME = "spsongsbucket"
PREFIX = "data/"
REDSHIFT_TABLE = "user_data"

logger = logging.getLogger(__name__)


def read_csvs_from_s3(**kwargs):
    """Reads all CSV files from S3 and saves their content in XCom"""
    s3_hook = S3Hook(aws_conn_id="aws_default")
    files = s3_hook.list_keys(bucket_name=BUCKET_NAME, prefix=PREFIX)

    if not files:
        logger.warning("No files found in S3.")
        return []

    csv_data = {}

    for file_key in files:
        if file_key.endswith(".csv"):
            file_content = s3_hook.read_key(bucket_name=BUCKET_NAME, key=file_key)
            csv_data[file_key] = file_content

    logger.info(f"Read {len(csv_data)} CSV files from S3.")

    return csv_data


def validate_data(**kwargs):
    """Validates songs, users, and streams data, then saves cleaned DataFrames in XCom."""
    ti = kwargs["ti"]
    raw_data = ti.xcom_pull(task_ids="read_s3_task")

    if not raw_data:
        raise ValueError("No data found in XCom for validation.")

    cleaned_data = {}

    # validate songs and users
    for file_name, records in raw_data.items():
        df = pd.read_csv(StringIO(records))

        logging.info(f"Validating {file_name}...")

        if "songs" in file_name:
            cleaned_data["songs"] = validate_songs_df(df)
        elif "users" in file_name:
            cleaned_data["users"] = validate_users_df(df)

    # validate streams
    for file_name, records in raw_data.items():
        if "streams" in file_name:
            if "songs" not in cleaned_data or "users" not in cleaned_data:
                raise ValueError(
                    "Missing required songs or users data for validating streams."
                )

            df = pd.read_csv(StringIO(records))
            logging.info(f"Validating {file_name}...")
            cleaned_data["streams"] = validate_streams_df(
                df, cleaned_data["songs"], cleaned_data["users"]
            )
    # convert to csv
    for key in cleaned_data:
        cleaned_data[key] = cleaned_data[key].to_csv(index=False)

    return cleaned_data


def transform_data(**kwargs):
    """Transforms the data and saves the result in XCom."""
    ti = kwargs["ti"]
    data = ti.xcom_pull(task_ids="validate_data_task")
    if not data:
        raise ValueError("No data found in XCom for transformation.")

    transformed_data = {}

    songs_df = pd.read_csv(StringIO(data.get("songs")))
    users_df = pd.read_csv(StringIO(data.get("users")))
    streams_df = pd.read_csv(StringIO(data.get("streams")))

    # convert date
    streams_df["listen_time"] = pd.to_datetime(
        streams_df["listen_time"], errors="coerce"
    )
    streams_df.dropna(subset=["listen_time"], inplace=True)

    # created_at to date
    users_df["created_at"] = pd.to_datetime(users_df["created_at"], errors="coerce")
    users_df.dropna(subset=["created_at"], inplace=True)

    # Calculate the distribution of genres listened to by different age groups
    genres_age_distribution = calculate_genres_age_distribution(
        users_df, songs_df, streams_df
    )
    transformed_data["age_genres_distribution"] = genres_age_distribution.to_csv(
        index=False
    )

    # Calculate the distribution of hours listened by country
    country_hours_distribution = calculate_country_hours_distribution(
        songs_df, users_df, streams_df
    )
    transformed_data["country_hours_distribution"] = country_hours_distribution.to_csv(
        index=False
    )

    return transformed_data


# def create_tables(**kwargs):
#     """Creates metrics tables in Redshift"""
#     redshift_hook = RedshiftSQLHook(redshift_conn_id="redshift_connection")
#     for table_name, query in CREATE_TABLES_QUERIES.items():
#         redshift_hook.run(query)
#         logging.info(f"✅ Table '{table_name}' checked/created.")


def load_csv_to_redshift(**kwargs):
    """Inserts transformed data from XCom into Redshift tables."""

    ti = kwargs["ti"]
    transformed_data = ti.xcom_pull(task_ids="transform_data_task")

    if not transformed_data:
        raise ValueError("No cleaned data found in XCom for insertion.")

    redshift_hook = RedshiftSQLHook(redshift_conn_id="redshift_connection")

    for table, records in transformed_data.items():
        if records:
            df = pd.read_csv(StringIO(records))
            formatted_records = [tuple(row) for row in df.values]
            redshift_hook.insert_rows(
                table=table,
                rows=formatted_records,
                target_fields=None,
                replace=False,
                executemany=True,
            )
            logging.info(f"✅ Inserted {len(records)} rows into {table}.")

    return "Insertion Completed"


# Define Default Arguments
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": days_ago(1),
    "retries": 0,
}

# Create DAG
with DAG(
    dag_id="s3_to_redshift_dag",
    default_args=default_args,
    schedule_interval=None,  # trigger manually
    catchup=False,
) as dag:
    # create_tables_task = PythonOperator(
    #     task_id="create_tables_task",
    #     python_callable=create_tables,
    # )

    read_s3_task = PythonOperator(
        task_id="read_s3_task",
        python_callable=read_csvs_from_s3,
    )

    validate_data_task = PythonOperator(
        task_id="validate_data_task",
        python_callable=validate_data,
    )

    transform_data_task = PythonOperator(
        task_id="transform_data_task",
        python_callable=transform_data,
    )

    load_redshift_task = PythonOperator(
        task_id="load_redshift_task",
        python_callable=load_csv_to_redshift,
    )

    # Set Task Dependencies
    (
        # create_tables_task
        read_s3_task
        >> validate_data_task
        >> transform_data_task
        >> load_redshift_task
    )
