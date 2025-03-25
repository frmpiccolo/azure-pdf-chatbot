import os
from dotenv import load_dotenv
from fastapi import APIRouter, UploadFile, File, HTTPException

from app.services.blob import save_file_to_blob
from app.services.pdf_parser import extract_text_from_bytes
from app.services.openai import generate_embeddings
from app.services.search import index_document
from app.utils.sanitize import sanitize_id 

import tiktoken

router = APIRouter(prefix="/upload", tags=["Upload"])

# 🔐 Load environment and tokenizer
load_dotenv()
model = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT", "text-embedding-ada-002")
tokenizer = tiktoken.encoding_for_model(model)

# 📚 Helper: Split large text by max token count
def split_text_into_chunks(text: str, max_tokens: int = 2000) -> list[str]:
    tokens = tokenizer.encode(text)
    chunks = []

    for i in range(0, len(tokens), max_tokens):
        chunk_tokens = tokens[i:i + max_tokens]
        chunk_text = tokenizer.decode(chunk_tokens)
        chunks.append(chunk_text)

    return chunks

# 📤 Upload route
@router.post("/")
async def upload(file: UploadFile = File(...)):
    try:
        # 📥 Read file bytes
        content_bytes = await file.read()
        if not content_bytes:
            raise Exception("Uploaded file is empty.")

        # ☁️ Save to Azure Blob Storage
        filename = await save_file_to_blob(file.filename, content_bytes)
        print(f"✅ File saved: {filename}")

        # 📄 Extract text from PDF
        content = await extract_text_from_bytes(content_bytes, file.filename)
        print(f"✅ Extracted text ({len(content)} characters)")

        # ✂️ Split content if too large
        chunks = split_text_into_chunks(content)
        print(f"✂️ Text split into {len(chunks)} chunk(s)")

        # 🔁 Process each chunk: embed + index
        for i, chunk in enumerate(chunks):
            chunk_id = sanitize_id(f"{filename}_part_{i+1}" if len(chunks) > 1 else filename)

            vectors = await generate_embeddings(chunk)
            print(f"✅ Embeddings generated for chunk {i+1} ({len(vectors)} dimensions)")

            await index_document(chunk_id, chunk, vectors)
            print(f"✅ Chunk {i+1} indexed successfully.")

        return {"message": "File uploaded, processed and indexed."}

    except Exception as e:
        print(f"❌ Upload error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
