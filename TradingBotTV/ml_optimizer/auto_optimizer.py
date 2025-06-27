from dataclasses import dataclass
from pathlib import Path

import numpy as np

from .data_fetcher import fetch_klines
from .backtest import backtest_strategy
from .logger import get_logger
from .monitor import record_metric
from .state_utils import (
    load_state as load_json_state,
    save_state as save_json_state,
)

logger = get_logger(__name__)

STATE_DIR = Path(__file__).resolve().parent / "state"
STATE_PATH = STATE_DIR / "model_state.json"

DEFAULT_BUY = 30
DEFAULT_SELL = 70


@dataclass
class OptimizerState:
    """Stored optimizer parameters."""

    buy: int = DEFAULT_BUY
    sell: int = DEFAULT_SELL
    pnl: float = -np.inf


def load_state() -> OptimizerState:
    """Return stored optimization parameters."""
    STATE_DIR.mkdir(exist_ok=True)
    return load_json_state(STATE_PATH, OptimizerState)


def save_state(state: OptimizerState) -> None:
    """Persist ``state`` to :data:`STATE_PATH`."""
    STATE_DIR.mkdir(exist_ok=True)
    save_json_state(STATE_PATH, state)


def optimize(symbol: str, iterations: int = 20) -> tuple[int, int, float]:
    """Optimize RSI thresholds for ``symbol`` over ``iterations`` runs."""

    df = fetch_klines(symbol, interval="1h", limit=500)
    if df.empty:
        logger.warning("Brak danych do optymalizacji")
        return DEFAULT_BUY, DEFAULT_SELL, -np.inf

    state = load_state()
    best_buy, best_sell, best_pnl = state.buy, state.sell, state.pnl

    for _ in range(iterations):
        buy_th = int(np.clip(np.random.normal(best_buy, 5), 10, 50))
        sell_th = int(np.clip(np.random.normal(best_sell, 5), 50, 90))
        pnl = backtest_strategy(
            df,
            rsi_buy_threshold=buy_th,
            rsi_sell_threshold=sell_th,
        )
        logger.info("Test: Buy=%s Sell=%s => PnL=%s", buy_th, sell_th, pnl)
        if pnl > best_pnl:
            best_pnl = pnl
            best_buy = buy_th
            best_sell = sell_th

    save_state(OptimizerState(best_buy, best_sell, best_pnl))
    logger.info(
        "Najlepsze parametry: Buy=%s Sell=%s PnL=%s",
        best_buy,
        best_sell,
        best_pnl,
    )
    record_metric("optimizer_pnl", best_pnl)
    return best_buy, best_sell, best_pnl


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Optimize RSI thresholds')
    parser.add_argument('symbol', help='Trading symbol')
    parser.add_argument(
        '--iterations',
        type=int,
        default=20,
        help='Number of tests',
    )
    parser.add_argument(
        '--log-level',
        default='INFO',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        help='Logging verbosity',
    )
    args = parser.parse_args()

    logger.setLevel(args.log_level)

    optimize(args.symbol, iterations=args.iterations)
