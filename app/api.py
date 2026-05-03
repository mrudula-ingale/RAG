from fastapi import FastAPI
from pydantic import BaseModel

from rag_app.rag_chain import ask_rag

# creates the API app.
app = FastAPI(
    title="RAG Assistant API",
    description="A Retrieval-Augmented Generation API for answering questions from documents.",
    version="0.1.0",
)

# defines what input the API expects.
class QuestionRequest(BaseModel):
    question: str
    k: int = 4
    source_filter: str | None = None

# creates a simple homepage route.
@app.get("/")
def root():
    return {"message": "RAG Assistant API is running"}

# creates the main RAG endpoint.
@app.post("/query")
def ask_question(request: QuestionRequest):
    #response = ask_rag(question=request.question, k=request.k)
    response = ask_rag(
        question=request.question,
        k=request.k,
        source_filter=request.source_filter,
    )
    return response