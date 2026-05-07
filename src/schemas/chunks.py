from __future__ import annotations

from pydantic import BaseModel


class Chunk(BaseModel):
    chunk_id: str
    source_url: str
    source_title: str
    text: str
    chunk_hash: str
