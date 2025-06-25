import sys

from .data_fetcher import fetch_klines
from .backtest import backtest_strategy
import numpy as np


def optimize(symbol):
    df = fetch_klines(symbol, interval='1h', limit=500)
    best_pnl = -np.inf
    best_params = None

    for buy_th in range(20, 40, 5):
        for sell_th in range(60, 80, 5):
            pnl = backtest_strategy(
                df,
                rsi_buy_threshold=buy_th,
                rsi_sell_threshold=sell_th,
            )
            print(f"Test: Buy={buy_th}, Sell={sell_th} => PnL={pnl}")
            if pnl > best_pnl:
                best_pnl = pnl
                best_params = (buy_th, sell_th)

    print(
        f"Najlepsze parametry: Buy={best_params[0]} "
        f"Sell={best_params[1]} PnL={best_pnl}"
    )
    return best_params


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Użycie: python optimizer.py SYMBOL")
        sys.exit(1)
    symbol = sys.argv[1]
    optimize(symbol)
