from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from schemas import QuestionRequest, AnswerResponse
from rag_pipeline import answer_question
from ingest import load_pdf, chunk_text, store_embeddings
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
    """Save the uploaded PDF, run ingestion and return stats.

    This handler now performs basic validation and handles errors so
    that the caller receives an appropriate HTTP status instead of a
    raw traceback.
    """

    # server‑side validation: content type and file extension
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Filename must end with .pdf")

    # check file size without loading entire file into memory
    file.file.seek(0, os.SEEK_END)
    size = file.file.tell()
    file.file.seek(0)
    MAX_SIZE = 50 * 1024 * 1024  # 50 MB
    if size > MAX_SIZE:
        raise HTTPException(status_code=413, detail="File too large. Max 50MB allowed.")

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        text = load_pdf(file_path)
        chunks = chunk_text(text)

        store_embeddings(chunks)

    except Exception as e:
        # log the exception for debugging (could use logging module later)
        print("Error during upload/ingest:", e)
        raise HTTPException(status_code=500, detail="Failed to process PDF.")

    return {
        "message": "PDF uploaded and processed successfully",
        "chunk_stored": len(chunks)
    }


# Pydantic schemas ensure type safety, request validation, and clear API contracts between frontend and backend.
@app.post("/ask", response_model=AnswerResponse)
def ask_question(payload: QuestionRequest):
    """Return an answer for the supplied question.

    Wrap the call to the RAG pipeline so that failures are translated
    into a 500 response rather than crashing the server.
    """
    try:
        answer = answer_question(payload.question)
    except Exception as e:
        print("Error during question answering:", e)
        raise HTTPException(status_code=500, detail="Error generating answer.")

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