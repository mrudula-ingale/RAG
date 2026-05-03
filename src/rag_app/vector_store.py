from typing import List

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings

from rag_app.config import EMBEDDING_MODEL, VECTOR_STORE_DIR


def get_embedding_model() -> HuggingFaceEmbeddings:
    """
    Create the embedding model used to convert text chunks into vectors.
    """
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)


def create_vector_store(chunks: List[Document]) -> Chroma:
    """
    Create and persist a Chroma vector store from document chunks.
    """
    embedding_model = get_embedding_model()

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=str(VECTOR_STORE_DIR),
        collection_name="rag_documents",
    )

    return vector_store


def load_vector_store() -> Chroma:
    """
    Load an existing Chroma vector store.
    """
    embedding_model = get_embedding_model()

    vector_store = Chroma(
        persist_directory=str(VECTOR_STORE_DIR),
        embedding_function=embedding_model,
        collection_name="rag_documents",
    )

    return vector_store


# def get_retriever(k: int = 4):
#     """
#     Load vector store and return a retriever.
#     """
#     vector_store = load_vector_store()
#     return vector_store.as_retriever(search_kwargs={"k": k})

def get_retriever(k: int = 4, source_filter: str | None = None):
    vector_store = load_vector_store()

    search_kwargs = {"k": k}

    if source_filter:
        search_kwargs["filter"] = {"source": source_filter}

    return vector_store.as_retriever(search_kwargs=search_kwargs)