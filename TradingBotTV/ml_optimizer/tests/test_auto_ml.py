import sys
from pathlib import Path
import pandas as pd

ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from TradingBotTV.ml_optimizer import auto_ml  # noqa: E402


def test_optuna_optimize(monkeypatch):
    df = pd.DataFrame({"close": [1, 2, 3, 4, 5]})
    monkeypatch.setattr(auto_ml, "fetch_klines", lambda *a, **k: df)
    monkeypatch.setattr(auto_ml, "backtest_strategy", lambda *a, **k: 1.0)
    buy, sell, pnl = auto_ml.optuna_optimize("BTCUSDT", trials=1)
    assert 10 <= buy <= 50
    assert 50 <= sell <= 90
    assert pnl == 1.0
