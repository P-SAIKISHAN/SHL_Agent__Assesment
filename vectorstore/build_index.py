import json
from pathlib import Path
import pickle

import faiss
from sentence_transformers import SentenceTransformer

DATA_DIR = Path("data")
INDEX_DIR = Path("vectorstore/faiss_index")

INDEX_DIR.mkdir(parents=True, exist_ok=True)

# Load documents
with open(DATA_DIR / "search_documents.json", "r", encoding="utf-8") as f:
    docs = json.load(f)

print(f"Loaded {len(docs)} documents")

# Load embedding model
print("Loading embedding model...")
model = SentenceTransformer("BAAI/bge-small-en-v1.5")

texts = [doc["text"] for doc in docs]

print("Generating embeddings...")
embeddings = model.encode(
    texts,
    show_progress_bar=True,
    convert_to_numpy=True,
    normalize_embeddings=True
)

dimension = embeddings.shape[1]

print(f"Embedding Dimension: {dimension}")

# Build FAISS index
index = faiss.IndexFlatIP(dimension)
index.add(embeddings)

# Save index
faiss.write_index(index, str(INDEX_DIR / "index.faiss"))

# Save metadata
with open(INDEX_DIR / "documents.pkl", "wb") as f:
    pickle.dump(docs, f)

print("=" * 50)
print("FAISS Index Created Successfully")
print(f"Total Documents : {index.ntotal}")
print("=" * 50)