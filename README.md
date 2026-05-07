
# Autonomous Multi-Agent AI Research Assistant

A modular multi-agent RAG system that autonomously researches a topic, stores semantic memory, generates citation-backed reports, and performs self-review before final output generation.

---

## Features

- Multi-agent orchestration pipeline
- Retrieval-Augmented Generation (RAG)
- Semantic memory with ChromaDB
- Source provenance tracking with SQLite
- Citation-aware report generation
- Reviewer/self-critique loop
- Markdown + optional PDF export
- Ollama and Groq support

---

## Architecture

User Topic
    ↓
Planner Agent
    ↓
Research Agent
    ↓
Semantic Memory (Chroma + SQLite)
    ↓
Writer Agent
    ↓
Reviewer Agent
    ↓
Final Report Generator

---

## Example Workflow

Input:
"Explain BERT vs GPT"

Pipeline:
1. Planner creates report outline
2. Research agent retrieves sources
3. Text is chunked and embedded
4. Writer generates grounded sections
5. Reviewer validates coverage/citations
6. Final markdown report exported

---

## Tech Stack

- Python
- ChromaDB
- SQLite
- Ollama / Groq
- BeautifulSoup
- Sentence Transformers
- Streamlit (optional)

---

## Project Structure

src/
├── agents/
├── memory/
├── tools/
├── reporting/
├── schemas/
├── app/
└── utils/

---

## Running the Project

```bash
python -m src.app.main \
  --topic "Explain BERT vs GPT" \
  --max-sources 8 \
  --max-chunks 30
