import sys
from pathlib import Path
import pandas as pd

ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from TradingBotTV.ml_optimizer import expert_ai  # noqa: E402


def test_generate_expert_report(monkeypatch):
    df = pd.read_csv(
        ROOT_DIR / "TradingBotTV/ml_optimizer/data/BTCUSDT_1h.csv",
        parse_dates=["open_time"],
    )
    monkeypatch.setattr(expert_ai, "fetch_klines", lambda *a, **k: df)
    monkeypatch.setattr(
        expert_ai,
        "auto_select_best_strategy",
        lambda *a, **k: "RSI",
    )
    monkeypatch.setattr(
        expert_ai,
        "fetch_github_activity",
        lambda repo: {"stars": 42},
    )
    report = expert_ai.generate_expert_report(
        "BTCUSDT",
        ["good", "great"],
        "owner/repo",
    )
    assert report["strategy"] == "RSI"
    assert report["signal"] in {"BUY", "SELL"}
    assert report["sentiment"] == 1.0
    assert report["github_stars"] == 42
