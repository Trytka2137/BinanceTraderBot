from .data_fetcher import fetch_klines
import numpy as np
from sklearn.model_selection import TimeSeriesSplit

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


def auto_select_best_strategy(symbol: str, splits: int = 3) -> str:
    """Return best strategy using time-series cross validation."""
    df = fetch_klines(symbol, interval="1h", limit=500)
    if df.empty:
        raise ValueError("no data for auto selection")

    cv = TimeSeriesSplit(n_splits=splits)
    scores: dict[str, list[float]] = {}
    for _, test_idx in cv.split(df):
        res = compare_strategies(df.iloc[test_idx])
        for name, pnl in res.items():
            scores.setdefault(name, []).append(pnl)

    avg_scores = {n: float(np.mean(v)) for n, v in scores.items()}
    best = max(avg_scores, key=avg_scores.get)
    logger.info("Auto selected best strategy: %s", best)
    return best


def should_switch_strategy(
    current: str, scores: dict[str, float], threshold: float = 0.05
) -> bool:
    """Return ``True`` if a new strategy beats ``current`` by ``threshold``."""
    if current not in scores:
        raise ValueError("current strategy score missing")
    best = max(scores, key=scores.get)
    if best == current:
        return False
    improvement = scores[best] - scores[current]
    base = abs(scores[current]) if scores[current] != 0 else 1.0
    return improvement >= base * threshold


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Compare strategies')
    parser.add_argument('symbol', help='Trading symbol')
    parser.add_argument(
        '--log-level',
        default='INFO',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
    )
    args = parser.parse_args()

    logger.setLevel(args.log_level)

    run(args.symbol)
