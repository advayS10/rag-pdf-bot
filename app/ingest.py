import os
from pypdf import PdfReader
from chromadb import PersistentClient
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

# Step 1: Load PDF

def load_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""

    for page in reader.pages:

        content = page.extract_text()
        if content:
            text += content + "\n\n"
        
    return text
    
# Step 2: Text Chunking

def chunk_text(text, chunk_size=350):
    words = text.split()
    chunks = []
    current_chunk = []

    for word in words:
        current_chunk.append(word)
        if len(current_chunk) >= chunk_size:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
    
    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks

# Step 3: Create Embeddings + Store in ChromaDB

def store_embeddings(chunks):
    model = SentenceTransformer("all-MiniLM-L6-v2")

    client = PersistentClient(path="../chroma_db")

    collection = client.get_or_create_collection("pdf_chunks")

    # clear old embeddings
    existing = collection.get()
    if existing["ids"]:
        collection.delete(ids=existing["ids"])


    embeddings = model.encode(chunks).tolist()
    ids = [f"chunk_{i}" for i in range(len(chunks))]

    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=ids
    )

    print(f"Stored {len(chunks)} chunks in ChromaDB!")

if __name__ == "__main__":

    pdf_path = "../data/sample.pdf"

    if not os.path.exists(pdf_path):
        print("PDF not found! Put sample.pdf in this folder.")
        exit()

    print("Loading PDF...")
    text = load_pdf(pdf_path)

    print("Splitting into chunks...")
    chunks = chunk_text(text)

    print("Creating embeddings and saving to Chroma...")
    store_embeddings(chunks)

    print("\nDone! You now have a Vector DB memory for your PDF.")
