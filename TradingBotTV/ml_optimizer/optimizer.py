
import numpy as np

from .data_fetcher import fetch_klines
from .backtest import backtest_strategy
from .logger import get_logger


logger = get_logger(__name__)


def optimize(
    symbol: str,
    buy_start: int = 20,
    buy_end: int = 40,
    buy_step: int = 5,
    sell_start: int = 60,
    sell_end: int = 80,
    sell_step: int = 5,
) -> tuple[int, int]:
    """Grid search best RSI thresholds for ``symbol``."""

    df = fetch_klines(symbol, interval='1h', limit=500)
    best_pnl = -np.inf
    best_params = None

    for buy_th in range(buy_start, buy_end, buy_step):
        for sell_th in range(sell_start, sell_end, sell_step):
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
    import argparse

    parser = argparse.ArgumentParser(description="Grid search RSI parameters")
    parser.add_argument("symbol", help="Trading symbol")
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging verbosity",
    )
    parser.add_argument("--buy-start", type=int, default=20)
    parser.add_argument("--buy-end", type=int, default=40)
    parser.add_argument("--buy-step", type=int, default=5)
    parser.add_argument("--sell-start", type=int, default=60)
    parser.add_argument("--sell-end", type=int, default=80)
    parser.add_argument("--sell-step", type=int, default=5)
    args = parser.parse_args()

    logger.setLevel(args.log_level)

    optimize(
        args.symbol,
        buy_start=args.buy_start,
        buy_end=args.buy_end,
        buy_step=args.buy_step,
        sell_start=args.sell_start,
        sell_end=args.sell_end,
        sell_step=args.sell_step,
    )
