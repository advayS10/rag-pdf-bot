from sentence_transformers import SentenceTransformer
from typing import List

_MODEL_NAME = "all-MiniLM-L6-v2"
_model = None

def get_embedding_mode():
    global _model
    if _model is None:
        _model = SentenceTransformer(_MODEL_NAME)
    return _model

def embed_texts(texts: List[str]):
    
    model = get_embedding_mode()
    embeds = model.encode(texts)

    return embeds.tolist()

def embed_text(text: str):
    return embed_texts([text])[0]

'''
What it does:
- Lazily loads the SentenceTransformer model and exposes embed_text / embed_texts to create embeddings for queries or documents

'''