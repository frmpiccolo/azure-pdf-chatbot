import os
import requests
import uuid
from dotenv import load_dotenv
from app.utils.pdf_extractor import extract_text
from app.services.embedding import get_embedding

load_dotenv()

search_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
search_key = os.getenv("AZURE_SEARCH_KEY")
index_name = os.getenv("AZURE_SEARCH_INDEX")

def upload_document(text: str):
    vector = get_embedding(text)
    payload = {
        "value": [
            {
                "@search.action": "upload",
                "id": str(uuid.uuid4()),
                "content": text,
                "contentVector": vector
            }
        ]
    }

    url = f"{search_endpoint}/indexes/{index_name}/docs/index?api-version=2023-07-01-Preview"
    headers = {
        "Content-Type": "application/json",
        "api-key": search_key
    }

    r = requests.post(url, headers=headers, json=payload)
    print(r.status_code, r.text)

if __name__ == "__main__":
    with open("data/inputs/sample.pdf", "rb") as f:
        pdf_bytes = f.read()
        text = extract_text(pdf_bytes)
        upload_document(text)
