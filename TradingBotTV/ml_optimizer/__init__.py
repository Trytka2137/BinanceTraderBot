"""Utility exports for the :mod:`TradingBotTV.ml_optimizer` package."""

from .backtest import (
    backtest_macd_strategy,
    backtest_strategy,
    compare_strategies,
    compute_macd,
    compute_atr,
    compute_ema,
    compute_sma,
    compute_rsi,
)
from .data_fetcher import (
    fetch_klines,
    async_fetch_klines,
    fetch_coingecko_market_chart,
)
from .github_strategy_simulator import simulate_strategy
from .risk import kelly_fraction, value_at_risk
from .fundamental import (
    fetch_coinmarketcap_data,
    fetch_coingecko_market_data,
    fetch_messari_asset_metrics,
    fetch_github_activity,
)
from .analytics import (
    bollinger_bands,
    stochastic_oscillator,
    order_book_imbalance,
)
from .ml_models import (
    train_predictive_model,
    optimize_predictive_model,
    backtest_tick_strategy,
    train_deep_learning_model,
)
from .portfolio import allocate_equal_weight, calculate_position_sizes
from .orderbook import best_bid_ask, compute_order_flow_imbalance
from .hedging import hedge_ratio
from .arbitrage import price_spread
from .logger import get_logger
from .monitor import record_metric
from .network_utils import check_connectivity, async_check_connectivity
from .execution import twap_order, vwap_order
from .hft import midprice, generate_hft_signal
from .options import black_scholes_price, straddle_strategy

__all__ = [
    "compute_rsi",
    "compute_macd",
    "compute_ema",
    "compute_sma",
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
    "fetch_coingecko_market_chart",
    "kelly_fraction",
    "value_at_risk",
    "fetch_coinmarketcap_data",
    "fetch_coingecko_market_data",
    "fetch_messari_asset_metrics",
    "fetch_github_activity",
    "bollinger_bands",
    "stochastic_oscillator",
    "order_book_imbalance",
    "train_predictive_model",
    "optimize_predictive_model",
    "backtest_tick_strategy",
    "train_deep_learning_model",
    "allocate_equal_weight",
    "calculate_position_sizes",
    "best_bid_ask",
    "compute_order_flow_imbalance",
    "hedge_ratio",
    "price_spread",
    "twap_order",
    "vwap_order",
    "midprice",
    "generate_hft_signal",
    "black_scholes_price",
    "straddle_strategy",
]
