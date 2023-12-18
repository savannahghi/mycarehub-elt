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
    dag_id="mch_assessment_responses",
    description="Assessment responses on Mycarehub",
    schedule_interval="0 */4 * * *",
    default_args=default_args,
    catchup=False,
)

assessment_responses_ext = PythonOperator(
    task_id="assessment_responses_extract_to_gcs",
    python_callable=trigger.trigger_to_gcs,
    op_kwargs={'folder': config.mch_assessment_responses_fold,
               'engine': db_engines.mycarehub_engine,
               'bucket': config.mch_assessment_responses_bket},
    dag=etl_dag
)

assessment_responses_load = PythonOperator(
    task_id="assessment_responses_load_to_bquery",
    python_callable=trigger.trigger_to_bquery,
    op_kwargs={'folder': config.mch_assessment_responses_fold,
               'dataset': config.mch_assessment_responses_dset,
               'bucket': config.mch_assessment_responses_bket},
    dag=etl_dag
)
assessment_responses_staging = PythonOperator(
    task_id="mch_assessment_responses_staging",
    python_callable=run.trigger_staging,
    op_kwargs={'folder': config.mch_assessment_responses_staging_fold,
               'dataset': config.mch_assessment_responses_dset},
    dag=etl_dag
)
# Task Dependencies
assessment_responses_ext >> assessment_responses_load >> assessment_responses_staging

