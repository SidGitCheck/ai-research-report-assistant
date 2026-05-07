from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class SqliteCatalog:
    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_tables()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_tables(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS runs (
                    run_id TEXT PRIMARY KEY,
                    topic TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS sources (
                    source_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    run_id TEXT NOT NULL,
                    url TEXT NOT NULL,
                    title TEXT NOT NULL,
                    publisher TEXT,
                    retrieved_at TEXT NOT NULL
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS chunks (
                    chunk_id TEXT PRIMARY KEY,
                    run_id TEXT NOT NULL,
                    source_url TEXT NOT NULL,
                    source_title TEXT NOT NULL,
                    text TEXT NOT NULL,
                    chunk_hash TEXT NOT NULL UNIQUE
                )
                """
            )

    def create_run(self, run_id: str, topic: str) -> None:
        now = datetime.now(timezone.utc).isoformat()
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO runs(run_id, topic, created_at) VALUES(?,?,?)",
                (run_id, topic, now),
            )

    def add_source(self, run_id: str, url: str, title: str, publisher: str = "") -> None:
        now = datetime.now(timezone.utc).isoformat()
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO sources(run_id, url, title, publisher, retrieved_at)
                VALUES(?,?,?,?,?)
                """,
                (run_id, url, title, publisher, now),
            )

    def add_chunk(
        self,
        run_id: str,
        chunk_id: str,
        source_url: str,
        source_title: str,
        text: str,
        chunk_hash: str,
    ) -> bool:
        with self._connect() as conn:
            try:
                conn.execute(
                    """
                    INSERT INTO chunks(chunk_id, run_id, source_url, source_title, text, chunk_hash)
                    VALUES(?,?,?,?,?,?)
                    """,
                    (chunk_id, run_id, source_url, source_title, text, chunk_hash),
                )
                return True
            except sqlite3.IntegrityError:
                return False

    def get_chunks_by_ids(self, chunk_ids: list[str]) -> list[dict[str, Any]]:
        if not chunk_ids:
            return []
        placeholders = ",".join(["?"] * len(chunk_ids))
        with self._connect() as conn:
            rows = conn.execute(
                f"SELECT * FROM chunks WHERE chunk_id IN ({placeholders})",  # noqa: S608
                chunk_ids,
            ).fetchall()
        return [dict(row) for row in rows]

    def get_sources_by_run(self, run_id: str) -> list[dict[str, Any]]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT DISTINCT title, url, publisher, retrieved_at FROM sources WHERE run_id = ?",
                (run_id,),
            ).fetchall()
        return [dict(row) for row in rows]
