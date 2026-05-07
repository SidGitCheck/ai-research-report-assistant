from __future__ import annotations

from pathlib import Path

from src.reporting.markdown_export import export_markdown
from src.reporting.pdf_export import export_pdf
from src.schemas.report import ReportDraft


class ReportAgent:
    def generate(
        self,
        draft: ReportDraft,
        topic: str,
        sources: list[dict[str, str]],
        output_markdown_path: Path,
        output_pdf_path: Path | None = None,
    ) -> None:
        export_markdown(draft=draft, topic=topic, sources=sources, output_path=output_markdown_path)
        if output_pdf_path is not None:
            export_pdf(markdown_text=output_markdown_path.read_text(encoding="utf-8"), output_path=output_pdf_path)
