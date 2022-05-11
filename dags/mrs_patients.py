"""Airflow DAG to run ETL Jobs."""
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from pipelines.extract import trigger
from pipelines.staging import run
from pipelines.utils import config, db_engines

# Initialize DAG
default_args = {
    "owner": "Open MRS",
    "depends_on_past": False,
    "start_date": datetime(2020, 10, 12),
    "email": ["airflow@example.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 4,
    "retry_delay": timedelta(minutes=10),
}

etl_dag = DAG(
    dag_id="emr_patients",
    description="Patients on OpenMRS",
    schedule_interval="0 */4 * * *",
    default_args=default_args,
    catchup=False,
)

patients_ext = PythonOperator(
    task_id="patients_extract_to_gcs",
    python_callable=trigger.trigger_to_gcs,
    op_kwargs={'folder': config.emr_patients_fold,
               'engine': db_engines.openmrs_engine,
               'bucket': config.emr_patients_bket},
    dag=etl_dag
)

patients_load = PythonOperator(
    task_id="patients_load_to_bquery",
    python_callable=trigger.trigger_to_bquery,
    op_kwargs={'folder': config.emr_patients_fold,
               'dataset': config.emr_patients_dset,
               'bucket': config.emr_patients_bket},
    dag=etl_dag
)
patients_staging = PythonOperator(
    task_id="openmrs_patients_staging",
    python_callable=run.trigger_staging,
    op_kwargs={'folder': config.emr_patients_staging_fold,
               'dataset': config.emr_patients_dset},
    dag=etl_dag
)

# Task Dependencies
patients_ext >> patients_load >> patients_staging
