"""Authenticate and Initialize Google Clients."""
import json

from google.cloud import bigquery, secretmanager, storage
from google.oauth2.service_account import Credentials


def gcp_authentication():
    """Fetch GCP Credentials from secret manager."""
    # Set Google Credentials from Secret Manager
    secret_manager_client = secretmanager.SecretManagerServiceClient()
    service_account_file = secret_manager_client.access_secret_version(
        "projects/sghi-307909/secrets/mycarehub-elt/versions/1"
    ).payload.data.decode("utf-8")

    # Convert Credentials to python object
    info = json.loads(service_account_file)

    # Credentials to Authenticate
    credentials = Credentials.from_service_account_info(
        info=info,
        scopes=[
            "https://www.googleapis.com/auth/drive",
            "https://www.googleapis.com/auth/bigquery",
            "https://www.googleapis.com/auth/devstorage.full_control",
            "https://www.googleapis.com/auth/devstorage.read_only",
            "https://www.googleapis.com/auth/devstorage.read_write",
        ],
    )
    return credentials


def initialize_bq_client():
    """Initialize BQuery Client."""
    credentials = gcp_authentication()
    bq_client = bigquery.Client(credentials=credentials,
                                project=credentials.project_id)
    return bq_client


def initialize_gcs_client():
    """Initialize BQuery Client."""
    credentials = gcp_authentication()
    gcs_client = storage.Client(credentials=credentials,
                                project=credentials.project_id)

    return gcs_client


def initialize_secret_manager():
    """Initialize a secret manager client."""
    secret_manager_client = secretmanager.SecretManagerServiceClient()
    return secret_manager_client
