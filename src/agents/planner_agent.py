from __future__ import annotations

import json

from pydantic import ValidationError

from src.agents.llm_client import LLMClient
from src.schemas.plan import Plan


class PlannerAgent:
    def __init__(self, llm: LLMClient) -> None:
        self.llm = llm

    def plan(self, topic: str, max_sources: int, max_chunks: int) -> Plan:
        prompt = f"""
Return ONLY valid JSON.
Create a research plan for topic: {topic}
Constraints:
- max_sources: {max_sources}
- max_chunks_total: {max_chunks}

JSON schema:
{{
  "topic": "string",
  "sections": [{{"title":"string","query_strategy":["string"],"required_sources":2}}],
  "retrieval_budget": {{"max_sources": {max_sources}, "max_chunks_total": {max_chunks}}},
  "evaluation_rubric": ["coverage","citation_quality","clarity","correctness"]
}}
"""
        raw = self.llm.generate(prompt=prompt, system_prompt="You are a precise planning agent.")
        try:
            return Plan.model_validate_json(raw)
        except ValidationError:
            repaired = self.llm.generate(
                prompt=f"Fix this into valid JSON for the schema only:\n{raw}",
                system_prompt="You output strict JSON only.",
            )
            return Plan.model_validate_json(repaired)

    @staticmethod
    def save_plan_json(plan: Plan, path: str) -> None:
        with open(path, "w", encoding="utf-8") as file:
            json.dump(plan.model_dump(), file, indent=2)
