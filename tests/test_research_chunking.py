from src.agents.research_agent import _chunk_text


def test_chunk_text_creates_multiple_chunks() -> None:
    text = "a" * 2000
    chunks = _chunk_text(text, chunk_size=500, overlap=100)
    assert len(chunks) >= 4
