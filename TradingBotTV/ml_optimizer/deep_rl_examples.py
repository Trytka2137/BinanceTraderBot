"""Simple deep reinforcement learning examples for trading strategies."""

from __future__ import annotations

import numpy as np
import pandas as pd


def deep_q_learning_example(
    prices: pd.Series,
    episodes: int = 10,
    lr: float = 0.01,
    gamma: float = 0.95,
    epsilon: float = 1.0,
    epsilon_decay: float = 0.95,
) -> list[float]:
    """Train a minimal DQN on ``prices`` and return cumulative rewards."""
    if prices.empty or len(prices) < 2:
        raise ValueError("price series must contain at least 2 points")

    weights = np.random.randn(2, 2) * 0.1
    rewards_history: list[float] = []
    for _ in range(episodes):
        pos = 0  # 0 = flat, 1 = long
        total_reward = 0.0
        for i in range(len(prices) - 1):
            state = np.array([[prices.iloc[i]], [pos]])
            q_vals = state.T @ weights
            if np.random.rand() < epsilon:
                action = np.random.randint(0, 2)
            else:
                action = int(q_vals.argmax())

            next_pos = 1 if action == 1 else 0
            reward = (
                prices.iloc[i + 1] - prices.iloc[i] if next_pos == 1 else 0.0
            )
            next_state = np.array([[prices.iloc[i + 1]], [next_pos]])
            next_q = next_state.T @ weights
            td_target = reward + gamma * next_q.max()
            td_error = td_target - q_vals[0, action]
            weights[:, action] += lr * td_error * state[:, 0]
            pos = next_pos
            total_reward += reward
        epsilon *= epsilon_decay
        rewards_history.append(total_reward)
    return rewards_history
