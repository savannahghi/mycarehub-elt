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
    "start_date": datetime(2020, 10, 12),
    "email": ["airflow@example.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 4,
    "retry_delay": timedelta(minutes=10),
}

etl_dag = DAG(
    dag_id="ga_medical_information",
    description="Medical Information on Mycarehub from Google Analytics",
    schedule_interval="0 */4 * * *",
    default_args=default_args,
    catchup=False,
)

medical_information_extraction = PythonOperator(
    task_id="Extract_medical_information_from_GA_events",
    python_callable=run.trigger_staging,
    op_kwargs={'folder': config.GA_medical_information_fold,
               'dataset': config.GA_medical_information_dset},
    dag=etl_dag
)

medical_information_staging = PythonOperator(
    task_id="stage_medical_information_events",
    python_callable=run.trigger_staging,
    op_kwargs={'folder': config.GA_medical_information_staging_fold,
               'dataset': config.GA_medical_information_dset},
    dag=etl_dag
)

medical_information_extraction_v2 = PythonOperator(
    task_id="Extract_medical_information_from_GA_events_v2",
    python_callable=run.trigger_staging,
    op_kwargs={'folder': config.GA_medical_information_fold_v2,
               'dataset': config.GA_medical_information_dset_v2},
    dag=etl_dag
)

medical_information_staging_v2 = PythonOperator(
    task_id="stage_medical_information_events_v2",
    python_callable=run.trigger_staging,
    op_kwargs={'folder': config.GA_medical_information_staging_fold_v2,
               'dataset': config.GA_medical_information_dset_v2},
    dag=etl_dag
)

# Task Dependencies
medical_information_extraction >> medical_information_staging
medical_information_extraction_v2 >> medical_information_staging_v2
