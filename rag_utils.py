import re
import math
from collections import Counter


def split_pages_into_chunks(pages):
    chunks = []
    chunk_id = 0

    for page in pages:
        text = page["text"]
        page_num = page["page"]

        split = text.split("\n")

        for s in split:
            if len(s.strip()) < 10:
                continue

            chunks.append({
                "chunk_id": chunk_id,
                "page": page_num,
                "content": s.strip()
            })
            chunk_id += 1

    return chunks


def tokenize(text):
    return re.findall(r"\w+", text.lower())


def build_vector_store(chunks):
    docs_tokens = []
    df = Counter()

    for c in chunks:
        tokens = set(tokenize(c["content"]))
        docs_tokens.append(tokens)

        for t in tokens:
            df[t] += 1

    return {
        "chunks": chunks,
        "tokens": docs_tokens,
        "df": df,
        "n": len(chunks)
    }


def score(query_tokens, doc_tokens, df, n):
    score = 0
    for t in query_tokens:
        if t in doc_tokens:
            score += math.log((n + 1) / (df[t] + 1))
    return score


def retrieve_relevant_chunks(store, query, k=3):
    q_tokens = set(tokenize(query))
    results = []

    for i, doc_tokens in enumerate(store["tokens"]):
        c = store["chunks"][i]

        s = score(q_tokens, doc_tokens, store["df"], store["n"])

        results.append({
            "chunk_id": c["chunk_id"],
            "page": c["page"],
            "content": c["content"],
            "score": s
        })

    return sorted(results, key=lambda x: x["score"], reverse=True)[:k]