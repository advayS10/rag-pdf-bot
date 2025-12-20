from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import QuestionRequest, AnswerResponse
from app.rag_pipeline import answer_question
from app.ingest import load_pdf, chunk_text, store_embeddings
import os
import shutil

app = FastAPI(title="RAG PDF BOT") #This initializes a FastAPI application. FastAPI automatically handles request validation, async support, and API documentation using OpenAPI.

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploaded_pdfs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# A health-check endpoint is used to verify if the service is running and reachable, often used by monitoring tools or load balancers.
@app.get("/") 
def health_check():
    return {'status': 'RAG PDF BOT is running'}


# FastAPI provides UploadFile for handling large files efficiently using streaming instead of loading everything into memory.
# File uploads are I/O-bound operations, so using async improves performance by allowing the server to handle other requests while waiting for file operations
@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    text = load_pdf(file_path)
    chunks = chunk_text(text)

    store_embeddings(chunks)

    return {
        "message": "PDF uploaded and processed successfully",
        "chunk_stored": len(chunks)
    }


# Pydantic schemas ensure type safety, request validation, and clear API contracts between frontend and backend.
@app.post("/ask", response_model=AnswerResponse)
def ask_question(payload: QuestionRequest):
    answer = answer_question(payload.question)
    return AnswerResponse(answer=answer)




'''
def run_cli():
    print("RAG PDF BOT - console test")
    print("Type 'exit' to quit.\n")

    while True:
        user_q = input("Question: ").strip()
        if not user_q:
            continue
        if user_q.lower() == "exit":
            break

        print("\n[1] Searching DB and generating answer (this may take a few seconds)...\n")
        try:
            ans = answer_question(user_q, top_k=3)
            print("\n--- ANSWER ---\n")
            print(ans)
            print("\n----------------\n")
        except Exception as e:
            print("Error during answering:", e)
            print("If this is an embedding-function conflict, delete ./app/chroma_db and re-run ingest.")
            break

if __name__ == "__main__":
    run_cli()
'''
'''
What this does:

A simple CLI loop that asks user for a question, calls answer_question and prints the answer.
'''