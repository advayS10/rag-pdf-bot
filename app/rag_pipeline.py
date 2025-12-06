from chromadb.utils import embedding_functions
from transformers import pipeline
from chromadb import PersistentClient

# Load embedding function again for search
embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

# Reload existing chroma db
def load_db():
    client = PersistentClient(path="chroma_db")
    return client.get_collection("pdf_chunks")

# Search relevant chunks
def get_relevant_chunks(question, top_k=3):
    collection = load_db()
    results = collection.query(
        query_texts=[question],
        n_results=top_k
    )
    return results["documents"][0]

# Ask LLM with context
def answer_question(question):
    chunks = get_relevant_chunks(question)

    context = "\n\n".join(chunks)

    prompt = f"Use ONLY the context below to answer.\n\nContext:{context}\n\nQuestion: {question}\nAnswer:"

    llm = pipeline("text-generation", model="distilbert/distilgpt2") # Free HuggingFace model

    response = llm(prompt, max_length=300, do_sample=True)[0]["generated_text"]
    return response


if __name__ == "__main__":

    print("Ask a question about your PDF:")
    user_q = input("> ")
    ans = answer_question(user_q)
    print("\n Answer:\n", ans)