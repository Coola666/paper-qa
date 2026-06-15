import streamlit as st
import tempfile
import pandas as pd
import matplotlib.pyplot as plt

from openai import OpenAI

from utils import DEEPSEEK_API_KEY
from pdf_utils import extract_pages_from_pdf
from rag_utils import split_pages_into_chunks, build_vector_store, retrieve_relevant_chunks
from table_utils import extract_tables_from_llm, analyze_sota_vs_baseline
from report_utils import extract_sections_from_llm, generate_markdown_report


# =========================
# LLM CLIENT
# =========================
client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com/v1"
)

st.set_page_config(layout="wide")
st.title("📄 Research Paper AI Agent (Final Version)")


# =========================
# SESSION STATE（核心）
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
chunks = []
docs = []
paper_context = ""
tables_data = []

if uploaded_pdf:

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_pdf.read())
        pdf_path = tmp.name

    # -------------------------
    # TEXT
    # -------------------------
    pages = extract_pages_from_pdf(pdf_path)

    paper_context = "\n\n".join(
        [p["text"] for p in pages]
    )

    chunks = split_pages_into_chunks(pages)
    vector_store = build_vector_store(chunks)

    st.success("PDF loaded successfully")


# =========================
# ASK QUESTION (中文修复)
# =========================
query = st.text_input("Ask a question about the paper")

if st.button("💬 Ask") and vector_store:

    with st.spinner("🧠 正在生成回答..."):

        docs = retrieve_relevant_chunks(vector_store, query, k=3)

        context = "\n\n".join([d["content"] for d in docs])

        full_context = context + "\n\n" + st.session_state.table_summary

        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {
                    "role": "system",
                    "content": "你是科研论文分析助手，必须全部用中文回答"
                },
                {
                    "role": "user",
                    "content": f"""
基于论文内容回答问题：

要求：
- 必须中文
- 不允许编造
- 如果不知道就说“不确定”

论文内容：
{full_context}

问题：
{query}
"""
                }
            ],
            temperature=0
        )

        st.session_state.answer = response.choices[0].message.content

        st.success("回答完成")

        st.markdown("## 🧠 Answer")
        st.write(st.session_state.answer)

        st.markdown("## 📌 Sources")
        for d in docs:
            st.write(f"Page {d['page']} | Score {d['score']:.2f}")


# =========================
# PAPER ANALYSIS（独立按钮）
# =========================
if st.button("📊 Generate Paper Analysis"):

    with st.spinner("📊 正在生成论文分析..."):

        st.session_state.analysis_text = extract_sections_from_llm(
            client,
            paper_context + "\n\n" + st.session_state.table_summary
        )

    st.success("分析完成")

    st.markdown("## 📊 Analysis")
    st.write(st.session_state.analysis_text)


# =========================
# SOTA ANALYSIS（独立按钮）
# =========================
if st.button("🏆 Generate SOTA Analysis"):

    with st.spinner("📈 正在分析SOTA vs Baseline..."):

        tables_data = extract_tables_from_llm(client, paper_context)

        st.session_state.sota_analysis = analyze_sota_vs_baseline(tables_data)

    st.success("SOTA分析完成")

    st.markdown("## 🏆 SOTA Analysis")
    st.write(st.session_state.sota_analysis)


# =========================
# TABLE VISUALIZATION
# =========================
if tables_data:

    st.markdown("## 📈 Visualization")

    try:
        df = pd.DataFrame([
            [str(c) for c in row]
            for row in tables_data[0]["data"]
        ])

        numeric = df.apply(pd.to_numeric, errors="coerce")

        if numeric.shape[1] > 0:

            fig, ax = plt.subplots()
            numeric.fillna(0).iloc[:, 0].plot(kind="bar", ax=ax)

            ax.set_title("Experimental Results")
            st.pyplot(fig)

    except:
        st.warning("Cannot plot tables")


# =========================
# REPORT GENERATION（稳定版）
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