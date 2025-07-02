"""High-level AI utilities combining multiple modules."""

from __future__ import annotations

from typing import Iterable, Any, Dict

from .advanced_rl import LSTMTrendModel
from .compare_strategies import auto_select_best_strategy
from .data_fetcher import fetch_klines
from .sentiment import text_sentiment
from .fundamental import fetch_github_activity


def generate_expert_report(
    symbol: str, posts: Iterable[str], repo: str, splits: int = 3
) -> Dict[str, Any]:
    """Return strategy suggestion and indicators for ``symbol``.

    Parameters
    ----------
    symbol:
        Trading pair symbol.
    posts:
        Recent social media posts used for sentiment analysis.
    repo:
        GitHub repository in ``owner/name`` format for activity stats.
    splits:
        Number of splits for cross-validation when selecting strategy.
    """
    df = fetch_klines(symbol, interval="1h", limit=200)
    if df.empty:
        raise ValueError("no market data")

    strategy = auto_select_best_strategy(symbol, splits=splits)

    closes = df["close"].astype(float)
    model = LSTMTrendModel.create(window=5)
    model.fit(closes, epochs=1)
    next_price = model.predict_next(closes.iloc[-5:])
    last_close = float(closes.iloc[-1])
    signal = "BUY" if next_price > last_close else "SELL"

    sentiment_score = text_sentiment(posts)
    github_stats = fetch_github_activity(repo)

    return {
        "strategy": strategy,
        "signal": signal,
        "sentiment": sentiment_score,
        "github_stars": github_stats.get("stars", 0),
    }
