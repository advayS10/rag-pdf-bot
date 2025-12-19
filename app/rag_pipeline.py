from app import chroma_db
from typing import List, Dict, Any
from app.embeddings import embed_text
from chromadb.utils import embedding_functions
from transformers import pipeline
from chromadb import PersistentClient
import os 

CHROMA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "chroma_db"))
COLLECTION_NAME = "pdf_chunks"

llm = pipeline(
    "text-generation",
    model="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    device=-1
)

# DB Helper
def load_collection():
    '''
    Load existing collection. Raises RuntimeError if collection not found.
    '''
    client = PersistentClient(path=CHROMA_DIR)
    try:
        collection = client.get_collection(name=COLLECTION_NAME)
    except Exception as e:
        '''
        get_collection raises if not exists in some chroma builds
        try get_or_create but without embedding_function to avoid conflicts
        '''
        try:
            collection = client.get_or_create_collection(name=COLLECTION_NAME)
        except Exception as e2:
            raise RuntimeError(
                f"Could not load collection '{COLLECTION_NAME}'."
                f"Make sure you ran ingest and the collection exists. Error: {e2}"
            )
    return collection 


# Search relevant chunks
def get_relevant_chunks(question: str, top_k: int = 3) -> List[str]:
    '''
    Returns a list of the top_k most relevant document chunks (strings) from the chromaDB for the given question
    '''
    collection = load_collection()

    print("Total chunks stored:", collection.count())

    q_emb = embed_text(question)
    results = collection.query(
        query_embeddings=[q_emb],
        n_results=top_k
    )

    docs_for_query = results.get("documents", [[]])[0]
    # print("docs_for_query", docs_for_query)
    return docs_for_query

# Ask LLM with context
def answer_question(question:str, top_k:int=3):
    chunks = get_relevant_chunks(question, top_k=top_k)
    if not chunks:
        return "No relevant information found in document."

    # Build context (join top chunks). Limit size to avoid huge prompts.
    context = "\n\n".join(chunks)
    context = context[:1500]

    # Prompt template: strictly instruct the model to use ONLY the context.
    prompt = f"""
        You are a helpful AI assistant. Your job is to answer the user's question 
        using ONLY the information provided in the CONTEXT below.

        STRICT RULES:
        1. If the answer is not clearly stated in the context, reply exactly:
        "I don't know — the document does not contain this information."
        2. Do NOT add extra facts, assumptions, or hallucinations.
        3. Keep the answer short, clear, and factual.

        CONTEXT:
        \"\"\"{context}\"\"\"

        QUESTION:
        {question}

        FINAL ANSWER:
        """
    # Use a small local model for demo. You can swap this with a better HF model or an API.
    

    output = llm(prompt, max_new_tokens=256, truncation=True, do_sample=False, temperature=0.1)[0]["generated_text"]
    
    # print("Output", output)
    # print("======== Before Answer ========")
    # Remove the prompt prefix from the returned text if present:
    answer = output.split("ANSWER:")[-1].strip()

    # Simple cleanup: If model invented irrelevant text, keep first 300 chars (still demo)
    return answer


if __name__ == "__main__":
    q = input("Ask a question about the PDF (or 'exit'): ").strip()
    if q.lower() != "exit":
        print("\nRetrieving relevant chunks...")
        chunks = get_relevant_chunks(q, top_k=3)
        print(f"\nTop {len(chunks)} chunks:")
        for i, c in enumerate(chunks, 1):
            print(f"\n--- chunk {i} ---\n{c[:1000]}")  # print only first 1k chars per chunk

        print("\nGenerating answer...\n")
        ans = answer_question(q, top_k=3)
        print("\n--- ANSWER ---\n")
        print(ans)

'''
What this does:

get_relevant_chunks(question) manually embeds the question (using embeddings.embed_text) and queries ChromaDB with query_embeddings to avoid any embedding-function conflicts.

answer_question(question) builds a strict prompt instructing the model to only use context, calls a local HF model (distilgpt2) to generate text and extracts the generated portion.

Note: distilgpt2 is small demo model. For better answers move to a better LLM or Hugging Face Inference API. But this file will run locally.
'''