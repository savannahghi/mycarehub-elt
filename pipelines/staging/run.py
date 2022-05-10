"""Initialize BQuery-BQuery Pipeline."""
import logging

from pipelines.staging.query_client import DataClient
from pipelines.utils import query_feed
from pipelines.utils.google_clients import initialize_bq_client

bquery_client = DataClient(initialize_bq_client())


def trigger_staging(folder, dataset, site=None):
    """Feed query parameters."""
    queries = query_feed.QueryFeed(folder=folder,
                                   dataset=dataset).create_query_dict(
        query_folder=folder, dataset=dataset
    )
    for table_name, query in queries.items():
        run_query = bquery_client.query(query, table_name, site)
        logging.info(run_query)
