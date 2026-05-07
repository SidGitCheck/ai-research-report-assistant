from __future__ import annotations

from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


class ChromaStore:
    def __init__(self, persist_directory: Path, embedding_model: str, collection_name: str = "chunks") -> None:
        self.client = chromadb.PersistentClient(path=str(persist_directory))
        self.collection = self.client.get_or_create_collection(name=collection_name)
        self.embedder = SentenceTransformer(embedding_model)

    def add_chunks(
        self,
        chunk_ids: list[str],
        texts: list[str],
        metadatas: list[dict[str, str]],
    ) -> None:
        if not chunk_ids:
            return
        embeddings = self.embedder.encode(texts).tolist()
        self.collection.add(
            ids=chunk_ids,
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas,
        )

    def query(self, query_text: str, n_results: int = 5, where: dict | None = None) -> list[str]:
        query_embedding = self.embedder.encode([query_text]).tolist()
        result = self.collection.query(
            query_embeddings=query_embedding,
            n_results=n_results,
            where=where,
        )
        ids = result.get("ids", [[]])[0]
        return ids
