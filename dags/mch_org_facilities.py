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
    dag_id="mch_org_facilities",
    description="Facilities and Organisations in MCH",
    schedule_interval="0 */4 * * *",
    default_args=default_args,
    catchup=False,
)

org_facilities_ext = PythonOperator(
    task_id="facilities_orgs_extract_to_gcs",
    python_callable=trigger.trigger_to_gcs,
    op_kwargs={'folder': config.mch_fac_org_fold,
               'engine': db_engines.get_engine("mycarehub_engine"),
               'bucket': config.mch_fac_org_bket},
    dag=etl_dag
)

org_facilities_load = PythonOperator(
    task_id="facilities_orgs_load_to_bquery",
    python_callable=trigger.trigger_to_bquery,
    op_kwargs={'folder': config.mch_fac_org_fold,
               'dataset': config.mch_fac_org_dset,
               'bucket': config.mch_fac_org_bket},
    dag=etl_dag
)

org_facilities_ext_v2 = PythonOperator(
    task_id="facilities_orgs_extract_to_gcs_v2",
    python_callable=trigger.trigger_to_gcs,
    op_kwargs={'folder': config.mch_fac_org_fold_v2,
               'engine': db_engines.get_engine("mycarehub_engine_v2"),
               'bucket': config.mch_fac_org_bket_v2},
    dag=etl_dag
)

org_facilities_load_v2 = PythonOperator(
    task_id="facilities_orgs_load_to_bquery_v2",
    python_callable=trigger.trigger_to_bquery,
    op_kwargs={'folder': config.mch_fac_org_fold_v2,
               'dataset': config.mch_fac_org_dset_v2,
               'bucket': config.mch_fac_org_bket_v2},
    dag=etl_dag
)

# Task Dependencies
org_facilities_ext >> org_facilities_load
org_facilities_ext_v2 >> org_facilities_load_v2
