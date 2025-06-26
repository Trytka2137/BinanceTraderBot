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
    if len(sys.argv) < 2:
        logger.error('Uzycie: python compare_strategies.py SYMBOL')
        sys.exit(1)
    run(sys.argv[1])
