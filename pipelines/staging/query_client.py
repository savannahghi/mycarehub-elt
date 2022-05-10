"""Query and set Job configuration."""
from google.cloud import bigquery

from pipelines.utils.google_clients import initialize_bq_client

bquery_client = initialize_bq_client()


class DataClient:
    """
    DataClient Class.

    ...

    Attributes
    ----------
    client : str
        BQuery Client

    Methods
    -------
    query():
        Run query by passing query statement
    """

    def __init__(self, client):
        """
        Construct all the necessary attributes for the DataClient object.

        Parameters
        ----------
            client : str
                Bigquery Client

        """
        self.client = client
        self.table_name = None

    def query(self, query, table=None, site=None):
        """
        Query a BigQuery table using an SQL statement.

        Parameters
        ----------
        :param site:
        :param query: str
            SQL Query Statement

        :param table: str
            BigQuery table to save query results
        Returns
        -------
        Response object

        """
        self.table_name = table
        # Set up Parameters for Query
        job = bigquery.QueryJobConfig()
        query = query.format(dataset=site)
        job.destination = table
        job.write_disposition = bigquery.WriteDisposition().WRITE_TRUNCATE
        job.create_disposition = bigquery.CreateDisposition().CREATE_IF_NEEDED
        run = bquery_client.query(query, location="EU", job_config=job)
        run.result()
        return self.query_response(table)

    @staticmethod
    def query_response(table):
        """Response to show query execution."""
        return f"Query Complete. {table} is updated"
