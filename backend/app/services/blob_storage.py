import os
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

load_dotenv()
blob_service_client = BlobServiceClient.from_connection_string(os.getenv("AZURE_STORAGE_CONNECTION_STRING"))
container_name = os.getenv("AZURE_STORAGE_CONTAINER")

def upload_to_blob(filename: str, content: bytes):
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=filename)
    blob_client.upload_blob(content, overwrite=True)
