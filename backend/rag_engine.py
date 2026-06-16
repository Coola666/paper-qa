import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer


class RAGEngine:

    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.matrix = None
        self.docs = []
        self.is_fitted = False   # ⭐ 新增保护

    # =========================
    # BUILD
    # =========================
    def build(self, docs):

        # ✔ 统一 content
        self.docs = [
            {
                "content": d.get("content", d.get("text", "")),
                "page": d.get("page", -1),
                "chunk_id": d.get("chunk_id", 0)
            }
            for d in docs
        ]

        texts = [d["content"] for d in self.docs]

        # ❗防止空数据
        if len(texts) == 0:
            raise ValueError("RAG build失败：没有文本")

        self.matrix = self.vectorizer.fit_transform(texts)
        self.is_fitted = True   # ⭐关键
        print("RAG built successfully")

    # =========================
    # SEARCH
    # =========================
    def search(self, query, k=3):

        # ❗关键保护
        if not self.is_fitted:
            raise ValueError("RAG未初始化，请先调用 /build")

        q_vec = self.vectorizer.transform([query])
        scores = np.dot(self.matrix, q_vec.T).toarray().flatten()

        top_k = np.argsort(scores)[-k:][::-1]

        results = []

        for i in top_k:
            doc = self.docs[i]

            results.append({
                "content": doc["content"],
                "page": doc["page"],
                "chunk_id": doc["chunk_id"],
                "score": float(scores[i])
            })

        return results