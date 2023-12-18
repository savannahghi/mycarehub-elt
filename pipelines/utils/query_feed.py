"""Read SQL queries from GCS"""
from pipelines.utils import google_clients, config

gcs_client = google_clients.initialize_gcs_client()


class QueryFeed:
    def __init__(self, folder, bucket=None, dataset=None):
        self.folder = folder
        self.dataset = dataset
        self.bucket = bucket

    def get_sql_files(self, query_folder):
        self.folder = query_folder
        files = [
            f.name
            for f in gcs_client.list_blobs(
                bucket_or_name=config.mycarehub_queries, prefix=query_folder
            )
            if ".sql" in f.name
        ]
        return files

    def get_location_names(self, query_folder, bucket=None, dataset=None):
        self.folder = query_folder
        if bucket is not None:
            location = [
                f"{bucket}/{(file.name.split('.')[0]).split('/')[-1]}"
                for file in gcs_client.list_blobs(
                    bucket_or_name=config.mycarehub_queries, prefix=query_folder
                )
                if ".sql" in file.name
            ]
        else:
            location = [
                f"{dataset}.{(file.name.split('.')[0]).split('/')[-1]}"
                for file in gcs_client.list_blobs(
                    bucket_or_name=config.mycarehub_queries, prefix=query_folder
                )
                if ".sql" in file.name
            ]
        return location

    def read_queries(self, query_folder):
        """Read Query."""
        files = self.get_sql_files(query_folder)
        bucket = gcs_client.get_bucket(config.mycarehub_queries)
        file_contents = []
        for file in files:
            blob = bucket.blob(file)
            query = blob.download_as_text()
            file_contents.append(query)
        return file_contents

    def create_query_dict(self, query_folder, bucket=None, dataset=None):
        """Create dictionary for logging purposes."""
        self.folder = query_folder
        file_contents = self.read_queries(query_folder)
        location = self.get_location_names(query_folder, bucket, dataset)
        files = dict(zip(location, file_contents))
        return files
