from __future__ import annotations

from pydantic import BaseModel


class Source(BaseModel):
    url: str
    title: str
    publisher: str = ""
    retrieved_at: str
