from __future__ import annotations

import optuna

from .data_fetcher import fetch_klines
from .backtest import backtest_strategy
from .logger import get_logger

logger = get_logger(__name__)


def optuna_optimize(symbol: str, trials: int = 20) -> tuple[int, int, float]:
    """Optimize RSI thresholds for ``symbol`` using Optuna."""
    df = fetch_klines(symbol, interval="1h", limit=500)
    if df.empty:
        raise ValueError("no data for optimization")

    def objective(trial: optuna.Trial) -> float:
        buy_th = trial.suggest_int("buy_th", 10, 50)
        sell_th = trial.suggest_int("sell_th", 50, 90)
        pnl = backtest_strategy(
            df, rsi_buy_threshold=buy_th, rsi_sell_threshold=sell_th
        )
        return -pnl

    study = optuna.create_study()
    study.optimize(objective, n_trials=trials)
    best_buy = study.best_params["buy_th"]
    best_sell = study.best_params["sell_th"]
    best_pnl = -study.best_value
    logger.info(
        "Optuna best params: Buy=%s Sell=%s PnL=%.2f",
        best_buy,
        best_sell,
        best_pnl,
    )
    return best_buy, best_sell, best_pnl
