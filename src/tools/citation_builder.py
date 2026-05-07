from __future__ import annotations


def build_citation_token(chunk_id: str) -> str:
    return f"[{chunk_id}]"
