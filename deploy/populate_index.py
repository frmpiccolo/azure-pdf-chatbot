import os
import uuid
import sys
import requests
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

    response = requests.post(url, headers=headers, json=payload)
    print(response.status_code, response.text)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python populate_index.py <path_to_pdf>")
        sys.exit(1)

    pdf_path = sys.argv[1]
    if not os.path.isfile(pdf_path):
        print(f"File not found: {pdf_path}")
        sys.exit(1)

    with open(pdf_path, "rb") as f:
        pdf_bytes = f.read()
        text = extract_text(pdf_bytes)
        upload_document(text)
