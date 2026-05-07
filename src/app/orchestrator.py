from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from src.agents.llm_client import LLMClient
from src.agents.planner_agent import PlannerAgent
from src.agents.report_agent import ReportAgent
from src.agents.research_agent import ResearchAgent
from src.agents.reviewer_agent import ReviewerAgent
from src.agents.writer_agent import WriterAgent
from src.config.settings import Settings
from src.memory.chroma_store import ChromaStore
from src.memory.memory_manager import MemoryManager
from src.memory.sqlite_catalog import SqliteCatalog
from src.schemas.report import ReportDraft
from src.utils.logging import configure_logger, log_event


@dataclass(slots=True)
class RunResult:
    run_id: str
    run_dir: Path
    final_markdown_path: Path
    final_pdf_path: Path | None


class Orchestrator:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.settings.ensure_dirs()

    def run(
        self,
        topic: str,
        max_sources: int = 8,
        max_chunks: int = 30,
        export_pdf: bool = False,
        dry_run: bool = False,
    ) -> RunResult:
        run_id = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        run_dir = self.settings.runs_dir / run_id
        logger = configure_logger(run_dir)
        log_event(logger, "run_started", run_id=run_id, topic=topic)

        sqlite_catalog = SqliteCatalog(self.settings.sqlite_path)
        sqlite_catalog.create_run(run_id=run_id, topic=topic)
        chroma_store = ChromaStore(self.settings.chroma_dir, self.settings.embedding_model)
        memory = MemoryManager(sqlite_catalog=sqlite_catalog, chroma_store=chroma_store)
        llm = LLMClient(
            provider=self.settings.llm_provider,
            model=self.settings.llm_model,
            ollama_base_url=self.settings.ollama_base_url,
            groq_api_key=self.settings.groq_api_key,
        )

        planner = PlannerAgent(llm=llm)
        researcher = ResearchAgent(
            memory=memory,
            timeout_seconds=self.settings.request_timeout_seconds,
            max_extract_chars=self.settings.max_extract_chars,
        )
        writer = WriterAgent(llm=llm, memory=memory)
        reviewer = ReviewerAgent(llm=llm)
        reporter = ReportAgent()

        log_event(logger, "planning_started")
        plan = planner.plan(topic=topic, max_sources=max_sources, max_chunks=max_chunks)
        (run_dir / "plan.json").write_text(json.dumps(plan.model_dump(), indent=2), encoding="utf-8")
        log_event(logger, "planning_completed", sections=len(plan.sections))

        if not dry_run:
            log_event(logger, "research_started")
            retrieval_stats = researcher.run(run_id=run_id, plan=plan)
            (run_dir / "retrieval_manifest.json").write_text(
                json.dumps(retrieval_stats, indent=2),
                encoding="utf-8",
            )
            log_event(logger, "research_completed", **retrieval_stats)
        else:
            (run_dir / "retrieval_manifest.json").write_text(
                json.dumps({"dry_run": True, "source_count": 0, "chunk_count": 0}, indent=2),
                encoding="utf-8",
            )

        log_event(logger, "writing_started")
        draft: ReportDraft = writer.write(run_id=run_id, plan=plan)
        (run_dir / "draft.md").write_text(draft.markdown, encoding="utf-8")
        (run_dir / "claim_map.json").write_text(
            json.dumps([item.model_dump() for item in draft.claim_map], indent=2),
            encoding="utf-8",
        )
        log_event(logger, "writing_completed")

        log_event(logger, "review_started")
        review = reviewer.review(plan=plan, draft=draft)
        (run_dir / "review.json").write_text(json.dumps(review.model_dump(), indent=2), encoding="utf-8")
        log_event(logger, "review_completed", needs_regeneration=review.needs_regeneration)

        if review.needs_regeneration and not dry_run:
            log_event(logger, "regeneration_started")
            draft = writer.write(run_id=run_id, plan=plan, per_section_k=7)
            (run_dir / "draft_regenerated.md").write_text(draft.markdown, encoding="utf-8")
            log_event(logger, "regeneration_completed")

        final_md = run_dir / "final.md"
        final_pdf = run_dir / "final.pdf" if export_pdf else None
        sources_rows = sqlite_catalog.get_sources_by_run(run_id=run_id)
        sources = [{"title": row["title"], "url": row["url"]} for row in sources_rows]
        reporter.generate(
            draft=draft,
            topic=topic,
            sources=sources,
            output_markdown_path=final_md,
            output_pdf_path=final_pdf,
        )
        log_event(logger, "report_generated", markdown=str(final_md), pdf=str(final_pdf) if final_pdf else None)
        return RunResult(run_id=run_id, run_dir=run_dir, final_markdown_path=final_md, final_pdf_path=final_pdf)
