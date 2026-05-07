from __future__ import annotations

import time
from collections.abc import Callable
from typing import TypeVar


T = TypeVar("T")


def retry(operation: Callable[[], T], attempts: int = 3, backoff_seconds: float = 0.5) -> T:
    last_error: Exception | None = None
    for i in range(attempts):
        try:
            return operation()
        except Exception as exc:  # noqa: BLE001
            last_error = exc
            if i < attempts - 1:
                time.sleep(backoff_seconds * (2**i))
    assert last_error is not None
    raise last_error
