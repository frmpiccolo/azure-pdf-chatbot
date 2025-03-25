from fastapi import APIRouter, UploadFile
from app.services.blob_storage import upload_to_blob
from app.utils.pdf_extractor import extract_text

router = APIRouter()

@router.post("/")
async def upload_file(file: UploadFile):
    content = await file.read()
    upload_to_blob(file.filename, content)
    text = extract_text(content)
    return {"filename": file.filename, "content_excerpt": text[:300]}
