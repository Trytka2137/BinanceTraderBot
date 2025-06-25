"""Utility exports for the :mod:`TradingBotTV.ml_optimizer` package."""

from .backtest import (
    backtest_macd_strategy,
    backtest_strategy,
    compare_strategies,
    compute_macd,
    compute_rsi,
)
from .data_fetcher import fetch_klines
from .github_strategy_simulator import simulate_strategy

__all__ = [
    "compute_rsi",
    "compute_macd",
    "backtest_strategy",
    "backtest_macd_strategy",
    "compare_strategies",
    "fetch_klines",
    "simulate_strategy",
]
