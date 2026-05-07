# AI Policy RAG Assistant

A Retrieval-Augmented Generation (RAG) application for asking questions about AI policy documents, currently focused on:

- EU AI Act
- GDPR
- NIST AI Risk Management Framework

This project implements an end-to-end RAG pipeline that:
- ingests PDF documents
- performs semantic retrieval
- generates grounded answers using an LLM

## Features

- PDF loading and chunking with LangChain
- Local Chroma vector store
- Hugging Face sentence-transformer embeddings
- Semantic document retrieval using embeddings (Chroma DB)
- Automatic source detection (EU AI Act / GDPR / NIST) with optional document filtering
- Configurable retrieval (`k` chunks) 
  - `k`: Number of document chunks retrieved for answering a query  
    - Lower k → faster, less context  
    - Higher k → more context, but can introduce noise  
- Groq LLM response generation
- Two modes:
  - Direct RAG execution
  - API-based interaction (FastAPI)
- Streamlit web UI
- Docker and Docker Compose support
- CLI entry point for local experimentation

## What Makes This Project Interesting

- Uses real regulatory documents (EU AI Act, GDPR, NIST AI RMF)
- Implements **source-aware retrieval** with automatic document detection
- Supports **two execution modes (Direct + API)** for flexibility
- Designed as a **modular, extensible RAG system** (not just a notebook)
- Includes **UI, API, CLI, and Docker setup** in one project

## Design Choices

- **Chunking:** Fixed-size chunks with overlap to preserve context
- **Embeddings:** Lightweight MiniLM model for fast semantic search
- **Vector DB:** Chroma for local persistence and simplicity
- **LLM:** Groq API for low-latency inference
- **Source Filtering:** Rule-based routing to improve retrieval relevance

##  Limitations

- Requires a pre-built vector store (must be generated before use)
- Source detection is rule-based and may not generalize to unseen queries
- Retrieval uses simple top-k similarity without advanced re-ranking
- Performance depends on chunking strategy and embedding quality
- Not optimized for large-scale or production deployment
- Cloud deployment on free tiers (e.g., Render) may fail due to memory constraints

## System Architecture

This project supports two modes of operation:

### 1. Direct Mode (Default)

User Query 

   ↓

Streamlit UI

   ↓

Retriever (Chroma Vector Store)
   
   ↓

Top-k Relevant Chunks

   ↓

Prompt Template

   ↓

Groq LLM (Llama 3.1)

   ↓

Answer + Sources

### 2. API Mode
User

   ↓

Streamlit UI

   ↓

FastAPI (/query endpoint)

   ↓

Retriever (Chroma Vector Store)

   ↓

Top-k Relevant Chunks

   ↓

Prompt Template

   ↓

Groq LLM (Llama 3.1)

   ↓

Answer + Sources

## Project Structure

```text
.
|-- app/
|   `-- api.py                  # FastAPI app
|-- data/
|   |-- raw/ai_policy/          # Source PDFs
|   `-- vector_store/           # Generated Chroma database
|-- notebooks/
|   `-- rag_notebook.ipynb      # Original learning notebook
|-- src/
|   `-- rag_app/
|       |-- config.py           # Paths, model names, env vars
|       |-- document_loader.py  # PDF loading and chunking
|       |-- rag_chain.py        # Retrieval and answer generation
|       `-- vector_store.py     # Embeddings and Chroma setup
|-- ui/
|   `-- streamlit_app.py        # Streamlit UI
|-- main.py                     # CLI app interface
|-- Dockerfile
|-- docker-compose.yml
`-- pyproject.toml
```

## Requirements

- Python 3.11
- `uv`
- Groq API key

The main dependencies are managed in `pyproject.toml`.

## Environment Variables

Create a local `.env` file from the example:

```powershell
Copy-Item .env.example .env
```

Then add your Groq API key:

```env
GROQ_API_KEY=your_groq_api_key_here
APP_MODE="direct"
API_URL=http://127.0.0.1:8000/query
```

Do not commit `.env`.

## Installation

Install dependencies with `uv`:

```powershell
uv sync
```

If needed, activate the virtual environment:

```powershell
.venv\Scripts\Activate
```

## Data Setup

Place source PDFs in:

```text
data/raw/ai_policy/
```

The current app expects these filenames for source filtering:

```text
eu_ai_act.pdf
gdpr.pdf
nist_ai_rmf.pdf
```

The Chroma vector store is generated under:

```text
data/vector_store/
```

This directory is generated data and should not be committed.

## Build the Vector Store

Use the loader and vector-store helpers to create the local Chroma database:

```powershell
uv run python -c "from rag_app.document_loader import load_and_split_documents; from rag_app.vector_store import create_vector_store; create_vector_store(load_and_split_documents())"
```

Run this again whenever the source PDFs change.

## Run the Streamlit App (Direct mode)

Run the UI directly:

```powershell
$env:APP_MODE="direct"
uv run streamlit run ui/streamlit_app.py --server.fileWatcherType none
```

By default, the UI uses `APP_MODE=direct`, which calls the RAG chain directly from Streamlit.

Open:

```text
http://localhost:8501
```

## Run the FastAPI Backend only

Start the API:

```powershell
uv run uvicorn app.api:app --reload
```

Health check:

```text
http://127.0.0.1:8000/docs
```

Example request body:

```json
{
  "question": "What are high-risk AI systems under the EU AI Act?",
  "k": 6,
  "source_filter": "eu_ai_act.pdf"
}
```

`source_filter` is optional. If omitted, the app tries to infer the best source from the question.

## Run the API mode: Streamlit + FastAPI

Terminal 1:

```powershell
uv run uvicorn app.api:app --reload
```

Terminal 2:

```powershell
$env:APP_MODE="api"
$env:API_URL="http://127.0.0.1:8000/query"
uv run streamlit run ui/streamlit_app.py
```

Open:

```text
http://localhost:8501
```

## Run with Docker: Streamlit only

Your current Dockerfile runs Streamlit on port 10000.

Build the image:

```powershell
docker build -t rag-ai-policy-assistant .
```

Run the Streamlit app:

```powershell
docker run --env-file .env -p 10000:10000 rag-ai-policy-assistant
```

Open:

```text
http://localhost:10000
```


## Run with Docker Compose: API + Streamlit

Build and start both the API and UI:

```powershell
docker compose up --build
```

Open:

http://localhost:8501

FastAPI docs:

http://localhost:8000/docs

Stop with:

Ctrl + C

or:

docker compose down


## CLI mode

You can also ask questions from the terminal:

```powershell
uv run python main.py
```

## Deployment

The repository includes `render.yaml` for Docker-based deployment on Render.

Required environment variable:

```text
GROQ_API_KEY
```

### Deployment Notes

This project is designed primarily for **local execution**.

Cloud deployment (e.g., Render free tier) may fail due to:
- high memory usage from embedding + LLM dependencies

For production deployment, consider:
- lightweight embedding models
- external vector DB
- managed inference APIs

## Learning Background

This project started as a hands-on RAG learning notebook and has been extended into a small application with a UI, API, Docker setup, and reusable source package.

Learning references:

- Krish Naik RAG playlist: https://youtube.com/playlist?list=PLZoTAELRMXVM8Pf4U67L4UuDRgV4TNX9D
- RAG Tutorials repository: https://github.com/krishnaik06/RAG-Tutorials/tree/main
