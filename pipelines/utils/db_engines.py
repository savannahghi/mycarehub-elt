"""Fetch Database URIs and Create SQLAlchemy Engines."""
from google.cloud import secretmanager
from sqlalchemy.engine import create_engine

# Retrieve URIs from Secret Manager
secret_manager_client = secretmanager.SecretManagerServiceClient()

mch_cloudsql_uri = secret_manager_client.access_secret_version(
    "projects/sghi-307909/secrets/mch_cloudsql_uri/versions/1"
).payload.data.decode("utf-8")
openmrs_cloudsql_uri = secret_manager_client.access_secret_version(
    "projects/sghi-307909/secrets/openmrs_cloudsql_uri/versions/1"
).payload.data.decode("utf-8")

# Generate DB engines
mycarehub_engine = create_engine(
    mch_cloudsql_uri,
)
openmrs_engine = create_engine(
    openmrs_cloudsql_uri,
)