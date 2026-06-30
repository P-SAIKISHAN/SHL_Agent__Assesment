import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load embedding model
model = SentenceTransformer("BAAI/bge-small-en-v1.5")

# Load FAISS index
index = faiss.read_index("vectorstore/faiss_index/index.faiss")

# Load metadata
with open("vectorstore/faiss_index/documents.pkl", "rb") as f:
    documents = pickle.load(f)


def search(query: str, top_k: int = 5):
    """
    Semantic search over SHL assessments.
    """

    query_embedding = model.encode(
        [query],
        normalize_embeddings=True,
        convert_to_numpy=True,
    )

    scores, indices = index.search(
        np.array(query_embedding),
        top_k
    )

    results = []

    for score, idx in zip(scores[0], indices[0]):
        doc = documents[idx]

        results.append({
            "score": float(score),
            "id": doc.get("id", ""),
            "name": doc.get("name", ""),
            "url": doc.get("url", ""),
            "description": doc.get("description", ""),
            "job_levels": doc.get("job_levels", []),
            "categories": doc.get("categories", []),
            "languages": doc.get("languages", []),
            "duration": doc.get("duration", ""),
            "remote": doc.get("remote", ""),
            "adaptive": doc.get("adaptive", ""),
            "text": doc.get("text", "")
        })

    return results


if __name__ == "__main__":

    query = input("Enter Query: ")

    results = search(query)

    print("\nTop Matches\n")

    for i, item in enumerate(results, start=1):

        print("=" * 70)
        print(f"Rank       : {i}")
        print(f"Score      : {item['score']:.4f}")
        print(f"Name       : {item['name']}")
        print(f"URL        : {item['url']}")
        print(f"Duration   : {item['duration']}")
        print(f"Remote     : {item['remote']}")
        print(f"Adaptive   : {item['adaptive']}")
        print(f"Job Levels : {', '.join(item['job_levels'])}")
        print(f"Categories : {', '.join(item['categories'])}")
        print(f"\nDescription:\n{item['description']}")