from __future__ import annotations

from src.memory.memory_manager import MemoryManager


def retrieve_context(memory: MemoryManager, run_id: str, query: str, k: int = 5) -> list[str]:
    return memory.retrieve_chunk_ids(run_id=run_id, query_text=query, n_results=k)
