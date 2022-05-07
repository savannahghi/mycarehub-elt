import toml
from pipelines.utils import google_clients

# get & deserialize config.toml from gcs
c_client = google_clients.initialize_gcs_client()
c_bucket = c_client.get_bucket("mycarehub-queries")
c_blob = c_bucket.get_blob("config/config.toml")
toml_string = c_blob.download_as_string().decode("utf-8")
parsed_config = toml.loads(toml_string)

# parse through config keys and dynamically create variables :)
for key in parsed_config.keys():
    for var in parsed_config[key]:
        globals()[var] = parsed_config[key][var]
