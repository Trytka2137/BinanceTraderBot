import sys
import pandas as pd
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from TradingBotTV.ml_optimizer.risk import adaptive_stop_levels  # noqa: E402


def test_adaptive_stop_levels():
    prices = pd.Series([10, 11, 12, 13, 14, 15])
    levels = adaptive_stop_levels(
        prices, atr_period=3, stop_factor=1, take_factor=1
    )
    assert "stop_loss" in levels and "take_profit" in levels
