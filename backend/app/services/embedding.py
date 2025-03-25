import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("AZURE_OPENAI_KEY")
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
openai.api_type = "azure"
openai.api_version = "2023-05-15"

def get_embedding(text):
    result = openai.Embedding.create(
        input=[text],
        engine="text-embedding-ada-002"
    )
    return result['data'][0]['embedding']
