import pandas as pd
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from TradingBotTV.ml_optimizer import risk  # noqa: E402


def test_kelly_fraction_valid():
    frac = risk.kelly_fraction(0.6, 1)
    assert 0 < frac < 1


def test_kelly_fraction_formula():
    """Ensure kelly_fraction matches theoretical value."""
    frac = risk.kelly_fraction(0.6, 2)
    assert abs(frac - 0.4) < 1e-9


def test_value_at_risk_basic():
    series = pd.Series([1, -2, 3, -4, 5])
    var = risk.value_at_risk(series, level=0.2)
    assert var > 0
