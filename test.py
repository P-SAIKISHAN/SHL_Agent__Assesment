import pickle

with open("vectorstore/faiss_index/documents.pkl", "rb") as f:
    docs = pickle.load(f)

print(docs[0])