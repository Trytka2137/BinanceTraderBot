import sys

import numpy as np

from .data_fetcher import fetch_klines
from .backtest import backtest_strategy
from .logger import get_logger


logger = get_logger(__name__)


def optimize(symbol: str):
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
            logger.info(
                "Test: Buy=%s, Sell=%s => PnL=%s",
                buy_th,
                sell_th,
                pnl,
            )
            if pnl > best_pnl:
                best_pnl = pnl
                best_params = (buy_th, sell_th)

    logger.info(
        "Najlepsze parametry: Buy=%s Sell=%s PnL=%s",
        best_params[0],
        best_params[1],
        best_pnl,
    )
    return best_params


if __name__ == "__main__":
    if len(sys.argv) < 2:
        logger.error("Użycie: python optimizer.py SYMBOL")
        sys.exit(1)
    symbol = sys.argv[1]
    optimize(symbol)
