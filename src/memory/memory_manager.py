from __future__ import annotations

from src.memory.chroma_store import ChromaStore
from src.memory.sqlite_catalog import SqliteCatalog


class MemoryManager:
    def __init__(self, sqlite_catalog: SqliteCatalog, chroma_store: ChromaStore) -> None:
        self.sqlite_catalog = sqlite_catalog
        self.chroma_store = chroma_store

    def add_source(self, run_id: str, url: str, title: str, publisher: str = "") -> None:
        self.sqlite_catalog.add_source(run_id=run_id, url=url, title=title, publisher=publisher)

    def add_chunk(
        self,
        run_id: str,
        chunk_id: str,
        source_url: str,
        source_title: str,
        text: str,
        chunk_hash: str,
    ) -> bool:
        inserted = self.sqlite_catalog.add_chunk(
            run_id=run_id,
            chunk_id=chunk_id,
            source_url=source_url,
            source_title=source_title,
            text=text,
            chunk_hash=chunk_hash,
        )
        if inserted:
            self.chroma_store.add_chunks(
                chunk_ids=[chunk_id],
                texts=[text],
                metadatas=[
                    {
                        "run_id": run_id,
                        "source_url": source_url,
                        "source_title": source_title,
                    }
                ],
            )
        return inserted

    def retrieve_chunk_ids(self, run_id: str, query_text: str, n_results: int = 5) -> list[str]:
        return self.chroma_store.query(query_text=query_text, n_results=n_results, where={"run_id": run_id})
