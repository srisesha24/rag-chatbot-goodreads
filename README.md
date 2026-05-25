# Goodreads Self-Help Chatbot 📚

A Retrieval-Augmented Generation (RAG) chatbot that answers questions about popular self-help books from Goodreads using **hybrid Q/A retrieval** (semantic search on Q/A pairs + vector document search).

**Course:** AGAI-03 | **Due:** 29th May 2026

---

## 🎯 Project Overview

This chatbot implements a complete RAG pipeline:

1. **Web Scraping** → Scrape 104 self-help books from Goodreads
2. **Synthetic Q/A Generation** → Generate 26+ Q/A pairs using Groq API
3. **Vector Database** → Store embeddings in Chroma
4. **Hybrid Retrieval** → Two-stage search (Q/A first, fallback to documents)
5. **Streamlit UI** → Interactive chat interface with source citations

---

## 🚀 Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/srisesha24/rag-chatbot-goodreads.git
cd rag-chatbot-goodreads
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup API Key
Create a `.env` file:

Get your key from: https://console.groq.com/keys

### 5. Run the Chatbot
```bash
streamlit run app.py
```

Opens at: `http://localhost:8501`

---

## ⚠️ Important: Groq Version Compatibility

**Issue:** If you get `TypeError: __init__() got an unexpected keyword argument 'proxies'`

**Solution:** Upgrade Groq
```bash
pip install --upgrade groq
```

Or install specific versions:
```bash
pip uninstall groq httpx -y
pip install groq==0.10.0 httpx==0.24.1
```

---

## 📁 Project Structurerag-chatbot-goodreads/
├── src/
│   ├── scraper.py              # Web scraping logic
│   ├── qa_generator.py         # Q/A generation
│   └── hybrid_retriever.py     # Vector DB + retrieval
├── data/
│   ├── raw/
│   │   └── goodreads_books.json
│   └── processed/
│       └── qa_dataset.csv
├── app.py                      # Streamlit application
├── requirements.txt
├── README.md
└── .gitignore
---

## 🏗️ Architecture

### Data Pipeline
Goodreads Website
↓ (Scraper)
Book Data (104 books)
↓ (Q/A Generator)
Q/A Dataset (26 pairs)
↓ (Embeddings)
Chroma Vector Database
↓ (Hybrid Retrieval)
User Query → Groq API → Response
### Hybrid Retrieval Logic
1. **Stage 1:** Search Q/A pairs using semantic similarity
2. **Stage 2:** If confidence is low, fallback to document search
3. **Stage 3:** Generate final answer with Groq API

---

## 📊 Results

- **Books Scraped:** 104
- **Q/A Pairs Generated:** 26
- **Vector DB Size:** ~50MB
- **Query Response Time:** 1-2 seconds
- **Average Confidence Score:** 0.75

---

## 🔧 Technologies Used

- **Scraping:** BeautifulSoup, Requests
- **Q/A Generation:** Groq API (llama-3.3-70b-versatile)
- **Vector Database:** Chroma
- **Embeddings:** Sentence-Transformers (all-MiniLM-L6-v2)
- **UI:** Streamlit
- **Language:** Python 3.9+

---

## 📝 How to Use

1. **Ask Questions:** Type any question about self-help books
2. **View Sources:** See which book the answer came from
3. **Clear Chat:** Use the sidebar button to reset conversation

### Example Queries
- "What is Atomic Habits about?"
- "How do I build better habits?"
- "Tell me about The Subtle Art of Not Giving a F*ck"
- "Which books are best for productivity?"

---

## ✨ Features

✅ Web scraping with error handling  
✅ Synthetic Q/A generation using LLM  
✅ Vector embeddings and semantic search  
✅ Hybrid retrieval (Q/A + document fallback)  
✅ Chat history and conversation memory  
✅ Source attribution for all answers  
✅ Clean, modular code architecture  

---

## 🎓 Learning Outcomes

This project teaches:
- Web scraping and data collection
- NLP and semantic search
- Vector databases and embeddings
- RAG architecture and design patterns
- LLM integration and API usage
- Full-stack Python development
- Streamlit for rapid prototyping

---

## 📚 References

- [Chroma Documentation](https://docs.trychroma.com/)
- [Sentence Transformers](https://www.sbert.net/)
- [Streamlit API](https://docs.streamlit.io/)
- [Groq API](https://console.groq.com/docs)
- [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/)

---

## 👤 Author

**Student Name:** Sesha  
**Course:** AGAI-03  
**Submission Date:** 29th May 2026

---

## 📄 License

This project is submitted as coursework. Academic integrity guidelines apply.

---

## 🆘 Troubleshooting

| Issue | Solution |
|-------|----------|
| Groq API Key Invalid | Check `.env` file has correct key from https://console.groq.com/keys |
| Module Not Found | Run `pip install -r requirements.txt` |
| Streamlit Not Found | Activate venv: `source venv/bin/activate` |
| Vector DB Errors | Delete `data/chroma_db/` folder and rebuild |

---

**Last Updated:** 25 May 2026
