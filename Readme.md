🧠 DocQuery – RAG Based PDF Chatbot

DocQuery is a Retrieval-Augmented Generation (RAG) based chatbot that allows users to upload PDF documents and ask natural language questions about their content.

The system extracts text from PDFs, splits it into chunks, generates embeddings, stores them in a vector database, and retrieves the most relevant context to generate accurate answers using an LLM.

🔹 Key Features

PDF upload and text extraction

Embedding generation and vector storage

Semantic search using vector similarity

Context-aware answers using RAG

🔹 Tech Stack

Backend: Python (Fast Api)

LLM: TinyLlama

Vector DB: Chroma

Embeddings + Retrieval + Generation (RAG)

🔹 High-Level Flow

PDF Upload → Text Chunking → Embeddings → Vector DB → User Query → Context Retrieval → LLM Response