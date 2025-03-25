import os
import requests
from dotenv import load_dotenv

load_dotenv()

search_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
search_key = os.getenv("AZURE_SEARCH_KEY")
index_name = os.getenv("AZURE_SEARCH_INDEX")

url = f"{search_endpoint}/indexes/{index_name}?api-version=2023-07-01-Preview"

headers = {
    "Content-Type": "application/json",
    "api-key": search_key
}

schema = {
    "name": index_name,
    "fields": [
        {"name": "id", "type": "Edm.String", "key": True, "searchable": False},
        {"name": "content", "type": "Edm.String", "searchable": True},
        {"name": "contentVector", "type": "Collection(Edm.Single)", "searchable": True, "vectorSearchDimensions": 1536, "vectorSearchConfiguration": "default"}
    ],
    "vectorSearch": {
        "algorithmConfigurations": [
            {
                "name": "default",
                "kind": "hnsw",
                "hnswParameters": {
                    "m": 4,
                    "efConstruction": 400
                }
            }
        ]
    }
}

response = requests.put(url, headers=headers, json=schema)
print(response.status_code, response.text)
