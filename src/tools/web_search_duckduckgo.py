from __future__ import annotations

from urllib.parse import parse_qs, quote_plus, unquote, urlparse

import requests
from bs4 import BeautifulSoup

from src.utils.retry import retry


def _normalize_duckduckgo_href(href: str) -> str:
    if not href:
        return ""
    # DuckDuckGo often wraps outbound links as /l/?uddg=<encoded_url>
    if "duckduckgo.com/l/?" in href or href.startswith("/l/?"):
        parsed = urlparse(href)
        query = parse_qs(parsed.query)
        uddg_values = query.get("uddg", [])
        if uddg_values:
            return unquote(uddg_values[0])
    return href


def search_duckduckgo(query: str, max_results: int = 5, timeout_seconds: int = 15) -> list[dict[str, str]]:
    def _op() -> list[dict[str, str]]:
        url = f"https://duckduckgo.com/html/?q={quote_plus(query)}"
        response = requests.get(
            url,
            timeout=timeout_seconds,
            headers={"User-Agent": "Mozilla/5.0 (compatible; MAIRA/0.1)"},
        )
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        results: list[dict[str, str]] = []
        seen_urls: set[str] = set()
        for result in soup.select(".result"):
            link = result.select_one(".result__a")
            if not link:
                continue
            href = _normalize_duckduckgo_href(link.get("href", ""))
            title = link.get_text(" ", strip=True)
            if not href.startswith("http"):
                continue
            if href in seen_urls:
                continue
            seen_urls.add(href)
            if href and title:
                results.append({"url": href, "title": title})
            if len(results) >= max_results:
                break
        return results

    return retry(_op, attempts=3)
