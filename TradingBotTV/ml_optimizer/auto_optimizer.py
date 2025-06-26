<<<<<<< i6574t-codex/szukaj-błędów-i-optymalizuj-kod
import sys
from dataclasses import dataclass
=======
<<<<<<< 5m564b-codex/szukaj-błędów-i-optymalizuj-kod
import sys
from dataclasses import dataclass
=======

import sys
from dataclasses import dataclass
import json
import sys
from dataclasses import asdict, dataclass

>>>>>>> BOT
>>>>>>> BOT
from pathlib import Path

import numpy as np

from .data_fetcher import fetch_klines
from .backtest import backtest_strategy
from .logger import get_logger
from .state_utils import (
    load_state as load_json_state,
    save_state as save_json_state,
)
<<<<<<< i6574t-codex/szukaj-błędów-i-optymalizuj-kod

logger = get_logger(__name__)

=======
<<<<<<< 5m564b-codex/szukaj-błędów-i-optymalizuj-kod

logger = get_logger(__name__)

=======


logger = get_logger(__name__)

>>>>>>> BOT
>>>>>>> BOT
STATE_PATH = Path(__file__).with_name("model_state.json")

DEFAULT_BUY = 30
DEFAULT_SELL = 70


@dataclass
class OptimizerState:
    """Stored optimizer parameters."""

<<<<<<< i6574t-codex/szukaj-błędów-i-optymalizuj-kod
=======
<<<<<<< 5m564b-codex/szukaj-błędów-i-optymalizuj-kod
=======

>>>>>>> BOT
>>>>>>> BOT
    buy: int = DEFAULT_BUY
    sell: int = DEFAULT_SELL
    pnl: float = -np.inf


def load_state() -> OptimizerState:
    """Return stored optimization parameters."""
    return load_json_state(STATE_PATH, OptimizerState)
<<<<<<< i6574t-codex/szukaj-błędów-i-optymalizuj-kod
=======
<<<<<<< 5m564b-codex/szukaj-błędów-i-optymalizuj-kod
=======
>>>>>>> BOT

>>>>>>> BOT

<<<<<<< i6574t-codex/szukaj-błędów-i-optymalizuj-kod
def save_state(state: OptimizerState) -> None:
    """Persist ``state`` to :data:`STATE_PATH`."""
    save_json_state(STATE_PATH, state)
=======
    buy: int = DEFAULT_BUY
    sell: int = DEFAULT_SELL
    pnl: float = -np.inf


def save_state(state: OptimizerState) -> None:
    """Persist ``state`` to :data:`STATE_PATH`."""
    save_json_state(STATE_PATH, state)


def load_state() -> OptimizerState:
    """Return stored optimization parameters."""
    if STATE_PATH.exists():
        data = json.loads(STATE_PATH.read_text())
        return OptimizerState(
            buy=int(data.get("buy", DEFAULT_BUY)),
            sell=int(data.get("sell", DEFAULT_SELL)),
            pnl=float(data.get("pnl", -np.inf)),
        )
    return OptimizerState()


def save_state(state: OptimizerState) -> None:
    """Persist ``state`` to :data:`STATE_PATH`."""
    STATE_PATH.write_text(json.dumps(asdict(state)))

<<<<<<< 5m564b-codex/szukaj-błędów-i-optymalizuj-kod
def save_state(state: OptimizerState) -> None:
    """Persist ``state`` to :data:`STATE_PATH`."""
    save_json_state(STATE_PATH, state)
=======
>>>>>>> BOT
>>>>>>> BOT


def optimize(symbol, iterations=20):
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
<<<<<<< i6574t-codex/szukaj-błędów-i-optymalizuj-kod
=======
<<<<<<< 5m564b-codex/szukaj-błędów-i-optymalizuj-kod
=======

>>>>>>> BOT
>>>>>>> BOT
    logger.info(
        "Najlepsze parametry: Buy=%s Sell=%s PnL=%s",
        best_buy,
        best_sell,
        best_pnl,
<<<<<<< i6574t-codex/szukaj-błędów-i-optymalizuj-kod
=======
<<<<<<< 5m564b-codex/szukaj-błędów-i-optymalizuj-kod
=======

    print(
        f'Najlepsze parametry: Buy={best_buy} '
        f'Sell={best_sell} PnL={best_pnl}'

>>>>>>> BOT
>>>>>>> BOT
    )
    return best_buy, best_sell, best_pnl


if __name__ == '__main__':
    if len(sys.argv) < 2:
        logger.error('Użycie: python auto_optimizer.py SYMBOL')
        sys.exit(1)
    symbol = sys.argv[1]
    optimize(symbol)
