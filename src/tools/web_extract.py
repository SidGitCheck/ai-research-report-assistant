from __future__ import annotations

from bs4 import BeautifulSoup


def extract_main_text(html: str, max_chars: int = 20000) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript", "header", "footer", "nav"]):
        tag.decompose()
    text = soup.get_text(separator=" ", strip=True)
    return text[:max_chars]
