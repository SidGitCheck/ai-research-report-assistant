# 🤖 Autonomous Multi-Agent AI Research Assistant

> A modular multi-agent RAG system that autonomously researches any topic, stores semantic memory, generates citation-backed reports, and self-reviews before final output.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![ChromaDB](https://img.shields.io/badge/Vector_DB-ChromaDB-1D9E75?style=flat-square)
![LLM](https://img.shields.io/badge/LLM-Groq_%2F_Ollama-7F77DD?style=flat-square)
![Framework](https://img.shields.io/badge/Framework-CrewAI_%2F_LangChain-BA7517?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## ✨ Features

| Feature | Description |
|---|---|
| 🧠 Multi-agent orchestration | Planner → Researcher → Writer → Reviewer pipeline |
| 🔍 RAG pipeline | Semantic retrieval with ChromaDB vector store |
| 📦 Persistent memory | Source provenance tracked in SQLite |
| 📝 Report generation | Citation-aware markdown + optional PDF export |
| 🔄 Self-critique loop | Reviewer agent validates and triggers regeneration |
| 🖥️ Streamlit UI | Clean optional frontend for interactive use |

---

## 🏗️ Architecture

```
User Input (topic)
       │
       ▼
┌─────────────────┐
│  Planner Agent  │  ← Decomposes topic into research subtasks
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Research Agent  │  ← Web search → scrape → chunk → embed
└────────┬────────┘
         │
         ▼
┌──────────────────────────────┐
│  Semantic Memory             │
│  ChromaDB (vectors)          │
│  SQLite (source metadata)    │
└────────┬─────────────────────┘
         │
         ▼
┌─────────────────┐
│  Writer Agent   │  ← RAG retrieval → structured report draft
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Reviewer Agent  │  ← Validates coverage, citations, quality
└────────┬────────┘
         │
         ▼
┌──────────────────┐
│ Report Generator │  ← Final markdown + PDF with citations
└──────────────────┘
```

---

## 🔬 Example Workflow

**Input:** `"Explain BERT vs GPT"`

1. **Planner** creates a 5-section report outline
2. **Research Agent** retrieves 8 sources via DuckDuckGo, scrapes and chunks text
3. **Chunks** are embedded and stored in ChromaDB with source URLs in SQLite
4. **Writer Agent** queries ChromaDB, generates grounded sections using Groq LLM
5. **Reviewer Agent** scores each section, flags gaps, triggers selective regeneration
6. **Report Generator** assembles final markdown with citations and exports PDF

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.10+ |
| Agent Framework | CrewAI / LangChain |
| LLM | Groq (free tier) or Ollama (local) |
| Vector DB | ChromaDB |
| Metadata DB | SQLite |
| Embeddings | sentence-transformers |
| Web Search | DuckDuckGo Search API |
| Scraping | BeautifulSoup + requests |
| Frontend | Streamlit |
| Report Export | markdown, fpdf2 |

> ✅ **100% free stack** — no paid APIs required.

---

## 📁 Project Structure

```
src/
├── agents/
│   ├── planner.py         # Task decomposition
│   ├── researcher.py      # Search + scrape + embed
│   ├── writer.py          # RAG-grounded report generation
│   └── reviewer.py        # Quality validation + feedback
├── memory/
│   ├── vector_store.py    # ChromaDB interface
│   └── metadata_db.py     # SQLite source tracking
├── tools/
│   ├── search.py          # DuckDuckGo wrapper
│   ├── scraper.py         # BeautifulSoup scraper
│   └── embedder.py        # sentence-transformers
├── reporting/
│   └── report_gen.py      # Markdown + PDF export
├── schemas/               # Pydantic data models
├── app/
│   ├── main.py            # CLI entrypoint
│   └── ui.py              # Streamlit frontend
└── utils/
    ├── config.py
    └── logger.py
```

---

## 🚀 Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/your-username/research-agent
cd research-agent

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set your Groq API key (free at console.groq.com)
export GROQ_API_KEY=your_key_here

# 4. Run the pipeline
python -m src.app.main \
  --topic "Explain BERT vs GPT" \
  --max-sources 8 \
  --max-chunks 30

# 5. (Optional) Launch Streamlit UI
streamlit run src/app/ui.py
```

---

## 📊 Output

The pipeline produces:
- `outputs/report.md` — structured markdown report with inline citations
- `outputs/report.pdf` — formatted PDF export
- `outputs/sources.db` — SQLite database of all retrieved sources

---

## 🗺️ Roadmap

- [x] MVP: Planner → Researcher → Writer → Report
- [x] Reviewer agent with self-critique loop
- [ ] Confidence scoring per section
- [ ] Multi-topic comparison reports
- [ ] Web UI with real-time pipeline visualization
- [ ] Export to Notion / Google Docs

---

## 🤝 Contributing

Pull requests welcome. For major changes, open an issue first.

---

## 📄 License

MIT
