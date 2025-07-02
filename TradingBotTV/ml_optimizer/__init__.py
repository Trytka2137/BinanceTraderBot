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
from .compare_strategies import (
    auto_select_best_strategy,
    should_switch_strategy,
)
from .data_fetcher import (
    fetch_klines,
    async_fetch_klines,
    fetch_coingecko_market_chart,
)
from .github_strategy_simulator import simulate_strategy
from .risk import (
    kelly_fraction,
    value_at_risk,
    adaptive_stop_levels,
    max_drawdown,
    position_size_from_var,
    decide_investment_budget,
)
from .fundamental import (
    fetch_coinmarketcap_data,
    fetch_coingecko_market_data,
    fetch_messari_asset_metrics,
    fetch_github_activity,
    cache_fundamental_data,
    cache_fundamental_data_regularly,
)
from .expert_ai import generate_expert_report
from .analytics import (
    bollinger_bands,
    stochastic_oscillator,
    order_book_imbalance,
    detect_price_anomalies,
    autoencoder_anomaly_scores,
)
from .auto_ml import optuna_optimize
from .ml_models import (
    train_predictive_model,
    optimize_predictive_model,
    backtest_tick_strategy,
    train_deep_learning_model,
)
from .portfolio import (
    allocate_equal_weight,
    calculate_position_sizes,
    risk_parity_weights,
)
from .order_manager import limit_price_from_spread, adjust_order_price
from .orderbook import best_bid_ask, compute_order_flow_imbalance
from .hedging import hedge_ratio
from .arbitrage import price_spread
from .sentiment import fetch_political_crypto_hashtags
from .strategies import (
    grid_levels,
    dca_schedule,
    scalp_signal,
    choose_strategy,
)
from .logger import get_logger
from .monitor import record_metric
from .network_utils import check_connectivity, async_check_connectivity
from .execution import twap_order, vwap_order
from .hft import (
    midprice,
    generate_hft_signal,
    measure_latency,
    monitor_latency,
    fast_market_order,
)
from .options import black_scholes_price, straddle_strategy, option_greeks
from .visualizer import (
    plot_metrics,
    plot_performance_and_risk,
    plot_risk_indicators,
)
from .deep_rl_examples import deep_q_learning_example, policy_gradient_example
from .deep_rl_examples import online_q_learning
from .websocket_orderbook import stream_order_book
from .database import (
    init_db,
    store_trade,
    store_metric,
    fetch_trades,
    fetch_metrics,
)
from .web_panel import run_dashboard
from .signal_handler import parse_tradingview_payload, execute_strategies
from .alerts import send_discord_message

__all__ = [
    "compute_rsi",
    "compute_macd",
    "compute_ema",
    "compute_sma",
    "compute_atr",
    "backtest_strategy",
    "backtest_macd_strategy",
    "compare_strategies",
    "auto_select_best_strategy",
    "should_switch_strategy",
    "optuna_optimize",
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
    "detect_price_anomalies",
    "autoencoder_anomaly_scores",
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
    "measure_latency",
    "monitor_latency",
    "fast_market_order",
    "black_scholes_price",
    "straddle_strategy",
    "option_greeks",
    "risk_parity_weights",
    "plot_metrics",
    "plot_performance_and_risk",
    "plot_risk_indicators",
    "stream_order_book",
    "init_db",
    "store_trade",
    "store_metric",
    "fetch_trades",
    "fetch_metrics",
    "run_dashboard",
    "parse_tradingview_payload",
    "execute_strategies",
    "send_discord_message",
    "adaptive_stop_levels",
    "cache_fundamental_data",
    "cache_fundamental_data_regularly",
    "max_drawdown",
    "deep_q_learning_example",
    "policy_gradient_example",
    "online_q_learning",
    "position_size_from_var",
    "decide_investment_budget",
    "limit_price_from_spread",
    "adjust_order_price",
    "grid_levels",
    "dca_schedule",
    "scalp_signal",
    "choose_strategy",
    "choose_strategy",
    "fetch_political_crypto_hashtags",
    "generate_expert_report",
  
  
]
