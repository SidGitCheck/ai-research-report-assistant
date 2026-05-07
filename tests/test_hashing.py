from src.utils.hashing import stable_sha256


def test_stable_sha256_is_deterministic() -> None:
    assert stable_sha256("hello") == stable_sha256("hello")
