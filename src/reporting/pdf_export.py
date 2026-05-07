from __future__ import annotations

from pathlib import Path


def export_pdf(markdown_text: str, output_path: Path) -> None:
    try:
        from weasyprint import HTML  # type: ignore
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError("PDF export requires optional dependency: pip install .[pdf]") from exc

    html_content = f"<html><body><pre>{markdown_text}</pre></body></html>"
    HTML(string=html_content).write_pdf(str(output_path))
