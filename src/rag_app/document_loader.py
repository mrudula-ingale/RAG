from pathlib import Path
from typing import List

from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from rag_app.config import PDF_DIR, CHUNK_SIZE, CHUNK_OVERLAP

def load_pdf_files(pdf_dir: Path = PDF_DIR) -> List[Document]:
    """
    Load all PDF files from the given directory.

    Returns:
        A list of LangChain Document objects.
    """
    if not pdf_dir.exists():
        raise FileNotFoundError(f"PDF directory not found: {pdf_dir}")

    pdf_files = list(pdf_dir.glob("*.pdf"))

    if not pdf_files:
        raise FileNotFoundError(f"No PDF files found in: {pdf_dir}")

    print(f"Found {len(pdf_files)} PDF files to process")
    documents = []

    for pdf_file in pdf_files:
        print(f"\nProcessing: {pdf_file.name}")

        loader = PyPDFLoader(str(pdf_file))
        loaded_docs = loader.load()
        print(f"  Loaded {len(loaded_docs)} pages")

        for doc in loaded_docs:
            doc.metadata["source"] = pdf_file.name

        documents.extend(loaded_docs)

    return documents


def split_documents(documents: List[Document]) -> List[Document]:
    """
    Split loaded documents into smaller text chunks.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )

    chunks = text_splitter.split_documents(documents)
    return chunks


def load_and_split_documents(pdf_dir: Path = PDF_DIR) -> List[Document]:
    """
    Load PDFs and split them into chunks.
    """
    documents = load_pdf_files(pdf_dir)
    chunks = split_documents(documents)
    return chunks