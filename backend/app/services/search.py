import os
import requests
from app.services.embedding import get_embedding
from dotenv import load_dotenv

load_dotenv()

search_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
search_key = os.getenv("AZURE_SEARCH_KEY")
index_name = os.getenv("AZURE_SEARCH_INDEX")

def query_vector_index(question: str) -> str:
    embedding = get_embedding(question)

    url = f"{search_endpoint}/indexes/{index_name}/docs/search?api-version=2023-07-01-Preview"
    headers = {
        "Content-Type": "application/json",
        "api-key": search_key
    }

    payload = {
        "vector": {
            "value": embedding,
            "fields": "contentVector",
            "k": 3
        },
        "select": "content"
    }

    response = requests.post(url, headers=headers, json=payload)
    results = response.json()

    hits = results.get("value", [])
    context = "\n\n".join([hit["content"] for hit in hits])

    return generate_answer(question, context)

def generate_answer(question: str, context: str) -> str:
    from openai import AzureOpenAI
    client = AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_KEY"),
        api_version="2023-05-15",
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    )

    system_message = (
        "You are a helpful assistant answering questions based only on the provided context. "
        "Do not guess. If the answer is not in the context, say you don't know."
    )

    completion = client.chat.completions.create(
        deployment_id="gpt35",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
        ]
    )

    return completion.choices[0].message.content.strip()
