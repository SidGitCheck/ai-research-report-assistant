from __future__ import annotations

import re

from src.agents.llm_client import LLMClient
from src.schemas.plan import Plan
from src.schemas.report import ReportDraft
from src.schemas.review import ReviewIssue, ReviewResult


class ReviewerAgent:
    def __init__(self, llm: LLMClient) -> None:
        self.llm = llm

    def review(self, plan: Plan, draft: ReportDraft) -> ReviewResult:
        issues: list[ReviewIssue] = []
        for section in draft.claim_map:
            if not section.citation_chunk_ids:
                issues.append(
                    ReviewIssue(
                        severity="high",
                        category="citation_coverage",
                        evidence=f"Section '{section.section_heading}' has no citations.",
                    )
                )
        section_texts = self._extract_sections(draft.markdown)
        section_items = list(section_texts.items())
        for i in range(len(section_items)):
            title_i, text_i = section_items[i]
            words_i = text_i.split()
            if len(words_i) < 35:
                issues.append(
                    ReviewIssue(
                        severity="medium",
                        category="low_information",
                        evidence=f"Section '{title_i}' is too short to be informative.",
                    )
                )
            for j in range(i + 1, len(section_items)):
                title_j, text_j = section_items[j]
                overlap_ratio = self._token_overlap_ratio(text_i, text_j)
                if overlap_ratio > 0.72:
                    issues.append(
                        ReviewIssue(
                            severity="medium",
                            category="repetition",
                            evidence=f"Sections '{title_i}' and '{title_j}' are highly repetitive (overlap={overlap_ratio:.2f}).",
                        )
                    )

        prompt = f"""
Review this markdown report against rubric:
{plan.evaluation_rubric}

Report:
{draft.markdown[:6000]}

Return short critique bullets only.
"""
        critique = self.llm.generate(prompt=prompt, system_prompt="You are a strict reviewer.")
        actions = []
        if issues:
            actions.append("Rewrite only flagged sections with section-specific evidence and stronger citations.")
        if critique.strip():
            actions.append(critique.strip())
        needs_regeneration = len(issues) > 0
        return ReviewResult(issues=issues, recommended_actions=actions, needs_regeneration=needs_regeneration)

    @staticmethod
    def _extract_sections(markdown: str) -> dict[str, str]:
        sections: dict[str, str] = {}
        current_title = ""
        current_lines: list[str] = []
        for line in markdown.splitlines():
            if line.startswith("## "):
                if current_title:
                    sections[current_title] = "\n".join(current_lines).strip()
                current_title = line.replace("## ", "", 1).strip()
                current_lines = []
            else:
                if current_title:
                    current_lines.append(line)
        if current_title:
            sections[current_title] = "\n".join(current_lines).strip()
        return sections

    @staticmethod
    def _token_overlap_ratio(text_a: str, text_b: str) -> float:
        tokens_a = set(re.findall(r"[a-zA-Z]{3,}", text_a.lower()))
        tokens_b = set(re.findall(r"[a-zA-Z]{3,}", text_b.lower()))
        if not tokens_a or not tokens_b:
            return 0.0
        return len(tokens_a & tokens_b) / max(1, min(len(tokens_a), len(tokens_b)))
