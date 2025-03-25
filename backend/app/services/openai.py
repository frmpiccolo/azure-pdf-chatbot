import os
from dotenv import load_dotenv
from openai import AsyncAzureOpenAI

load_dotenv()

azure_openai_endpoint = "https://pdf-chatbot-openai.openai.azure.com"
api_key = os.getenv("AZURE_OPENAI_KEY")
api_version = "2023-05-15"

embedding_deployment = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT", "text-embedding-ada-002")
chat_deployment = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT", "gpt-35-turbo")

client = AsyncAzureOpenAI(
    azure_endpoint=azure_openai_endpoint,
    api_key=api_key,
    api_version=api_version,
)

async def generate_embeddings(text: str):
    result = await client.embeddings.create(
        model=embedding_deployment,
        input=text
    )
    return result.data[0].embedding

async def get_embedding(text: str):
    return await generate_embeddings(text)

async def chat_with_context(question: str, context: str) -> str:
    messages = [
        {
            "role": "system",
            "content": (
                "You are an intelligent assistant helping users retrieve answers based on a set of document excerpts.\n"
                "Use only the information from the context provided.\n"
                "If the answer is not found in the context, respond with: "
                "'I'm sorry, but I couldn't find relevant information in the provided documents.'\n"
                "Be concise, clear, and helpful."
            )
        },
        {
            "role": "user",
            "content": (
                f"Context:\n{context}\n\n"
                f"Question: {question}\n"
                f"Answer:"
            )
        }
    ]

    result = await client.chat.completions.create(
        model=chat_deployment,
        messages=messages,
        temperature=0.3,
    )

    return result.choices[0].message.content.strip()

