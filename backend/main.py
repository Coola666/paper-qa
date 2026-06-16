from fastapi import FastAPI
from pydantic import BaseModel

from llm_client import LLMClient
from rag_engine import RAGEngine
from utils import DEEPSEEK_API_KEY

app = FastAPI()

llm = LLMClient(DEEPSEEK_API_KEY)
rag = RAGEngine()


# =========================
# Models
# =========================
class BuildRequest(BaseModel):
    docs: list


class QueryRequest(BaseModel):
    question: str
    context: str = ""


# =========================
# BUILD RAG INDEX
# =========================
@app.post("/build")
def build(req: BuildRequest):

    clean_docs = []

    for i, d in enumerate(req.docs):
        clean_docs.append({
            "content": d.get("content", d.get("text", "")),
            "page": d.get("page", -1),
            "chunk_id": i
        })

    rag.build(clean_docs)

    return {"status": "ok", "docs": len(clean_docs)}


# =========================
# ASK
# =========================
@app.post("/ask")
def ask(req: QueryRequest):

    docs = rag.search(req.question, k=3)

    context = "\n\n".join([d["content"] for d in docs])

    answer = llm.chat(context + "\n\n问题：" + req.question)

    return {
        "answer": answer,
        "sources": docs
    }


# =========================
# SOTA
# =========================
@app.post("/sota")
def sota(req: QueryRequest):

    docs = rag.search("实验结果 accuracy performance table SOTA", k=5)

    context = "\n\n".join([d["content"] for d in docs])

    result = llm.chat(f"""
你是科研分析助手，请分析实验结果：

1. 找出 SOTA 模型
2. 找出 baseline
3. 对比提升
4. 必须中文输出

内容：
{context}
""")

    return {"sota": result}