from __future__ import annotations

from pydantic import BaseModel, Field


class ReviewIssue(BaseModel):
    severity: str
    category: str
    evidence: str


class ReviewResult(BaseModel):
    issues: list[ReviewIssue] = Field(default_factory=list)
    recommended_actions: list[str] = Field(default_factory=list)
    needs_regeneration: bool = False
