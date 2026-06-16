# 📄 Research Paper AI Agent (LLM + RAG + FastAPI + Streamlit)

## 🚀 Overview

This project is an AI-powered research paper analysis system that integrates Large Language Models (DeepSeek API), Retrieval-Augmented Generation (RAG), FastAPI backend, and Streamlit frontend. It enables users to upload academic papers in PDF format and automatically perform question answering, section extraction, experimental result analysis, SOTA comparison, and structured report generation.

The system is designed as a full-stack AI engineering project demonstrating LLM application development, RAG pipeline construction, and backend-service separation.

---

## 🧠 System Architecture

User uploads PDF → Streamlit frontend → FastAPI backend → RAG retrieval system → LLM reasoning (DeepSeek API) → structured academic insights returned to frontend.

Architecture:

User
↓
Streamlit Frontend (UI Layer)
↓ HTTP Requests
FastAPI Backend (Core Orchestration Layer)
↓
PDF Parser (PyMuPDF)
RAG Engine (TF-IDF / Vector Retrieval)
LLM Client (DeepSeek API)
↓
Final Research Insights

---

## ✨ Features

### 📄 Paper Understanding
- PDF upload and parsing
- Page-level text extraction
- Chunk-based document segmentation

### 🧠 RAG Question Answering
- Top-K semantic retrieval
- Context-aware LLM reasoning
- Source-aware responses

### 📊 SOTA Analysis
- Automatic extraction of experimental results
- Comparison between SOTA and baseline methods
- Structured academic interpretation

### 📄 Report Generation
- Markdown report export
- Structured research summaries
- Reusable academic output format

---

## ⚙️ Tech Stack

Frontend: Streamlit  
Backend: FastAPI  
LLM: DeepSeek API (OpenAI-compatible)  
RAG: TF-IDF / Vector-based retrieval  
PDF Parsing: PyMuPDF  
Data Processing: Pandas, NumPy  
Visualization: Matplotlib  

---

## 🚀 How to Run Locally

### Step 1: Install dependencies
```bash
pip install -r requirements.txt
Step 2: Start FastAPI backend
uvicorn backend.main:app --reload

Backend runs at:
http://127.0.0.1:8000

API documentation:
http://127.0.0.1:8000/docs

Step 3: Start Streamlit frontend
streamlit run app.py

Frontend runs at:
http://localhost:8501

🔑 Environment Variables

Create a .env file in project root:

DEEPSEEK_API_KEY=your_api_key_here

📊 Example Use Cases
Research paper assistant
Academic experiment analyzer
Automated literature review tool
SOTA benchmarking system
AI research copilot
🧠 Future Improvements
FAISS vector database upgrade
Multi-paper comparison system
ArXiv automatic paper ingestion
OCR-based table extraction improvement
Docker production deployment
Cloud SaaS version
👨‍💻 Author

This project demonstrates advanced AI engineering skills including LLM application development, RAG system design, FastAPI backend architecture, and full-stack AI product implementation.

It is designed as a portfolio project for AI Engineer / LLM Engineer roles.