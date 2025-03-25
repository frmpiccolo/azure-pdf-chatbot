import os
from uuid import uuid4
from dotenv import load_dotenv
from azure.storage.blob.aio import BlobServiceClient

load_dotenv()

CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
CONTAINER_NAME = os.getenv("AZURE_STORAGE_CONTAINER")

async def get_blob_service():
    return BlobServiceClient.from_connection_string(CONNECTION_STRING)

async def save_file_to_blob(filename: str, content_bytes: bytes) -> str:
    name = f"{uuid4()}_{filename}"
    blob_service = await get_blob_service()
    blob_client = blob_service.get_blob_client(container=CONTAINER_NAME, blob=name)
    await blob_client.upload_blob(content_bytes)
    return name

async def list_files_in_blob():
    blob_service = await get_blob_service()
    container = blob_service.get_container_client(CONTAINER_NAME)
    return [blob async for blob in container.list_blobs()]