from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.search import semantic_search_vector_based
from app.services.openai import chat_with_context

router = APIRouter(prefix="/chat", tags=["Chat"])

class Question(BaseModel):
    question: str

@router.post("/")
async def chat(question: Question):
    try:
        print(f"📩 Received question: {question.question}")
        
        # Perform vector-based semantic search
        context = await semantic_search_vector_based(question.question)
        print(f"🔍 Retrieved context:\n{context}\n")

        # Use OpenAI to respond based on the context
        answer = await chat_with_context(question.question, context)
        print(f"🤖 Answer: {answer}")

        return {"answer": answer}

    except Exception as e:
        print(f"❌ Error in /chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))
