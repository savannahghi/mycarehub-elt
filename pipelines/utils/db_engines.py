"""Fetch Database URIs and Create SQLAlchemy Engines."""
from google.cloud import secretmanager
from sqlalchemy.engine import create_engine

# Retrieve URIs from Secret Manager
secret_manager_client = secretmanager.SecretManagerServiceClient()
ssl_mode = "?sslmode=require"

mycarehub_uri = secret_manager_client.access_secret_version(
    "projects/rdo-reporting/secrets/mycarehub_uri/versions/1"
).payload.data.decode("utf-8")
mycarehub_uri += ssl_mode

# Generate DB engines
mycarehub_engine = create_engine(
    mycarehub_uri
)
