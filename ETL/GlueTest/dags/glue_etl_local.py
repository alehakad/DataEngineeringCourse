"""
Script to run two glue jobs inside docker container with airflow
"""

import os
import subprocess

from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.utils.dates import days_ago
from docker.types import Mount

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'retries': 1,
}

cwd = os.path.dirname(os.getcwd())
home_dir = os.path.expanduser('~')

aws_mount = Mount(
    target='/home/glue_user/.aws',
    source=f'{home_dir}/.aws',
    type='bind',
    read_only=False,
    consistency='delegated'
)

data_mount = Mount(
    target='/home/glue_user/data/csv',
    source=f'{os.path.dirname(cwd)}/data',
    type='bind',
    read_only=False
)

workspace_mount = Mount(
    target='/home/glue_user/workspace',
    source=cwd,
    type='bind',
    read_only=False
)


def get_aws_config(param):
    try:
        result = subprocess.run(['aws', 'configure', 'get', param],
                                capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None


# Get AWS credentials
aws_access_key_id = get_aws_config('aws_access_key_id')
aws_secret_access_key = get_aws_config('aws_secret_access_key')
aws_session_token = get_aws_config('aws_session_token')
aws_region = get_aws_config('region')

# Define the DAG
with DAG(
        'glue_jobs_sequential_local',
        default_args=default_args,
        description='Run two Glue jobs sequentially in Glue container locally',
        schedule_interval=None,  # Set to None for manual trigger or define a schedule
) as dag:
    # Run first Glue job inside Docker container
    run_process_files_job = DockerOperator(
        task_id='run_process_files_job',
        image='glue-local-dev',
        command='spark-submit /home/glue_user/workspace/process_files.py',
        auto_remove='force',
        container_name='glue_local_dev',
        mounts=[aws_mount, data_mount, workspace_mount],
        environment={
            'AWS_ACCESS_KEY_ID': aws_access_key_id,
            'AWS_SECRET_ACCESS_KEY': aws_secret_access_key,
            'AWS_SESSION_TOKEN': aws_session_token,
            'AWS_REGION': aws_region
        },
        dag=dag,
    )

    run_write_redshift_job = DockerOperator(
        task_id='run_write_redshift_job',
        image='glue-local-dev',  # Replace with the correct Docker image name
        api_version='auto',
        auto_remove="force",  # Equivalent to --rm
        command='spark-submit /home/glue_user/workspace/write_to_redshift.py',
        mounts=[aws_mount, data_mount, workspace_mount],
        environment={
            'AWS_ACCESS_KEY_ID': aws_access_key_id,
            'AWS_SECRET_ACCESS_KEY': aws_secret_access_key,
            'AWS_SESSION_TOKEN': aws_session_token,
            'AWS_REGION': aws_region
        },
        network_mode='host',  # Ensures proper networking
        dag=dag,
    )

    run_process_files_job >> run_write_redshift_job
