# 📄 Research Paper & Experiment Analysis Agent (RAG + LLM)

An AI-powered research assistant that enables users to analyze academic papers and experimental results through a Retrieval-Augmented Generation (RAG) pipeline.

---

## 🚀 Demo Features

### 📚 Paper Understanding (RAG)
- Upload PDF research papers
- Automatically extract and chunk content
- Retrieve most relevant sections based on user query
- Generate LLM-based answers grounded in paper content

### 📊 Experiment Analysis (CSV)
- Upload experimental result tables (CSV)
- Automatically compute statistical summaries (mean / max / min)
- Combine experiment results with paper context for reasoning

### 🧠 LLM-Powered Reasoning (DeepSeek API)
- Unified reasoning over:
  - Paper content
  - Retrieved chunks
  - Experiment results
- Generates final structured answers

### 📑 Report Generation
- Automatically generate Markdown research reports
- Include:
  - LLM answers
  - Retrieved sources (Page-level citation)
  - Experiment summary

---

## 🏗️ System Architecture


PDF → Text Extraction (PyMuPDF)
→ Chunking
→ Lightweight Retrieval (TF-IDF style)
→ Top-K Context

CSV → Pandas Analysis → Experiment Summary

Paper Context + Experiment Context
↓
DeepSeek LLM
↓
Final Answer + Report


---

## 🧰 Tech Stack

- Python
- Streamlit (UI)
- DeepSeek API (LLM)
- PyMuPDF (PDF parsing)
- Pandas (data analysis)
- Custom lightweight retrieval (no heavy vector DB)

---

## ⚙️ How to Run

```bash
pip install -r requirements.txt
streamlit run app.py
📌 Example Workflow
Upload a research paper (PDF)
Upload experiment results (CSV)
Ask questions like:
"What are the main contributions?"
"Do experiments support the claims?"
Generate final report
🧠 Key Highlights (For Interview)
Built a full RAG pipeline from scratch without relying on heavy frameworks
Integrated structured (CSV) + unstructured (PDF) data reasoning
Implemented retrieval-based grounding with source citation (Page-level)
Designed LLM-based research assistant workflow end-to-end
📈 Future Improvements
Replace TF-IDF with embedding-based retrieval
Add chart visualization (ROC / accuracy curves)
Multi-paper comparison system
Deployment on cloud (Streamlit / Docker)