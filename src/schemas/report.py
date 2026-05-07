from __future__ import annotations

from pydantic import BaseModel, Field


class ClaimMapItem(BaseModel):
    section_heading: str
    citation_chunk_ids: list[str] = Field(default_factory=list)


class ReportDraft(BaseModel):
    markdown: str
    claim_map: list[ClaimMapItem] = Field(default_factory=list)
