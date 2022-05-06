import logging
from pathlib import Path

import fastparquet
import pandas as pd

from pipelines.utils import google_clients, config

logging.basicConfig(level=logging.INFO)
gcs_client = google_clients.initialize_gcs_client()
folder = config.queries


class DataClient:
    def __init__(self, client):
        self.client = client
        self.location = None

    def fetch_rows(self, query, engine, location=None):
        """Query Actisure DBs and Load Data to GCS DataLake."""
        self.location = location
        chunk_number = 0
        dir_path = Path(f"{folder}/{location.split('/')[-2]}")
        dir_path.mkdir(parents=True, exist_ok=True)
        file_name = f"{folder}/{location.partition('/')[2]}.parquet"
        Path(file_name).touch()
        conn = engine.connect()
        result = conn.execution_options(stream_results=True).execute(query)
        row_batch = result.fetchmany(size=100000)
        append = False
        while len(row_batch) > 0:
            chunk_number += 1
            chunk = pd.DataFrame(row_batch)
            chunk.columns = result.keys()
            fastparquet.write(
                filename=file_name, data=chunk,
                compression="GZIP", append=append
            )
            append = True
            logging.info(
                f"Chunk {chunk_number} :"
                f"Fetched {chunk.shape[0]} "
                f"rows and Inserted "
                f"{chunk.shape[0]} into {file_name} with "
                f"{chunk.shape[1]} columns:{chunk.columns}"
            )
            row_batch = result.fetchmany(size=100000)

    def load_to_gcs(self, location=None):
        self.location = location
        file_name = f"{folder}/{location.partition('/')[2]}.parquet"
        blob_path = f"{location.partition('/')[2]}.parquet"
        bucket_name = location.partition("/")[0]
        bucket = gcs_client.get_bucket(bucket_name)
        blob = bucket.blob(blob_path)
        blob.upload_from_filename(filename=file_name)
        Path(file_name).unlink()
        logging.info(f"{blob_path} uploaded to GCS ")
