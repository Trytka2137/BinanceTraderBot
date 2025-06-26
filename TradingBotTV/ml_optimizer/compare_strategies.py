import sys

from .data_fetcher import fetch_klines
from .backtest import compare_strategies
from .logger import get_logger


logger = get_logger(__name__)


def run(symbol: str) -> None:
    df = fetch_klines(symbol, interval='1h', limit=500)
    if df.empty:
        logger.warning('Brak danych do porownania')
        return
    results = compare_strategies(df)
    for name, pnl in results.items():
        logger.info('%s PnL: %s', name, pnl)
    best = max(results, key=results.get)
    logger.info('Najlepsza strategia: %s', best)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Compare strategies')
    parser.add_argument('symbol', help='Trading symbol')
    parser.add_argument('--log-level', default='INFO', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'])
    args = parser.parse_args()

    logger.setLevel(args.log_level)

    run(args.symbol)
