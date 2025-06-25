"""Simple reinforcement learning optimizer for RSI thresholds."""

import json
import random

import numpy as np

from .data_fetcher import fetch_klines
from .backtest import backtest_strategy

STATE_PATH = 'rl_state.json'

# Search space for RSI thresholds
BUY_SPACE = list(range(20, 41, 2))
SELL_SPACE = list(range(60, 81, 2))

def load_state():
    try:
        with open(STATE_PATH, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_state(state):
    with open(STATE_PATH, 'w') as f:
        json.dump(state, f)

def train(symbol, episodes=30, population=20, elite_frac=0.2, seed=None):
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

    mean_buy = state.get('mean_buy', 30.0)
    std_buy = state.get('std_buy', 5.0)
    mean_sell = state.get('mean_sell', 70.0)
    std_sell = state.get('std_sell', 5.0)

    df = fetch_klines(symbol, interval='1h', limit=500)
    if df.empty:
        print('No data fetched – aborting training')
        return int(round(mean_buy)), int(round(mean_sell))

    for _ in range(episodes):
        buys = np.random.normal(mean_buy, std_buy, population).astype(int)
        sells = np.random.normal(mean_sell, std_sell, population).astype(int)
        results = []
        for b, s in zip(buys, sells):
            b = int(np.clip(b, 20, 40))
            s = int(np.clip(s, 60, 80))
            pnl = backtest_strategy(df, rsi_buy_threshold=b, rsi_sell_threshold=s)
            results.append((pnl, b, s))
        results.sort(reverse=True)
        elite = results[: max(1, int(population * elite_frac))]
        mean_buy = np.mean([b for _, b, _ in elite])
        std_buy = np.std([b for _, b, _ in elite]) + 1e-6
        mean_sell = np.mean([s for _, _, s in elite])
        std_sell = np.std([s for _, _, s in elite]) + 1e-6

    best_buy = int(round(mean_buy))
    best_sell = int(round(mean_sell))
    save_state({
        'mean_buy': mean_buy,
        'std_buy': std_buy,
        'mean_sell': mean_sell,
        'std_sell': std_sell,
        'best_buy': best_buy,
        'best_sell': best_sell,
    })
    print(f'Best params: {best_buy} {best_sell}')
    return best_buy, best_sell

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print('Usage: python rl_optimizer.py SYMBOL')
        sys.exit(1)
    train(sys.argv[1])
