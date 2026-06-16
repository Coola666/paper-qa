import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer


# =========================
# Step 1: Split into chunks
# =========================
def split_pages_into_chunks(pages, chunk_size=500):
    chunks = []

    chunk_id = 0

    for page in pages:
        text = page["content"]
        page_num = page["page"]

        words = text.split()

        for i in range(0, len(words), chunk_size):
            chunk_text = " ".join(words[i:i + chunk_size])

            chunks.append({
                "content": chunk_text,
                "page": page_num,
                "chunk_id": chunk_id
            })

            chunk_id += 1

    return chunks


# =========================
# Step 2: Build Vector Store
# =========================
class VectorStore:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.matrix = None
        self.chunks = []

    def build(self, chunks):
        self.chunks = chunks
        texts = [c["content"] for c in chunks]
        self.matrix = self.vectorizer.fit_transform(texts)

    def search(self, query, k=3):
        q_vec = self.vectorizer.transform([query])
        scores = np.dot(self.matrix, q_vec.T).toarray().flatten()

        top_k = np.argsort(scores)[-k:][::-1]

        results = []
        for i in top_k:
            c = self.chunks[i]

            results.append({
                "content": c["content"],
                "page": c["page"],
                "chunk_id": c["chunk_id"],
                "score": float(scores[i])
            })

        return results


def build_vector_store(chunks):
    store = VectorStore()
    store.build(chunks)
    return store


def retrieve_relevant_chunks(vector_store, query, k=3):
    return vector_store.search(query, k)