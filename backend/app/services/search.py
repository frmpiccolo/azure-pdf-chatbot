import os
from dotenv import load_dotenv
from typing import List
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.aio import SearchClient
from azure.search.documents.indexes.aio import SearchIndexClient
from azure.search.documents.models import VectorizedQuery
from app.services.openai import get_embedding

load_dotenv()

endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
key = os.getenv("AZURE_SEARCH_KEY")
index_name = os.getenv("AZURE_SEARCH_INDEX")

credential = AzureKeyCredential(key)

async def index_document(doc_id: str, content: str, vector: List[float]):
    async with SearchClient(endpoint=endpoint, index_name=index_name, credential=credential) as client:
        document = {
            "id": doc_id,
            "content": content,
            "contentVector": vector,
        }
        await client.upload_documents(documents=[document])

async def semantic_search(query: str) -> str:
    async with SearchClient(endpoint=endpoint, index_name=index_name, credential=credential) as client:
        results = await client.search(query, top=3)
        chunks = []
        async for result in results:
            chunks.append(result["content"])
        return "\n---\n".join(chunks)

async def semantic_search_vector_based(query: str, top_k: int = 3) -> str:
    embedding = await get_embedding(query)

    vector_query = VectorizedQuery(        
        fields="contentVector",
        vector=embedding,
        k_nearest_neighbors=top_k
    )

    async with SearchClient(endpoint=endpoint, index_name=index_name, credential=credential) as client:
        results = await client.search(
            vector_queries=[vector_query],
            select=["content"]
        )

        chunks = []
        async for result in results:
            chunks.append(result["content"])

        return "\n---\n".join(chunks)

async def get_index_stats() -> str:
    async with SearchIndexClient(endpoint=endpoint, credential=credential) as client:
        result = await client.get_index_statistics(index_name)        
        count = result["document_count"]
        return f"{count} documents indexed"
