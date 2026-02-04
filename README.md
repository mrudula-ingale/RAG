# 📄 Retrieval-Augmented Generation (RAG) – Mini Project

This repository contains my **first mini-project on Retrieval-Augmented Generation (RAG)**, implemented as a Python notebook.  
The goal of this project was to **understand the end-to-end RAG pipeline** and apply it to a real, personal dataset.

In this project, I use **my Master’s thesis documents** as the knowledge base and build a RAG system that can answer natural-language queries grounded in those documents.

---

## 🚀 What this project does

- Loads and processes documents from my **thesis files**
- Splits documents into chunks and generates embeddings
- Stores embeddings in a vector store
- Retrieves relevant chunks for a user query
- Uses an LLM to generate answers **based only on retrieved context**
- Implements multiple RAG variants:
  - A simple RAG pipeline
  - An advanced RAG pipeline with metadata, confidence, and sources
  - A class-based pipeline with history, citations, and optional summarization

---

## 🧠 Motivation

I wanted to:
- Learn **RAG fundamentals** hands-on
- Understand how retrieval quality affects LLM answers
- Apply RAG to **my own academic work**, not a toy dataset

This notebook is intentionally kept simple and educational rather than production-ready.

---

## 🧩 RAG Variants Implemented

### 1. `rag_simple`
- Minimal RAG implementation
- Retrieves top-k chunks
- Builds a single prompt
- Returns only the generated answer

### 2. `rag_advanced`
- Adds:
  - similarity score filtering
  - source metadata (file, page, preview)
  - confidence estimation
- Returns a structured dictionary instead of plain text

### 3. `AdvancedRAGPipeline` (class)
- Stateful RAG pipeline
- Supports:
  - query history
  - inline citations
  - optional answer summarization
  - simulated streaming output
- Designed as a reusable component for future extensions

---

## 📂 Data Used

- **My Master’s thesis documents**
- Files were used purely for learning and experimentation
- The RAG system answers questions only using content retrieved from these documents

---

## 📚 Learning Resources & References

This project is heavily inspired by and built while learning from the following excellent resources:

### 📺 YouTube Playlist
I learned the core RAG concepts from this playlist by **Krish Naik**:

https://youtube.com/playlist?list=PLZoTAELRMXVM8Pf4U67L4UuDRgV4TNX9D&si=86SdH91x88Bpp8or

### 💻 Reference GitHub Repository
I also referred to the following GitHub repository for understanding implementation patterns:

https://github.com/krishnaik06/RAG-Tutorials/tree/main

While the concepts and structure are inspired by these resources, this notebook uses **my own dataset**.
---

## 🛠️ Tech Stack

- Python
- LangChain
- Vector store for embeddings
- Groq LLM API
- Jupyter Notebook

---

## ⚠️ Disclaimer

This is a **learning project**, not a production system.

- Prompts, thresholds, and confidence metrics are experimental
- Streaming is simulated
- Security, scaling, and optimization are out of scope

---

## 🙌 Acknowledgements

Thanks to **Krish Naik** for the clear explanations and practical RAG tutorials that made this project possible.
