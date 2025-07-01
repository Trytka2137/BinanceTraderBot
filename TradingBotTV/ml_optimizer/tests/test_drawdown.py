import sys
from pathlib import Path
import pandas as pd

ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from TradingBotTV.ml_optimizer.risk import max_drawdown  # noqa: E402


def test_max_drawdown_basic():
    prices = pd.Series([1, 2, 1, 1.5])
    dd = max_drawdown(prices)
    assert dd < 0
