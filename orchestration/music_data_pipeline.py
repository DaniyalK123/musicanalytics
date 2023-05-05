import datetime
import os
from pathlib import Path
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

# Import your custom data extraction function from data_extraction.py
from data_extraction import extract_music_data

# Define the BigQuery load function
def load_data_to_bigquery():
    bigquery_project_id = os.environ.get("BIGQUERY_PROJECT_ID")
    bigquery_dataset_name = os.environ.get("BIGQUERY_DATASET_NAME")
    gcs_bucket_name = os.environ.get("GCS_BUCKET_NAME")
    gcs_path = os.environ.get("GCS_PATH")

    os.system(f"bq load --source_format=PARQUET {bigquery_project_id}:{bigquery_dataset_name}.music_data gs://{gcs_bucket_name}/{gcs_path}/*.parquet")

# Set the default arguments for the DAG
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": datetime.timedelta(minutes=5),
    "start_date": datetime.datetime.now(),
}

# Define the DAG
dag = DAG(
    "music_data_pipeline",
    default_args=default_args,
    description="A music data pipeline that extracts data, loads it into BigQuery and runs dbt transformations.",
    schedule_interval=datetime.timedelta(weeks=1),
    catchup=False,
)

# Define the data extraction task
extract_data_task = PythonOperator(
    task_id="extract_music_data",
    python_callable=extract_music_data,
    dag=dag,
)

# Define the BigQuery load task
load_data_to_bigquery_task = PythonOperator(
    task_id="load_data_to_bigquery",
    python_callable=load_data_to_bigquery,
    dag=dag,
)

# Define the dbt run task
dbt_run_task = BashOperator(
    task_id="dbt_run",
    bash_command="dbt run",
    dag=dag,
)

# Define the dependencies between tasks
extract_data_task >> load_data_to_bigquery_task >> dbt_run_task
