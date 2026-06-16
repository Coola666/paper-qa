import streamlit as st
import tempfile
import pandas as pd
import matplotlib.pyplot as plt
import requests

from pdf_utils import extract_pages_from_pdf
from rag_utils import split_pages_into_chunks, build_vector_store, retrieve_relevant_chunks
from table_utils import extract_tables_from_llm, analyze_sota_vs_baseline
from report_utils import extract_sections_from_llm, generate_markdown_report


# =========================
# CONFIG
# =========================
FASTAPI_URL = "paper-qa-production.up.railway.app"

st.set_page_config(layout="wide")
st.title("📄 Research Paper AI Agent (FastAPI Version)")


# =========================
# SESSION STATE
# =========================
if "answer" not in st.session_state:
    st.session_state.answer = ""

if "analysis_text" not in st.session_state:
    st.session_state.analysis_text = ""

if "sota_analysis" not in st.session_state:
    st.session_state.sota_analysis = ""

if "table_summary" not in st.session_state:
    st.session_state.table_summary = ""


# =========================
# PDF UPLOAD
# =========================
uploaded_pdf = st.file_uploader("Upload Paper PDF", type=["pdf"])

vector_store = None
paper_context = ""
tables_data = []

if uploaded_pdf:

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_pdf.read())
        pdf_path = tmp.name

    pages = extract_pages_from_pdf(pdf_path)

    # ✅ FIX 1：兼容 text / content
    paper_context = "\n\n".join([p.get("content", p.get("text", "")) for p in pages])

    # ✅ FIX 2：必须用 chunks
    chunks = split_pages_into_chunks(pages)
    vector_store = build_vector_store(chunks)
    # =========================
    # SEND TO FASTAPI (IMPORTANT FIX)
    # =========================
    requests.post(
        f"{FASTAPI_URL}/build",
        json={"docs": chunks}
    )
    st.success("PDF loaded successfully")


# =========================
# ASK QUESTION (FASTAPI CALL)
# =========================
query = st.text_input("Ask a question about the paper")

if st.button("💬 Ask") and vector_store:

    with st.spinner("🧠 FastAPI 处理中..."):

        docs = retrieve_relevant_chunks(vector_store, query, k=3)

        # ✅ FIX 3：统一 content
        context = "\n\n".join([d.get("content", "") for d in docs])

        full_context = context + "\n\n" + st.session_state.table_summary

        response = requests.post(
            f"{FASTAPI_URL}/ask",
            json={
                "question": query,
                "context": full_context
            }
        )

        if response.status_code == 200:
            st.session_state.answer = response.json()["answer"]
        else:
            st.error("FastAPI 请求失败")

    st.success("回答完成")

    st.markdown("## 🧠 Answer")
    st.write(st.session_state.answer)


# =========================
# PAPER ANALYSIS
# =========================
if st.button("📊 Generate Paper Analysis"):

    with st.spinner("📊 FastAPI 分析中..."):

        response = requests.post(
            f"{FASTAPI_URL}/ask",
            json={
                "question": "请分析这篇论文的Abstract、Contribution和Conclusion（中文）",
                "context": paper_context
            }
        )

        if response.status_code == 200:
            st.session_state.analysis_text = response.json()["answer"]

    st.success("分析完成")

    st.markdown("## 📊 Analysis")
    st.write(st.session_state.analysis_text)


if st.button("🏆 Generate SOTA Analysis"):

    with st.spinner("📈 FastAPI 分析SOTA中..."):

        response = requests.post(
            f"{FASTAPI_URL}/sota",
            json={
                "question": "分析SOTA",
                "context": paper_context
            }
        )

        if response.status_code == 200:
            st.session_state.sota_analysis = response.json()["sota"]
        else:
            st.error("SOTA API 请求失败")

    st.success("SOTA分析完成")

    st.markdown("## 🏆 SOTA Analysis")
    st.write(st.session_state.sota_analysis)


# =========================
# REPORT
# =========================
if st.button("📄 Generate Report"):

    report = generate_markdown_report(
        answer=st.session_state.answer,
        analysis_text=st.session_state.analysis_text,
        sota_analysis=st.session_state.sota_analysis,
        table_summary=st.session_state.table_summary
    )

    st.download_button(
        "⬇ Download Report",
        report,
        file_name="research_report.md"
    )
