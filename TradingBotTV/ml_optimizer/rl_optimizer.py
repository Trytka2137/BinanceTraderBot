"""Simple reinforcement learning optimizer for RSI thresholds."""

import random
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from .data_fetcher import fetch_klines
from .backtest import backtest_strategy
from .logger import get_logger
from .monitor import record_metric
from .alerts import send_telegram_message
from .state_utils import (
    load_state as load_json_state,
    save_state as save_json_state,
)

logger = get_logger(__name__)

STATE_DIR = Path(__file__).resolve().parent / "state"
STATE_PATH = STATE_DIR / "rl_state.json"

# Search space for RSI thresholds
BUY_SPACE = list(range(20, 41, 2))
SELL_SPACE = list(range(60, 81, 2))


@dataclass
class RLState:
    """Internal state persisted between training runs."""

    mean_buy: float = 30.0
    std_buy: float = 5.0
    mean_sell: float = 70.0
    std_sell: float = 5.0
    best_buy: int = 30
    best_sell: int = 70


def load_state() -> RLState:
    """Load persisted :class:`RLState` from :data:`STATE_PATH`."""
    STATE_DIR.mkdir(exist_ok=True)
    return load_json_state(STATE_PATH, RLState)


def save_state(state: RLState) -> None:
    """Persist ``state`` to :data:`STATE_PATH`."""
    STATE_DIR.mkdir(exist_ok=True)
    save_json_state(STATE_PATH, state)


def train(
    symbol: str,
    episodes: int = 30,
    population: int = 20,
    elite_frac: float = 0.2,
    seed: int | None = None,
) -> tuple[int, int]:
    """Train thresholds using a simple cross-entropy method.

    Parameters
    ----------
    symbol : str
        Trading pair symbol.
    episodes : int, optional
        Number of training iterations. Default ``30``.
    population : int, optional
        Size of the sample population per iteration. Default ``20``.
    elite_frac : float, optional
        Fraction of top performing samples used to update the distribution.
        Default ``0.2``.
    seed : int, optional
        Random seed ensuring deterministic behaviour. When ``None`` a seed
        is drawn from ``random`` module's state. This makes the function
        reproducible when ``random.seed`` has been called by the caller.
    """

    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)
    else:
        np.random.seed(random.randint(0, 2**32 - 1))

    state = load_state()

    mean_buy = state.mean_buy
    std_buy = state.std_buy
    mean_sell = state.mean_sell
    std_sell = state.std_sell

    df = fetch_klines(symbol, interval="1h", limit=500)
    if df.empty:
        logger.warning('No data fetched – aborting training')
        return int(round(mean_buy)), int(round(mean_sell))

    for _ in range(episodes):
        buys = np.random.normal(mean_buy, std_buy, population).astype(int)
        sells = np.random.normal(mean_sell, std_sell, population).astype(int)
        results = []
        for b, s in zip(buys, sells):
            b = int(np.clip(b, 20, 40))
            s = int(np.clip(s, 60, 80))
            pnl = backtest_strategy(
                df,
                rsi_buy_threshold=b,
                rsi_sell_threshold=s,
            )
            results.append((pnl, b, s))
        results.sort(reverse=True)
        elite = results[: max(1, int(population * elite_frac))]
        mean_buy = np.mean([b for _, b, _ in elite])
        std_buy = np.std([b for _, b, _ in elite]) + 1e-6
        mean_sell = np.mean([s for _, _, s in elite])
        std_sell = np.std([s for _, _, s in elite]) + 1e-6

    best_buy = int(round(mean_buy))
    best_sell = int(round(mean_sell))
    save_state(
        RLState(
            mean_buy=mean_buy,
            std_buy=std_buy,
            mean_sell=mean_sell,
            std_sell=std_sell,
            best_buy=best_buy,
            best_sell=best_sell,
        )
    )
    logger.info('Best params: %s %s', best_buy, best_sell)
    record_metric('rl_optimizer_buy', best_buy)
    record_metric('rl_optimizer_sell', best_sell)
    try:
        send_telegram_message(
            f"RL optimizer params: Buy={best_buy} Sell={best_sell}"
        )
    except Exception:
        pass
    return best_buy, best_sell


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Reinforcement optimizer')
    parser.add_argument('symbol', help='Trading symbol')
    parser.add_argument('--episodes', type=int, default=30)
    parser.add_argument('--population', type=int, default=20)
    parser.add_argument('--elite-frac', type=float, default=0.2)
    parser.add_argument(
        '--log-level',
        default='INFO',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
    )
    args = parser.parse_args()

    logger.setLevel(args.log_level)

    train(
        args.symbol,
        episodes=args.episodes,
        population=args.population,
        elite_frac=args.elite_frac,
    )
