from datetime import datetime
from typing import List
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os

from azure.search.documents.aio import SearchClient
from azure.search.documents.models import QueryType
from azure.core.credentials import AzureKeyCredential

from app.utils.sanitize import sanitize_id
from app.services.blob import list_files_in_blob

load_dotenv()

router = APIRouter(prefix="/files", tags=["Files"])

class FileInfo(BaseModel):
    filename: str
    size: int
    uploadedAt: datetime
    indexed: bool

@router.get("/", response_model=List[FileInfo])
async def list_files():
    try:
        blobs = await list_files_in_blob()
        results: List[FileInfo] = []

        async with SearchClient(
            endpoint=os.getenv("AZURE_SEARCH_ENDPOINT"),
            index_name=os.getenv("AZURE_SEARCH_INDEX"),
            credential=AzureKeyCredential(os.getenv("AZURE_SEARCH_KEY")),
        ) as search_client:

            for blob in blobs:
                filename = blob.name
                size = blob.size or 0
                uploaded = blob.last_modified or datetime.utcnow()

                # Sanitize the ID used for indexing chunks
                safe_id = sanitize_id(filename)

                # Perform search using search_text in ID field
                search_result = await search_client.search(
                    search_text=safe_id,
                    search_fields=["id"],
                    query_type=QueryType.SIMPLE,
                    select=["id"],
                    top=1,
                )

                indexed = False
                async for _ in search_result:
                    indexed = True
                    break

                results.append(FileInfo(
                    filename=filename,
                    size=size,
                    uploadedAt=uploaded,
                    indexed=indexed,
                ))

        return results

    except Exception as e:
        print(f"❌ Error in /files: {e}")
        raise HTTPException(status_code=500, detail=str(e))
