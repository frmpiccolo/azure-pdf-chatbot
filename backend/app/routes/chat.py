from fastapi import APIRouter
from pydantic import BaseModel
from app.services.search import query_vector_index

router = APIRouter()

class QuestionRequest(BaseModel):
    question: str

@router.post("/")
async def ask_question(payload: QuestionRequest):
    answer = query_vector_index(payload.question)
    return {"answer": answer}
