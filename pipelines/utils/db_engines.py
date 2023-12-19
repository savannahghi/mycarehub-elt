"""Fetch Database URIs and Create SQLAlchemy Engines."""
import toml
from google.cloud import secretmanager
from sqlalchemy.engine import create_engine

from pipelines.utils import google_clients

# Retrieve URIs from Secret Manager
secret_manager_client = secretmanager.SecretManagerServiceClient()

# get & deserialize config.toml from gcs
c_client = google_clients.initialize_gcs_client()
c_bucket = c_client.get_bucket("mycarehub-queries")
c_blob = c_bucket.get_blob("config/db_engines.toml")
toml_string = c_blob.download_as_bytes().decode("utf-8")
parsed_config = toml.loads(toml_string)

# parse through config keys and dynamically create variables


def get_engine(engine_key):
    engine_uri = secret_manager_client.access_secret_version(
        request={"name": f"projects/sghi-307909/secrets/{parsed_config[engine_key]['engine_uri']}/versions/latest"}
    ).payload.data.decode("utf-8")

    db = "POSTGRES"
    if "db_type" in parsed_config[engine_key]:
        db = parsed_config[engine_key]["db_type"]

    if db == "POSTGRES":
        return create_engine(
            engine_uri,
            connect_args={"options": f"-c statement_timeout={parsed_config[engine_key]['timeout']}"},
        )
    else:
        return create_engine(
            engine_uri,
        )
