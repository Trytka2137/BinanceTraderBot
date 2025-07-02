import pandas as pd
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from TradingBotTV.ml_optimizer import compare_strategies as cs  # noqa: E402


def test_auto_select_best_strategy(monkeypatch):
    monkeypatch.setattr(
        cs,
        "fetch_klines",
        lambda *a, **k: pd.DataFrame({"close": [1, 2, 3, 4, 5, 4, 3, 2, 1]})
    )
    monkeypatch.setattr(
        cs,
        "compare_strategies",
        lambda df: {"s1": df["close"].sum(), "s2": -df["close"].sum()}
    )
    best = cs.auto_select_best_strategy("TEST", splits=2)
    assert best == "s1"


def test_should_switch_strategy():
    scores = {"s1": 10.0, "s2": 12.0}
    assert cs.should_switch_strategy("s1", scores, threshold=0.1)
    assert not cs.should_switch_strategy("s2", scores)
