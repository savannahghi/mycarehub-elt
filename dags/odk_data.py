"""Airflow DAG to run ETL Jobs."""
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from pipelines.extract import trigger
from pipelines.staging import run
from pipelines.utils import config, db_engines

# Initialize DAG
default_args = {
    "owner": "mycarehub",
    "depends_on_past": False,
    "start_date": datetime(2021, 10, 12),
    "email": ["airflow@example.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 4,
    "retry_delay": timedelta(minutes=10),
}

etl_dag = DAG(
    dag_id="odk_data",
    description="Odk Response and Forms",
    schedule_interval="0 */4 * * *",
    default_args=default_args,
    catchup=False,
)

odk_ext = PythonOperator(
    task_id="odk_extract_to_gcs",
    python_callable=trigger.trigger_to_gcs,
    op_kwargs={'folder': config.odk_data_fold,
               'engine': db_engines.get_engine("odk_engine"),
               'bucket': config.odk_data_bket},
    dag=etl_dag
)

odk_load = PythonOperator(
    task_id="odk_load_to_bquery",
    python_callable=trigger.trigger_to_bquery,
    op_kwargs={'folder': config.odk_data_fold,
               'dataset': config.odk_data_dset,
               'bucket': config.odk_data_bket},
    dag=etl_dag
)

odk_staging = PythonOperator(
    task_id="odk_staging",
    python_callable=run.trigger_staging,
    op_kwargs={'folder': config.odk_data_staging_fold,
               'dataset': config.odk_data_dset},
    dag=etl_dag
)
# Task Dependencies
odk_ext >> odk_load >> odk_staging
