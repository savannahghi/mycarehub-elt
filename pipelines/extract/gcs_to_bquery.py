from google.cloud import bigquery

from pipelines.utils import google_clients

bq_client = google_clients.initialize_bq_client()


def load_to_bquery(bucket, location=None):
    gcs_uri = f"gs://{bucket}/{location.split('.', 2)[-1]}.parquet"
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.PARQUET,
        write_disposition="WRITE_TRUNCATE",
        create_disposition="CREATE_IF_NEEDED",
    )
    load_job = bq_client.load_table_from_uri(gcs_uri, location,
                                             job_config=job_config)
    load_job.result()
    return response(location)


def response(location):
    print(f"Table: {location} loaded")
