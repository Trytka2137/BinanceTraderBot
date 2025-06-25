import pandas as pd
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from TradingBotTV.ml_optimizer import rl_optimizer as rl  # noqa: E402


def test_train_learns_best_thresholds(monkeypatch):
    import random
    random.seed(0)
    # Fake data fetcher returns simple dataframe
    monkeypatch.setattr(
        rl,
        "fetch_klines",
        lambda *a, **k: pd.DataFrame({
            "close": [1, 2, 3, 4, 5, 4, 3, 2, 1, 2]
        }),
    )

    # Reward is highest when buy=28, sell=72
    def fake_backtest(df, rsi_buy_threshold, rsi_sell_threshold):
        return 100 - abs(rsi_buy_threshold - 28) - abs(rsi_sell_threshold - 72)

    monkeypatch.setattr(rl, "backtest_strategy", fake_backtest)

    # Disable state saving
    monkeypatch.setattr(rl, "save_state", lambda state: None)

    buy, sell = rl.train("TEST", episodes=60)
    assert abs(buy - 28) <= 6
    assert abs(sell - 72) <= 6
