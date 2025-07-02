import sys
from pathlib import Path

import pandas as pd

ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from TradingBotTV.ml_optimizer import solana_ai  # noqa: E402


def test_load_sol_data():
    df = solana_ai.load_sol_data(limit=10)
    assert not df.empty
    assert {"open_time", "close"}.issubset(df.columns)


def test_ai_trade_decision():
    df = pd.read_csv(
        ROOT_DIR / "TradingBotTV/ml_optimizer/data/SOLUSDC_1h.csv",
        parse_dates=["open_time"],
    )
    decision = solana_ai.ai_trade_decision(df)
    assert decision in {"BUY", "SELL"}
