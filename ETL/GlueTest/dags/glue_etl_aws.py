from airflow import DAG
from airflow.providers.amazon.aws.operators.glue import GlueJobOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'retries': 1,
}

with DAG(
        'glue_jobs_aws',
        default_args=default_args,
        description='Run two Glue jobs sequentially in Glue container locally',
        schedule_interval=None,
) as dag:
    # Define the Glue job for process_files
    run_process_files_job = GlueJobOperator(
        task_id='run_process_files_job',
        job_name='process_files_etl_job',  # The name of your Glue job
        script_location='s3://your-bucket/scripts/process_files.py',  # S3 location of your script
        aws_conn_id='aws_default',  # Your Airflow AWS connection ID
        region_name='us-east-1',  # Your AWS region
        wait_for_completion=True,  # Wait for the job to complete before proceeding
        create_job_kwargs={
            "GlueVersion": "3.0",  # Or the version you've selected
            "NumberOfWorkers": 2,
            "WorkerType": "G.1X",
            "DefaultArguments": {
                '--job-language': 'python',
                '--job-bookmark-option': 'job-bookmark-disable',
            },
        },
        dag=dag,
    )

    # Define the Glue job for write_to_redshift
    run_write_redshift_job = GlueJobOperator(
        task_id='run_write_redshift_job',
        job_name='write_to_redshift_etl_job',  # The name of your Glue job
        script_location='s3://your-bucket/scripts/write_to_redshift.py',  # S3 location of your script
        aws_conn_id='aws_default',  # Your Airflow AWS connection ID
        region_name='us-east-1',  # Your AWS region
        wait_for_completion=True,  # Wait for the job to complete before proceeding
        create_job_kwargs={
            "GlueVersion": "3.0",
            "NumberOfWorkers": 2,
            "WorkerType": "G.1X",
            "DefaultArguments": {
                '--job-language': 'python',
                '--job-bookmark-option': 'job-bookmark-disable',
            },
        },
        dag=dag,
    )

    run_process_files_job >> run_write_redshift_job
