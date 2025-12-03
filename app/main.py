from transformers import pipeline
qa = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")
print(qa({
    'question': 'What is AI?',
    'context': 'Artificial intelligence is the simulation of human intelligence by machines.'
}))