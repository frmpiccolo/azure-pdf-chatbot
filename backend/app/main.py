from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import upload, chat, status, files

load_dotenv()

app = FastAPI(
    title="Azure PDF Chatbot API",
    description="Backend para upload, indexação e chat com PDFs usando Azure Blob, Cognitive Search e OpenAI.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, definir domínios específicos
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(files.router)
app.include_router(upload.router)
app.include_router(chat.router)
app.include_router(status.router)
