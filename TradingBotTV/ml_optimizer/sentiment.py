from collections import Counter
from typing import Iterable
import os
import requests


POSITIVE_WORDS = {"good", "great", "positive", "bull", "up"}
NEGATIVE_WORDS = {"bad", "negative", "bear", "down", "fear"}


def text_sentiment(texts: Iterable[str]) -> float:
    """Return naive sentiment score in range [-1, 1]."""
    counts = Counter()
    for t in texts:
        words = {w.lower().strip('.,!') for w in t.split()}
        counts.update(words)
    pos = sum(counts[w] for w in POSITIVE_WORDS)
    neg = sum(counts[w] for w in NEGATIVE_WORDS)
    total = pos + neg
    if total == 0:
        return 0.0
    return (pos - neg) / total


def fetch_fear_greed_index() -> int:
    """Return the current value of the Crypto Fear & Greed Index."""
    url = "https://api.alternative.me/fng/"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()
    return int(data["data"][0]["value"])


def fetch_lunarcrush_score(symbol: str, api_key: str | None = None) -> float:
    """Return LunarCrush galaxy score for ``symbol``."""
    api_key = api_key or os.getenv("LUNARCRUSH_API_KEY", "")
    params = {"data": "galaxyScore", "symbol": symbol, "key": api_key}
    url = "https://lunarcrush.com/api3"
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    return float(data["data"][0]["galaxy_score"])
