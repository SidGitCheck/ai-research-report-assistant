from __future__ import annotations

from pathlib import Path

from jinja2 import Template

from src.schemas.report import ReportDraft


def _sanitize_body_markdown(markdown: str) -> str:
    lines = markdown.splitlines()
    safe_lines: list[str] = []
    blocked_prefixes = (
        "import ",
        "from ",
        "def ",
        "class ",
        "print(",
        "debug:",
        "implementation:",
        "internal:",
        "traceback",
    )
    for raw_line in lines:
        line = raw_line.rstrip()
        stripped = line.strip()
        if not stripped:
            if safe_lines and safe_lines[-1] != "":
                safe_lines.append("")
            continue
        if stripped.startswith("```"):
            continue
        lowered = stripped.lower()
        if any(lowered.startswith(prefix) for prefix in blocked_prefixes):
            continue
        # Keep only section-level headings in body to avoid duplicating the report title.
        if stripped.startswith("# ") and not stripped.startswith("## "):
            continue
        safe_lines.append(line)
    while safe_lines and safe_lines[-1] == "":
        safe_lines.pop()
    return "\n".join(safe_lines)


def export_markdown(
    draft: ReportDraft,
    topic: str,
    sources: list[dict[str, str]],
    output_path: Path,
) -> None:
    template_path = Path("src/reporting/templates/report_md_template.jinja")
    template = Template(template_path.read_text(encoding="utf-8"))
    markdown = template.render(
        title=topic,
        executive_summary=f"This report synthesizes findings about {topic}.",
        methodology="Planner -> Research -> Retrieval -> Writing -> Review loop",
        body_markdown=_sanitize_body_markdown(draft.markdown),
        sources=sources,
    )
    output_path.write_text(markdown, encoding="utf-8")
