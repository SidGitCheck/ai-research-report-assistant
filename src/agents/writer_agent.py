from __future__ import annotations

import re

from src.agents.llm_client import LLMClient
from src.memory.memory_manager import MemoryManager
from src.schemas.plan import Plan
from src.schemas.report import ClaimMapItem, ReportDraft


class WriterAgent:
    def __init__(self, llm: LLMClient, memory: MemoryManager) -> None:
        self.llm = llm
        self.memory = memory

    def write(self, run_id: str, plan: Plan, per_section_k: int = 5) -> ReportDraft:
        sections_md: list[str] = ["## Introduction", f"Research report on {plan.topic}."]
        claim_map: list[ClaimMapItem] = []
        used_sentences: set[str] = set()

        for section in plan.sections:
            query = section.query_strategy[0] if section.query_strategy else section.title
            chunk_ids = self.memory.retrieve_chunk_ids(run_id=run_id, query_text=query, n_results=per_section_k)
            chunks = self.memory.sqlite_catalog.get_chunks_by_ids(chunk_ids)
            context_lines = [
                f"- ({c['chunk_id']}) {c['text'][:350]} ... source: {c['source_title']} ({c['source_url']})"
                for c in chunks
            ]
            context = "\n".join(context_lines) if context_lines else "- No retrieved context."
            prompt = f"""
Write a concise markdown section titled "{section.title}" for topic "{plan.topic}".
Focus ONLY on this section and do not repeat wording from other sections.
Use only provided context. Add citation tokens like [chunk_id] for factual lines.
Use 2-3 distinct bullets or short paragraphs with concrete differences, not generic text.
Context:
{context}
"""
            section_text = self.llm.generate(prompt=prompt, system_prompt="You are a grounded technical report writer.")
            section_text = self._sanitize_section_text(section_text)
            section_text = self._dedupe_sentence_level(section_text, used_sentences)
            if len(section_text.split()) < 40 and chunks:
                section_text = self._build_mock_section_from_chunks(section.title, chunks, used_sentences)
            section_text = self._sanitize_section_text(section_text)
            sections_md.extend([f"## {section.title}", section_text, ""])
            claim_map.append(ClaimMapItem(section_heading=section.title, citation_chunk_ids=chunk_ids))

        markdown = "\n".join(sections_md)
        return ReportDraft(markdown=markdown, claim_map=claim_map)

    def _build_mock_section_from_chunks(
        self,
        section_title: str,
        chunks: list[dict[str, str]],
        used_sentences: set[str],
    ) -> str:
        bullets: list[str] = []
        focus = section_title.lower()
        for chunk in chunks:
            sentence = re.split(r"(?<=[.!?])\s+", chunk["text"].strip())[0].strip()
            if not sentence:
                continue
            sentence_lower = sentence.lower()
            if "bert" in focus and "bert" not in sentence_lower:
                continue
            if "gpt overview" in focus and "gpt" not in sentence_lower:
                continue
            citation = f"[{chunk['chunk_id']}]"
            candidate = f"- {sentence} {citation}"
            normalized = re.sub(r"\s+", " ", candidate.lower()).strip()
            if normalized in used_sentences:
                continue
            used_sentences.add(normalized)
            bullets.append(candidate)
            if len(bullets) == 3:
                break
        if not bullets:
            for chunk in chunks[:2]:
                citation = f"[{chunk['chunk_id']}]"
                candidate = f"- {chunk['text'][:180].strip()}... {citation}"
                normalized = re.sub(r"\s+", " ", candidate.lower()).strip()
                if normalized in used_sentences:
                    continue
                used_sentences.add(normalized)
                bullets.append(candidate)
        return "\n".join(bullets)

    @staticmethod
    def _dedupe_sentence_level(text: str, used_sentences: set[str]) -> str:
        sentences = re.split(r"(?<=[.!?])\s+", text.strip())
        kept: list[str] = []
        for sentence in sentences:
            normalized = re.sub(r"\s+", " ", sentence.lower()).strip()
            if not normalized or normalized in used_sentences:
                continue
            used_sentences.add(normalized)
            kept.append(sentence)
        return " ".join(kept).strip()

    @staticmethod
    def _sanitize_section_text(text: str) -> str:
        cleaned_lines: list[str] = []
        blocked_prefixes = (
            "import ",
            "from ",
            "def ",
            "class ",
            "print(",
            "debug:",
            "note:",
            "implementation:",
            "internal:",
            "traceback",
        )
        for raw_line in text.splitlines():
            line = raw_line.strip()
            if not line:
                continue
            if line.startswith("```"):
                continue
            lowered = line.lower()
            if any(lowered.startswith(prefix) for prefix in blocked_prefixes):
                continue
            if "python" in lowered and ("import " in lowered or "def " in lowered):
                continue
            cleaned_lines.append(line)
        cleaned = "\n".join(cleaned_lines).strip()
        return cleaned if cleaned else "No reliable content generated for this section."
