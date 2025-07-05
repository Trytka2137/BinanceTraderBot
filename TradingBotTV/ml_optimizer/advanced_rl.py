"""Advanced reinforcement learning utilities using LSTM and DQN."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np
import pandas as pd

try:  # TensorFlow 2.x exposes Keras as a submodule
    from tensorflow import keras
    from tensorflow.keras import layers
except Exception:  # pragma: no cover - fall back to standalone Keras
    import keras  # type: ignore
    from keras import layers


@dataclass
class LSTMTrendModel:
    model: keras.Model

    @classmethod
    def create(cls, window: int = 10) -> "LSTMTrendModel":
        inputs = keras.Input(shape=(window, 1))
        x = layers.LSTM(16, activation="tanh")(inputs)
        outputs = layers.Dense(1)(x)
        model = keras.Model(inputs, outputs)
        model.compile(optimizer="adam", loss="mse")
        return cls(model)

    def fit(self, prices: pd.Series, epochs: int = 3) -> None:
        if len(prices) <= self.model.input_shape[1]:
            raise ValueError("price series too short")
        window = self.model.input_shape[1]
        X = []
        y = []
        for i in range(len(prices) - window):
            X.append(prices.iloc[i: i + window].values)
            y.append(prices.iloc[i + window])
        X = np.array(X)[..., None]
        y = np.array(y)
        self.model.fit(X, y, epochs=epochs, verbose=0)

    def predict_next(self, window_prices: Iterable[float]) -> float:
        arr = np.array(window_prices, dtype=float)[None, :, None]
        return float(self.model.predict(arr, verbose=0)[0, 0])


class OnlineRLTrainer:
    """Simple online trainer adjusting model as new data arrives."""

    def __init__(
        self, model: LSTMTrendModel, update_interval: int = 10
    ) -> None:
        self.model = model
        self.update_interval = update_interval
        self.buffer: list[float] = []

    def process_price(self, price: float) -> float | None:
        self.buffer.append(price)
        if len(self.buffer) >= self.update_interval:
            series = pd.Series(self.buffer)
            self.model.fit(series)
            self.buffer = self.buffer[-self.model.model.input_shape[1]:]
        if len(self.buffer) >= self.model.model.input_shape[1]:
            return self.model.predict_next(
                self.buffer[-self.model.model.input_shape[1]:]
            )
        return None


def dqn_training_example(
    states: np.ndarray,
    actions: np.ndarray,
    rewards: np.ndarray,
    episodes: int = 5,
) -> keras.Model:
    """Train a minimal DQN on provided data."""
    num_features = states.shape[1]
    model = keras.Sequential([
        layers.Dense(32, activation="relu", input_shape=(num_features,)),
        layers.Dense(32, activation="relu"),
        layers.Dense(actions.max() + 1, activation="linear"),
    ])
    model.compile(optimizer=keras.optimizers.Adam(0.001), loss="mse")
    for _ in range(episodes):
        q_values = model.predict(states, verbose=0)
        target = q_values.copy()
        for i, a in enumerate(actions):
            target[i, a] = rewards[i]
        model.fit(states, target, epochs=1, verbose=0)
    return model
