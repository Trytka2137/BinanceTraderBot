import pandas as pd
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from TradingBotTV.ml_optimizer import (  # noqa: E402
    train_predictive_model,
    optimize_predictive_model,
    backtest_tick_strategy,
    train_deep_learning_model,
)


def test_train_predictive_model_returns_estimator():
    df = pd.DataFrame({"close": [1, 2, 3, 2, 3, 4, 5, 4, 5, 6]})
    model = train_predictive_model(df)
    assert hasattr(model, "predict")


def test_optimize_predictive_model_returns_estimator():
    df = pd.DataFrame({"close": [1, 2, 3, 2, 3, 4, 5, 4, 5, 6]})
    model = optimize_predictive_model(df, {"n_estimators": [5, 10]})
    assert hasattr(model, "predict")


class DummyModel:
    def predict(self, X):
        return [1] * len(X)


def test_backtest_tick_strategy_basic():
    df = pd.DataFrame({"price": [1, 1.1, 1.2, 1.3]})
    pnl = backtest_tick_strategy(df, DummyModel())
    assert pnl > 0


def test_train_deep_learning_model_returns_estimator():
    df = pd.DataFrame({"close": [1, 2, 3, 2, 3, 4, 5, 4, 5, 6]})
    model = train_deep_learning_model(df, hidden_layers=(4, 4), epochs=50)
    assert hasattr(model, "predict")
