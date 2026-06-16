from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI

from utils import DEEPSEEK_API_KEY
from rag_utils import retrieve_relevant_chunks, build_vector_store

app = FastAPI()

client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com/v1"
)

# =========================
# Request Schema
# =========================
class QuestionRequest(BaseModel):
    question: str
    context: str


# =========================
# QA API
# =========================
@app.post("/ask")
def ask(req: QuestionRequest):

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {
                "role": "system",
                "content": "你是科研论文助手，只用中文回答"
            },
            {
                "role": "user",
                "content": req.context + "\n\n问题：" + req.question
            }
        ]
    )

    return {
        "answer": response.choices[0].message.content
    }