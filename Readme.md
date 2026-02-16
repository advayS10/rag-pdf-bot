# 📄 DocQuery — Ask Questions From Your PDF
DocQuery is a Retrieval-Augmented Generation (RAG) based system that allows users to upload a PDF file and ask questions from it.
The system reads the PDF, creates embeddings, stores them in a vector database, and uses an LLM to generate answers only from the document content.

## 🚀 Features
- Upload any PDF file
- Automatic text chunking & embedding generation
- Stores document embeddings in ChromaDB
- Ask questions and get accurate answers from the PDF
- FastAPI backend with simple HTML frontend

## 🛠 Tech Stack
- Backend: Python, FastAPI
- Embeddings: SentenceTransformers
- Vector DB: ChromaDB
- LLM: HuggingFace Transformers
- Frontend: HTML, CSS, JavaScript

## RAG pipeline
```
PDF → Chunk Text → Embeddings → Vector DB
                                 ↑
                                 |
User Question → Embedding → Similarity Search → Relevant Chunks → LLM
```

## 📂 Project Structure
```
rag-pdf-bot/
 ├─ app/
 │   ├─ main.py
 │   ├─ rag_pipeline.py
 │   ├─ embeddings.py
 │   └─ schemas.py
 ├─ frontend/
 │   ├─ index.html
 │   ├─ script.js
 │   └─ style.css
 ├─ chroma_db/
 └─ data/
```

## ▶ How to Run
1️⃣ Create Virtual Environment
```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```
2️⃣ Start FastAPI Server
```powershell
uvicorn app.main:app --reload
```

Server runs at:
```
http://127.0.0.1:8000
```

## 🌐 Use the App
Open browser:
```
http://127.0.0.1:8000/docs
```
or open:
```
frontend/index.html
```

Flow:
1. Upload PDF
2. Ask a question
3. Get answer from your document

## 🎯 Example

Upload a PDF and ask:
```
What is Artificial Intelligence?
```

DocQuery will return the answer using only the uploaded document.

## 📌 Why DocQuery?
This project demonstrates real-world GenAI concepts such as:
- Vector search
- Retrieval-Augmented Generation
- Backend API design
- Working with large documents
