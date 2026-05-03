from typing import Dict, Any

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq

from rag_app.config import GROQ_API_KEY, LLM_MODEL
from rag_app.vector_store import get_retriever


RAG_PROMPT = """
You are a helpful AI assistant. 

Answer the question using only the provided context. Answer clearly in bullet points when listing multiple items.

Rules:
- Be concise and clear
- Do not repeat the question
- Do not include citations like [1], [2]
- If the answer is not in the context, say:
  "I could not find this information in the provided documents."

Context:
{context}

Question:
{question}

Answer:
"""


def format_docs(docs):
    return "\n\n".join(
        f"Source: {doc.metadata.get('source', 'unknown')}\n"
        f"Page: {doc.metadata.get('page', 'unknown')}\n"
        f"Content: {doc.page_content}"
        for doc in docs
    )

def detect_source_filter(question: str) -> str | None:
    """
    Detect which document should be searched based on the user's question.
    """
    question_lower = question.lower()

    if any(term in question_lower for term in ["eu ai act", "high-risk", "high risk", "ai act"]):
        return "eu_ai_act.pdf"

    if any(term in question_lower for term in ["gdpr", "data subject", "personal data", "data protection"]):
        return "gdpr.pdf"

    if any(term in question_lower for term in ["nist", "risk management framework", "ai rmf"]):
        return "nist_ai_rmf.pdf"

    return None

def ask_rag(question: str, k: int = 4, source_filter: str | None = None) -> Dict[str, Any]:
#def ask_rag(question: str, k: int = 4) -> Dict[str, Any]:
    """
    Answer a question using retrieved document chunks and Groq LLM.
    """
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is missing. Please add it to your .env file.")
    
    if source_filter is None:
        source_filter = detect_source_filter(question)

    retriever = retriever = get_retriever(k=k, source_filter=source_filter) #get_retriever(k=k)
    docs = retriever.invoke(question)

    context = format_docs(docs)

    prompt = ChatPromptTemplate.from_template(RAG_PROMPT)

    llm = ChatGroq(
        model=LLM_MODEL,
        api_key=GROQ_API_KEY,
        temperature=0,
    )

    chain = prompt | llm | StrOutputParser()

    raw_answer  = chain.invoke(
        {
            "context": context,
            "question": question,
        }
    )
    answer = raw_answer.strip().replace('\\"', '"')
    sources = [
        {
            "source": doc.metadata.get("source", "unknown"),
            "page": doc.metadata.get("page", "unknown"),
            "preview": doc.page_content[:200],
        }
        for doc in docs
    ]

    return {
        "question": question,
        "answer": answer,
        "sources": sources,
    }