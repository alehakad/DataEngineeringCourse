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
        task_id='process_files_job',
        job_name='process_files_job',  # The name of your Glue job
        aws_conn_id='aws_default',  # Your Airflow AWS connection ID
        region_name='eu-north-1',  # Your AWS region
        wait_for_completion=True,  # Wait for the job to complete before proceeding
        dag=dag,
    )

    # Define the Glue job for write_to_redshift
    run_write_redshift_job = GlueJobOperator(
        task_id='write_to_dynamo_script',
        job_name='write_to_dynamo_script',  # The name of your Glue job
        aws_conn_id='aws_default',  # Your Airflow AWS connection ID
        region_name='eu-north-1',  # Your AWS region
        wait_for_completion=True,  # Wait for the job to complete before proceeding
        dag=dag,
    )

    run_process_files_job >> run_write_redshift_job
