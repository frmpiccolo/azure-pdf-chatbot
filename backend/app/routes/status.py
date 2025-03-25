from fastapi import APIRouter
from app.services.search import get_index_stats

router = APIRouter(prefix="/status", tags=["Status"])

@router.get("/")
async def get_status():
    return {"status": await get_index_stats()}