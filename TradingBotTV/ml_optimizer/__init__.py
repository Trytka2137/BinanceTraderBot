"""Utility exports for the :mod:`TradingBotTV.ml_optimizer` package."""

from .backtest import (
    backtest_macd_strategy,
    backtest_strategy,
    compare_strategies,
    compute_macd,
    compute_atr,
    compute_ema,
    compute_rsi,
)
from .data_fetcher import fetch_klines, async_fetch_klines
from .github_strategy_simulator import simulate_strategy
from .tradingview_auto_trader import (
    auto_trade_from_tv,
    async_auto_trade_from_tv,
)
from .logger import get_logger
from .monitor import record_metric
from .network_utils import (
    check_connectivity,
    async_check_connectivity,
)
from .network_utils import check_connectivity

__all__ = [
    "compute_rsi",
    "compute_macd",
    "compute_ema",
    "compute_atr",
    "backtest_strategy",
    "backtest_macd_strategy",
    "compare_strategies",
    "fetch_klines",
    "async_fetch_klines",
    "get_logger",
    "record_metric",
    "check_connectivity",
    "async_check_connectivity",
    "simulate_strategy",
    "auto_trade_from_tv",
    "async_auto_trade_from_tv",
]
