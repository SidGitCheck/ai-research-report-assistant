from __future__ import annotations

import requests

from src.utils.retry import retry


def fetch_url(url: str, timeout_seconds: int = 15) -> str:
    def _op() -> str:
        response = requests.get(
            url,
            timeout=timeout_seconds,
            headers={"User-Agent": "Mozilla/5.0 (compatible; MAIRA/0.1)"},
        )
        response.raise_for_status()
        return response.text

    return retry(_op, attempts=3)
