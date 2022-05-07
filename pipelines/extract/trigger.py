"""Initialize extraction pipeline."""
import logging

from pipelines.extract import query_client, gcs_to_bquery
from pipelines.utils import google_clients, query_feed


def trigger_to_gcs(folder, engine, bucket):
    """Trigger extraction pipeline."""
    gcs_client = google_clients.initialize_gcs_client()
    queries = query_feed.QueryFeed(folder=folder,
                                   bucket=bucket).create_query_dict(
        query_folder=folder, bucket=bucket
    )
    client = query_client.DataClient(gcs_client)
    for location, query in queries.items():
        fetch_rows = client.fetch_rows(query, engine, location)
        load_to_gcs = client.load_to_gcs(location)
        logging.info(fetch_rows, load_to_gcs)


def trigger_to_bquery(folder, dataset, bucket):
    blobs_list = query_feed.QueryFeed(
        folder=folder, dataset=dataset
    ).get_location_names(query_folder=folder, dataset=dataset)
    for blobs in blobs_list:
        load_to_bq = gcs_to_bquery.load_to_bquery(bucket, blobs)
        logging.info(load_to_bq)
