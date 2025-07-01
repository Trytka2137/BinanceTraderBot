import sys
import pandas as pd
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from TradingBotTV.ml_optimizer.deep_rl_examples import (  # noqa: E402
    policy_gradient_example,
)


def test_policy_gradient_example_runs():
    prices = pd.Series([1.0, 1.1, 0.9, 1.2])
    rewards = policy_gradient_example(prices, episodes=2, lr=0.01)
    assert len(rewards) == 2
