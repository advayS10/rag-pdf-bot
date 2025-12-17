from rag_pipeline import answer_question

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
What this does:

A simple CLI loop that asks user for a question, calls answer_question and prints the answer.
'''