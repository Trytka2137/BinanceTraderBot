import sys
from pathlib import Path
import pandas as pd

ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from TradingBotTV.ml_optimizer.deep_rl_examples import (  # noqa: E402
    deep_q_learning_example,
    online_q_learning,
)


def test_deep_q_learning_example_runs():
    prices = pd.Series([1.0, 1.1, 1.2, 1.1, 1.3])
    rewards = deep_q_learning_example(prices, episodes=3)
    assert len(rewards) == 3


def test_online_q_learning_runs():
    prices = [1.0, 1.1, 1.2, 1.3]
    rewards = online_q_learning(prices)
    assert len(rewards) == 3
