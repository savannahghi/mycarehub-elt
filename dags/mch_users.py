"""Airflow DAG to run ETL Jobs."""
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from pipelines.extract import trigger

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
    dag_id="mch_users",
    description="Registered users on Mycarehub",
    schedule_interval="0 */4 * * *",
    default_args=default_args,
    catchup=False,
)

users_ext = PythonOperator(
    task_id="users_extract_to_gcs",
    python_callable=trigger.trigger_to_gcs(),
    op_kwargs={'folder': config.mch_users_fold,
               'engine': db_engines.mycarehub_engine,
               'bucket': config.mch_users_bket},
    dag=etl_dag
)

users_load = PythonOperator(
    task_id="users_load_to_bquery",
    python_callable=trigger.trigger_to_bquery,
    op_kwargs={'folder': config.mch_users_fold,
               'dataset': config.mch_users_dset,
               'bucket': config.mch_users_bket},
    dag=etl_dag
)

# Task Dependencies
users_ext >> users_load
