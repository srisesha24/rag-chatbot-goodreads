# 📚 Goodreads Self-Help Chatbot

> A Retrieval-Augmented Generation (RAG) chatbot for answering questions about self-help books from Goodreads.

**Course:** AGAI-03 | **Status:** ✅ Complete

---

## 📁 Project Structure

```
rag-chatbot-goodreads/
│
├── src/
│   ├── scraper.py
│   ├── qa_generator.py
│   └── hybrid_retriever.py
│
├── data/
│   ├── raw/
│   │   └── goodreads_books.json
│   └── processed/
│       └── qa_dataset.csv
│
├── app.py
├── requirements.txt
├── README.md
├── report.pdf
├── .env.example
├── .gitignore
└── [data/chroma_db/]
```

## 🚀 Quick Start

### Installation
```bash
git clone https://github.com/srisesha24/rag-chatbot-goodreads.git
cd rag-chatbot-goodreads
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Setup
```bash
cp .env.example .env
# Edit .env and add your Groq API key from https://console.groq.com/keys
```

### Run
```bash
streamlit run app.py
```

Opens at: `http://localhost:8501`

---

## 💡 How It Works

**Data Pipeline:**
1. **Scrape** → 104 books from Goodreads
2. **Generate** → 26 Q/A pairs using Groq API
3. **Index** → Vector embeddings in Chroma DB
4. **Retrieve** → Hybrid search (Q/A + fallback)
5. **Respond** → LLM generates answer with citations

---

## ✨ Key Features

- ✅ Web scraping with error handling
- ✅ Synthetic Q/A generation using LLM
- ✅ Vector embeddings & semantic search
- ✅ Hybrid retrieval (Q/A + document search)
- ✅ Chat interface with source attribution
- ✅ Professional Streamlit UI

---

## 📊 Results

- **Books Scraped:** 104
- **Q/A Pairs:** 26
- **Response Time:** 1-2 seconds
- **Confidence Score:** 0.75 average

---

## 👤 Team

- **Student:** Sesha
- **Course:** AGAI-03
- **Type:** Individual Submission

---

## 📚 References

- [Chroma Documentation](https://docs.trychroma.com/)
- [Sentence Transformers](https://www.sbert.net/)
- [Streamlit](https://docs.streamlit.io/)
- [Groq API](https://console.groq.com/docs)

---

**Repository:** https://github.com/srisesha24/rag-chatbot-goodreads  
**Last Updated:** 25 May 2026
