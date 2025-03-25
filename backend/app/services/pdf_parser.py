from PyPDF2 import PdfReader
from io import BytesIO

async def extract_text_from_bytes(file_bytes: bytes, filename: str) -> str:
    if filename.lower().endswith(".pdf"):
        try:
            reader = PdfReader(BytesIO(file_bytes))
            return "\n".join([page.extract_text() or "" for page in reader.pages])
        except Exception as e:
            raise Exception(f"Error reading PDF: {e}")
    else:
        try:
            return file_bytes.decode("utf-8")
        except Exception as e:
            raise Exception(f"Unsupported file type or decoding error: {e}")
