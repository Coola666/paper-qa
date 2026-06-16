📄 Research Paper AI Agent (LLM + RAG + FastAPI + Streamlit)
🚀 Project Overview

This project is an AI-powered research paper analysis system that combines:

🧠 Large Language Models (DeepSeek / OpenAI-compatible API)
📚 Retrieval-Augmented Generation (RAG)
⚡ FastAPI backend service
🎨 Streamlit interactive frontend
📄 PDF parsing + automatic paper understanding
📊 SOTA (State-of-the-Art) experimental analysis

It enables users to upload research papers and automatically:

Ask questions about papers
Extract abstract / contributions / conclusions
Analyze experimental results
Identify SOTA vs baseline performance
Generate structured research reports
🧩 System Architecture
                ┌──────────────────────┐
                │   Streamlit Frontend │
                │  (User Interface UI) │
                └──────────┬───────────┘
                           │ HTTP Requests
                           ▼
                ┌──────────────────────┐
                │   FastAPI Backend    │
                │  (LLM Orchestrator)  │
                └──────────┬───────────┘
                           │
         ┌─────────────────┼─────────────────┐
         ▼                 ▼                 ▼
 ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
 │   RAG Engine  │  │  LLM Client  │  │ PDF Parser   │
 │ (TF-IDF / FAISS)││ DeepSeek API │  │ PyMuPDF      │
 └──────────────┘  └──────────────┘  └──────────────┘
                           │
                           ▼
               ┌──────────────────────┐
               │  Research Insights   │
               │  + SOTA Analysis     │
               └──────────────────────┘
✨ Key Features
📄 Paper Understanding
Automatic PDF parsing
Chunk-based document processing
Page-aware text extraction
🧠 RAG Question Answering
TF-IDF / vector-based retrieval
Top-K relevant chunk selection
Context-aware LLM reasoning
📊 Experimental Analysis
SOTA vs baseline detection
Automatic interpretation of results
Research insight summarization
📄 Report Generation
Markdown report export
Structured academic-style output
⚙️ Tech Stack
Frontend: Streamlit
Backend: FastAPI
LLM: DeepSeek / OpenAI-compatible API
RAG: TF-IDF (upgradeable to FAISS)
PDF Parsing: PyMuPDF
Data Processing: Pandas, NumPy
Visualization: Matplotlib
🚀 How to Run Locally
1️⃣ Install dependencies
pip install -r requirements.txt
2️⃣ Start FastAPI backend
uvicorn backend.main:app --reload

Backend runs at:

http://127.0.0.1:8000
3️⃣ Start Streamlit frontend
streamlit run app.py

Frontend runs at:

http://localhost:8501
🔑 Environment Variables

Create .env file:

DEEPSEEK_API_KEY=your_api_key_here
📊 Example Use Cases
Research paper understanding assistant
Academic experiment analysis tool
AI research copilot
Literature review automation
🧠 Future Improvements
FAISS vector database upgrade
Multi-paper comparison system
Real-time paper crawling (arXiv)
Automatic figure/table extraction (OCR + LayoutLM)
Docker deployment
Cloud SaaS version
👨‍💻 Author

Built as an AI Engineering Portfolio Project demonstrating:

LLM application development
RAG system design
FastAPI backend architecture
End-to-end AI product engineering