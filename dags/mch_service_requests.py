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
    dag_id="mch_service_requests",
    description="Service Requests in MCH",
    schedule_interval="0 */4 * * *",
    default_args=default_args,
    catchup=False,
)

service_requests_ext = PythonOperator(
    task_id="service_requests_extract_to_gcs",
    python_callable=trigger.trigger_to_gcs,
    op_kwargs={'folder': config.mch_service_requests_fold,
               'engine': db_engines.get_engine("mycarehub_engine"),
               'bucket': config.mch_service_requests_bket},
    dag=etl_dag
)

service_requests_load = PythonOperator(
    task_id="service_requests_load_to_bquery",
    python_callable=trigger.trigger_to_bquery,
    op_kwargs={'folder': config.mch_service_requests_fold,
               'dataset': config.mch_service_requests_dset,
               'bucket': config.mch_service_requests_bket},
    dag=etl_dag
)

service_requests_staging = PythonOperator(
    task_id="mch_service_requests_staging",
    python_callable=run.trigger_staging,
    op_kwargs={'folder': config.mch_service_requests_staging_fold,
               'dataset': config.mch_service_requests_dset},
    dag=etl_dag
)

service_requests_ext_v2 = PythonOperator(
    task_id="service_requests_extract_to_gcs_v2",
    python_callable=trigger.trigger_to_gcs,
    op_kwargs={'folder': config.mch_service_requests_fold_v2,
               'engine': db_engines.get_engine("mycarehub_engine_v2"),
               'bucket': config.mch_service_requests_bket_v2},
    dag=etl_dag
)

service_requests_load_v2 = PythonOperator(
    task_id="service_requests_load_to_bquery_v2",
    python_callable=trigger.trigger_to_bquery,
    op_kwargs={'folder': config.mch_service_requests_fold_v2,
               'dataset': config.mch_service_requests_dset_v2,
               'bucket': config.mch_service_requests_bket_v2},
    dag=etl_dag
)

service_requests_staging_v2 = PythonOperator(
    task_id="mch_service_requests_staging_v2",
    python_callable=run.trigger_staging,
    op_kwargs={'folder': config.mch_service_requests_staging_fold_v2,
               'dataset': config.mch_service_requests_dset_v2},
    dag=etl_dag
)
# Task Dependencies
service_requests_ext >> service_requests_load >> service_requests_staging
service_requests_ext_v2 >> service_requests_load_v2 >> service_requests_staging_v2
