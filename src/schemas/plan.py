from __future__ import annotations

from pydantic import BaseModel, Field


class PlanSection(BaseModel):
    title: str
    query_strategy: list[str] = Field(default_factory=list)
    required_sources: int = 2


class RetrievalBudget(BaseModel):
    max_sources: int = 8
    max_chunks_total: int = 30


class Plan(BaseModel):
    topic: str
    sections: list[PlanSection]
    retrieval_budget: RetrievalBudget = RetrievalBudget()
    evaluation_rubric: list[str] = Field(default_factory=list)
