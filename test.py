from vectorstore.retriever import search
from app.llm import generate_response

query = "Java Developer"

results = search(query, top_k=5)

reply = generate_response(query, results)

print("\n===== LLM RESPONSE =====\n")
print(reply)