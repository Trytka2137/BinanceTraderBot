import json
import os
import sys

import numpy as np

from .data_fetcher import fetch_klines
from .backtest import backtest_strategy

STATE_PATH = os.path.join(os.path.dirname(__file__), 'model_state.json')

DEFAULT_BUY = 30
DEFAULT_SELL = 70


def load_state():
    if os.path.exists(STATE_PATH):
        with open(STATE_PATH, 'r') as f:
            data = json.load(f)
            return (
                data.get('buy', DEFAULT_BUY),
                data.get('sell', DEFAULT_SELL),
                data.get('pnl', -np.inf),
            )
    return DEFAULT_BUY, DEFAULT_SELL, -np.inf


def save_state(buy, sell, pnl):
    with open(STATE_PATH, 'w') as f:
        json.dump({'buy': buy, 'sell': sell, 'pnl': pnl}, f)


def optimize(symbol, iterations=20):
    df = fetch_klines(symbol, interval='1h', limit=500)
    if df.empty:
        print('Brak danych do optymalizacji')
        return DEFAULT_BUY, DEFAULT_SELL, -np.inf

    best_buy, best_sell, best_pnl = load_state()

    for _ in range(iterations):
        buy_th = int(np.clip(np.random.normal(best_buy, 5), 10, 50))
        sell_th = int(np.clip(np.random.normal(best_sell, 5), 50, 90))
        pnl = backtest_strategy(
            df,
            rsi_buy_threshold=buy_th,
            rsi_sell_threshold=sell_th,
        )
        print(f'Test: Buy={buy_th}, Sell={sell_th} => PnL={pnl}')
        if pnl > best_pnl:
            best_pnl = pnl
            best_buy = buy_th
            best_sell = sell_th

    save_state(best_buy, best_sell, best_pnl)
    print(
        f'Najlepsze parametry: Buy={best_buy} '
        f'Sell={best_sell} PnL={best_pnl}'
    )
    return best_buy, best_sell, best_pnl


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Użycie: python auto_optimizer.py SYMBOL')
        sys.exit(1)
    symbol = sys.argv[1]
    optimize(symbol)
