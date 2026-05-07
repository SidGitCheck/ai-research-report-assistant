from __future__ import annotations

import argparse

from src.app.orchestrator import Orchestrator
from src.config.settings import settings


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Autonomous Multi-Agent AI Research & Report Assistant")
    parser.add_argument("--topic", required=True, help="Research topic")
    parser.add_argument("--max-sources", type=int, default=8, help="Maximum sources to fetch")
    parser.add_argument("--max-chunks", type=int, default=30, help="Maximum chunks to store")
    parser.add_argument("--model", default=None, help="Override model name")
    parser.add_argument("--provider", default=None, choices=["ollama", "groq", "mock"], help="LLM provider")
    parser.add_argument("--pdf", action="store_true", help="Export PDF output")
    parser.add_argument("--dry-run", action="store_true", help="Skip web retrieval and run synthetic flow")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    if args.model:
        settings.llm_model = args.model
    if args.provider:
        settings.llm_provider = args.provider

    orchestrator = Orchestrator(settings=settings)
    result = orchestrator.run(
        topic=args.topic,
        max_sources=args.max_sources,
        max_chunks=args.max_chunks,
        export_pdf=args.pdf,
        dry_run=args.dry_run,
    )
    print(f"Run completed: {result.run_id}")
    print(f"Markdown: {result.final_markdown_path}")
    if result.final_pdf_path:
        print(f"PDF: {result.final_pdf_path}")


if __name__ == "__main__":
    main()
