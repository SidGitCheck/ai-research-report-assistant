<div align="center">

# 🧠 Autonomous Multi-Agent AI Research Assistant

**An end-to-end agentic AI system that researches any topic, stores semantic memory,<br>generates citation-backed reports, and self-reviews before final output.**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![ChromaDB](https://img.shields.io/badge/Vector_DB-ChromaDB-1D9E75?style=for-the-badge)](https://trychroma.com)
[![Gemini](https://img.shields.io/badge/LLM-Gemini_%7C_Groq_%7C_Ollama-7F77DD?style=for-the-badge)](https://groq.com)
[![License](https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-BA7517?style=for-the-badge)]()

<br>

> *"Not a chatbot wrapper. A real agentic pipeline with planning, retrieval, memory, and self-critique."*

</div>

---

## 📌 What Is This?

Most AI projects are simple API wrappers. This isn't.

This project implements a **full multi-agent orchestration system** where autonomous agents collaborate to research a topic end-to-end — searching the web, building semantic memory, writing grounded reports, and reviewing their own output before delivering a final citation-backed document.

Built to demonstrate real AI engineering concepts: **RAG**, **multi-agent orchestration**, **vector memory**, **provider failover**, and **automated quality loops** — all on a completely free stack.

---

## ✨ Features

- 🤖 **5-agent pipeline** — Planner → Researcher → Writer → Reviewer → Report Generator
- 🔄 **Automatic LLM failover** — Gemini → OpenRouter → Groq → Ollama → Mock
- 🧠 **Persistent semantic memory** — ChromaDB vector store + SQLite metadata catalog
- 🌐 **Web retrieval pipeline** — DuckDuckGo search + content extraction + semantic chunking
- 📝 **Grounded report generation** — structured markdown with inline citations
- 🔍 **Self-critique loop** — Reviewer validates coverage, repetition, and citation quality
- 📦 **Run artifacts** — every run saves a full audit trail of plan, sources, draft, review, and final report
- 📄 **PDF export** — ReportLab-powered styled PDF output

---

## 🏗️ Architecture

```
                        ┌─────────────────────────────────┐
                        │         User Input (topic)      │
                        └────────────────┬────────────────┘
                                         │
                              ┌──────────▼──────────┐
                              │    Planner Agent    │
                              │  sections • queries │
                              │  strategies • budget│
                              └──────────┬──────────┘
                                         │
                              ┌──────────▼──────────┐
                              │   Research Agent    │
                              │  search • fetch     │
                              │  extract • chunk    │
                              └──────────┬──────────┘
                                         │
                   ┌─────────────────────▼──────────────────────┐
                   │               Memory Layer                 │
                   │   ChromaDB (vector embeddings)             │
                   │   SQLite (sources, metadata, run tracking) │
                   └─────────────────────┬──────────────────────┘
                                         │
                              ┌──────────▼──────────┐
                              │    Writer Agent     │
                              │  retrieve • ground  │
                              │  synthesize • cite  │
                              └──────────┬──────────┘
                                         │
                              ┌──────────▼──────────┐
                              │   Reviewer Agent    │
                              │  coverage • clarity │
                              │  citations • repeat │
                              └──────────┬──────────┘
                                         │
                              ┌──────────▼──────────┐
                              │   Report Generator  │
                              │  final.md • PDF     │
                              │  run artifacts      │
                              └─────────────────────┘
```

---

## 🔄 Provider Failover System

The system automatically falls back across LLM providers at runtime — zero manual switching needed.

```
Gemini  ──✗──▶  OpenRouter  ──✗──▶  Groq  ──✗──▶  Ollama  ──✗──▶  Mock
  ✓                  ✓                ✓               ✓               ✓
(primary)        (fallback 1)   (fallback 2)    (local/offline)  (dev mode)
```

This makes the project resilient to API failures, rate limits, and offline environments — a real production engineering concern.

---

## 🔬 Example Run

**Input:**
```
Compare BERT vs GPT — architecture, training objectives,
fine-tuning, scalability, hallucination risks, enterprise use cases
```

**Pipeline execution:**

```
[LLM] Trying provider: gemini
[LLM] Provider success: gemini

{"event": "planning_completed",   "sections": 8}
{"event": "research_completed",   "source_count": 9, "chunk_count": 45}
{"event": "writing_completed"}
{"event": "review_completed",     "needs_regeneration": false}
{"event": "report_generated"}
```

**Output:** A structured 8-section markdown + PDF report with inline citations, source manifest, and review log.

---

## 📂 Project Structure

```
src/
├── agents/
│   ├── planner_agent.py       # Topic decomposition → research plan
│   ├── research_agent.py      # Search + scrape + chunk + embed
│   ├── writer_agent.py        # RAG retrieval → grounded sections
│   ├── reviewer_agent.py      # Quality validation + feedback
│   ├── report_agent.py        # Final assembly + export
│   └── llm_client.py          # Multi-provider client with failover
│
├── app/
│   ├── main.py                # CLI entrypoint
│   └── orchestrator.py        # Pipeline runner
│
├── memory/
│   ├── chroma_store.py        # ChromaDB vector interface
│   ├── sqlite_catalog.py      # Source metadata + run tracking
│   └── memory_manager.py      # Unified memory abstraction
│
├── tools/
│   ├── web_search_duckduckgo.py
│   ├── web_fetch.py
│   ├── web_extract.py
│   ├── vector_retrieval.py
│   └── citation_builder.py
│
├── reporting/
│   ├── markdown_export.py
│   ├── pdf_export.py
│   └── templates/
│
├── schemas/                   # Pydantic data models
├── config/                    # Settings + provider config
├── utils/                     # Logger, helpers
└── ui/
    └── streamlit_app.py       # Optional Streamlit frontend
```

---

## 📦 Run Artifacts

Every pipeline run saves a complete audit trail under `data/runs/<run_id>/`:

| File | Contents |
|---|---|
| `plan.json` | Generated research plan + section outlines |
| `retrieval_manifest.json` | All retrieved sources with URLs |
| `claim_map.json` | Chunk-to-section citation mappings |
| `draft.md` | First-pass writer output |
| `review.json` | Reviewer scores and feedback |
| `final.md` | Final polished report |
| `run_metadata.json` | Provider used, timings, token counts |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.10+ |
| LLM Providers | Gemini, Groq, OpenRouter, Ollama |
| Vector Database | ChromaDB |
| Metadata Store | SQLite |
| Embeddings | Sentence Transformers |
| Web Retrieval | DuckDuckGo + Requests + BeautifulSoup |
| PDF Export | ReportLab |
| UI (optional) | Streamlit |

> ✅ **Fully free stack** — Gemini free tier + Groq free tier + local Ollama. No credit card needed.

---

## 🚀 Getting Started

**1. Clone and set up**
```bash
git clone https://github.com/your-username/research-agent
cd research-agent
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**2. Configure environment**
```bash
cp .env.example .env
```
```env
LLM_PROVIDER=gemini
GEMINI_API_KEY=your_key_here

GROQ_API_KEY=your_key_here
GROQ_MODEL=llama-3.1-8b-instant

OPENROUTER_API_KEY=your_key_here
OLLAMA_BASE_URL=http://localhost:11434
```

**3. Run**
```bash
python -m src.app.main \
  --topic "Explain BERT vs GPT in depth" \
  --provider gemini \
  --max-sources 10 \
  --max-chunks 50
```

---

## 🗺️ Roadmap

- [x] Multi-agent orchestration pipeline
- [x] ChromaDB + SQLite memory layer
- [x] Multi-provider LLM failover
- [x] Reviewer self-critique loop
- [x] Run artifact logging
- [ ] Streamlit real-time UI with pipeline visualization
- [ ] Async retrieval for faster research
- [ ] Advanced reranking (cross-encoder)
- [ ] Source reliability scoring
- [ ] LangGraph integration
- [ ] Agent memory persistence across runs

---

## 💡 Why This Project?

This project was built to go beyond tutorial-level GenAI work and demonstrate practical AI engineering:

- **Orchestration** — agents collaborate with defined roles, not a single monolithic prompt
- **RAG** — grounded generation from retrieved context, not hallucinated answers
- **Memory** — semantic vector store + relational metadata working together
- **Resilience** — provider failover handles real-world API instability
- **Quality loops** — automated self-review mirrors production AI evaluation pipelines

---

## 📄 License

MIT — free to use, modify, and build on.
