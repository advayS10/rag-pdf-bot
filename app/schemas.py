from pydantic import BaseModel

class QuestionRequest(BaseModel):
    question: str

class AnswerResponse(BaseModel):
    answer: str

'''
Why schemas.py is used (simple words)

FastAPI uses Pydantic models to:

1. Validate incoming request data

2. Convert JSON → Python objects

3. Control what data is sent in responses

4. Auto-generate API docs (Swagger)

We usually put these Pydantic models in schemas.py.
'''