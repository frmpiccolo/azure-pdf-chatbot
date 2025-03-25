# 🤖 Azure PDF Chatbot

This project is a full-stack AI-powered chatbot that allows users to upload PDF documents and ask questions based on the content. It leverages **Azure OpenAI**, **Azure Cognitive Search**, and **Azure Blob Storage** to ingest documents, create embeddings, and provide contextual answers through a chat interface.

---

## 🎯 Purpose

This project demonstrates how to build a domain-specific chatbot using Azure AI resources, enabling knowledge extraction from private PDF files. It mimics real-world enterprise use cases like internal knowledge bases, research assistants, or legal document analyzers.

---

## 🚀 Project Structure

```
azure-pdf-chatbot/
├── backend/                # FastAPI backend with Azure integration
│   ├── app/                # Main app logic
│   ├── scripts/            # Index creation and population scripts
│   └── Dockerfile          # Docker image for backend
├── frontend/               # React frontend for chat and upload
│   └── Dockerfile          # Docker image for frontend
├── deploy/                 # Scripts for provisioning Azure resources
├── data/inputs/            # Sample PDF files
├── .github/workflows/      # CI/CD pipelines for backend and frontend
├── .env.example            # Sample environment variables
└── README.md               # Project documentation
```

---

## 📦 Requirements

### Local Setup

- [Python 3.10+](https://www.python.org/downloads/)
- [Node.js 18+](https://nodejs.org/)
- [Docker](https://www.docker.com/)
- [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli)
- An active **Azure Subscription**

### Required Azure Resources

- ✅ Azure OpenAI resource with `gpt-35-turbo` or `gpt-4`
- ✅ Azure Cognitive Search (with vector search enabled)
- ✅ Azure Blob Storage (for PDF file storage)

---

## ⚙️ Running Locally

### 1. Configure `.env`

Copy `.env.example` to `.env` and fill in your Azure keys.

---

### 2. Run with Docker

```bash
# Build backend and frontend
docker build -t azure-pdf-backend ./backend
docker build -t azure-pdf-frontend ./frontend

# Run containers
docker run -d -p 8000:8000 --env-file .env azure-pdf-backend
docker run -d -p 3000:3000 azure-pdf-frontend
```

---

### 3. Run Manually

#### Backend (FastAPI)

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

#### Frontend (React)

```bash
cd frontend
npm install
npm start
```

Open: [http://localhost:3000](http://localhost:3000)

---

## ☁️ Azure Deployment

### 🔧 Provision Azure Resources

```bash
az login
cd deploy
bash provision.sh
```

> This script provisions:
> - Azure Cognitive Search
> - Azure Blob Storage
> - Azure OpenAI resource
> - Outputs keys for your `.env` file

---

### 🐳 Publish Backend to Azure

#### Option 1: Azure App Service (Docker)

```bash
# Build and push to ACR
docker build -t <registry>/azure-pdf-backend:latest ./backend
docker push <registry>/azure-pdf-backend:latest

# Deploy to Web App
az webapp create --name azure-pdf-backend \
  --resource-group <rg> \
  --plan <plan> \
  --deployment-container-image-name <registry>/azure-pdf-backend:latest
```

#### Option 2: Azure Container Apps

Use Bicep/Terraform or az CLI to deploy with container image.

---

### 🌐 Publish Frontend to Azure

#### Option 1: Azure Static Web Apps

- Configure GitHub Actions with `AZURE_STATIC_WEB_APPS_API_TOKEN`
- Push to main to trigger deployment

#### Option 2: Azure App Service (Node)

```bash
az webapp up --name azure-pdf-chatbot-ui --runtime "NODE:18LTS" --resource-group <your-rg>
```

---

## 🔁 CI/CD with GitHub Actions

This project includes:

- `backend.yml`: Docker build & push to Azure Container Registry + App Service deploy
- `frontend.yml`: React build + deploy to Azure Static Web App

Secrets required:
- `AZURE_CREDENTIALS`
- `REGISTRY_USERNAME` / `REGISTRY_PASSWORD`
- `AZURE_STATIC_WEB_APPS_API_TOKEN`

---

## 🧪 Sample Dataset

Use any PDF file, or the example in `data/inputs/sample.pdf`. Upload it and test your chatbot!

---

## 🔍 Features

- Upload and parse PDF documents
- Generate and index embeddings with Azure OpenAI + Cognitive Search
- Vector-based semantic search
- Context-aware Q&A using Azure GPT
- Dockerized + deployable with CI/CD

---

## 📸 Screenshots

```
📤 PDF Upload UI
💬 Chat interface
🧠 Relevant response from document context
```

---

## 🧰 Troubleshooting

- **CORS Errors:** Ensure frontend and backend URLs are aligned
- **Missing index?** Run the script to create and populate it
- **Auth Errors:** Check API keys in `.env`
- **Empty results?** Try uploading fresh content and re-embedding

---

## 📜 Disclaimer

This is a demo project for learning and portfolio use. Azure services used here may generate cost. Always monitor your usage via Azure Portal and set budget alerts.

---

## 🧠 What I Learned

- Azure AI integration for real-world LLM solutions
- Full-stack FastAPI + React development
- Vector search with Cognitive Search
- CI/CD pipelines and Docker deployment

---

## 📬 Contact

Created by [Fermin Piccolo](https://www.linkedin.com/in/ferminpiccolo)

---