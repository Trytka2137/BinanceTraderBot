import sys
from pathlib import Path
import numpy as np
import pandas as pd

ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from TradingBotTV.ml_optimizer.advanced_rl import (  # noqa: E402
    LSTMTrendModel,
    OnlineRLTrainer,
    dqn_training_example,
)


def test_lstm_trend_model_train_and_predict():
    prices = pd.Series(np.linspace(1, 2, 20))
    model = LSTMTrendModel.create(window=5)
    model.fit(prices, epochs=1)
    pred = model.predict_next(prices.iloc[-5:])
    assert isinstance(pred, float)


def test_online_rl_trainer_runs():
    prices = np.linspace(1, 2, 15)
    trainer = OnlineRLTrainer(
        LSTMTrendModel.create(window=3), update_interval=5
    )
    out = None
    for p in prices:
        out = trainer.process_price(float(p))
    assert out is not None


def test_dqn_training_example_runs():
    states = np.random.rand(10, 4)
    actions = np.random.randint(0, 2, size=10)
    rewards = np.random.rand(10)
    model = dqn_training_example(states, actions, rewards, episodes=1)
    pred = model.predict(states[:1], verbose=0)
    assert pred.shape == (1, 2)
