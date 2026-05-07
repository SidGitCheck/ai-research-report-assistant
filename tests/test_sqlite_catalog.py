from pathlib import Path

from src.memory.sqlite_catalog import SqliteCatalog


def test_chunk_deduplication(tmp_path: Path) -> None:
    db = SqliteCatalog(tmp_path / "catalog.db")
    db.create_run("run1", "topic")
    inserted_first = db.add_chunk("run1", "c1", "https://a", "A", "text", "hash1")
    inserted_second = db.add_chunk("run1", "c2", "https://a", "A", "text", "hash1")
    assert inserted_first is True
    assert inserted_second is False
