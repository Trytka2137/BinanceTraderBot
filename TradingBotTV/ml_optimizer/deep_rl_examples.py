"""Simple deep reinforcement learning examples for trading strategies."""

from __future__ import annotations

from typing import Iterable

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


def policy_gradient_example(
    prices: pd.Series,
    episodes: int = 10,
    lr: float = 0.01,
    gamma: float = 0.99,
) -> list[float]:
    """Train a toy policy gradient agent and return rewards."""
    if prices.empty or len(prices) < 2:
        raise ValueError("price series must contain at least 2 points")

    weights = np.random.randn(2) * 0.1
    history: list[float] = []
    for _ in range(episodes):
        grads: list[np.ndarray] = []
        rewards: list[float] = []
        pos = 0
        total = 0.0
        for i in range(len(prices) - 1):
            state = np.array([prices.iloc[i], pos])
            prob = 1 / (1 + np.exp(-state @ weights))
            action = 1 if np.random.rand() < prob else 0
            next_pos = action
            reward = prices.iloc[i + 1] - prices.iloc[i] if next_pos else 0.0
            grads.append(state * (action - prob))
            rewards.append(reward)
            pos = next_pos
            total += reward
        G = 0.0
        for g, r in zip(reversed(grads), reversed(rewards)):
            G = r + gamma * G
            weights += lr * G * g
        history.append(total)
    return history


def online_q_learning(
    prices: Iterable[float], lr: float = 0.01, gamma: float = 0.95
) -> list[float]:
    """Train a Q-learning agent incrementally on a stream of prices."""
    weights = np.zeros((2, 2))
    pos = 0
    prev = None
    rewards: list[float] = []
    for price in prices:
        if prev is None:
            prev = price
            continue
        state = np.array([[prev], [pos]])
        q_vals = state.T @ weights
        action = int(q_vals.argmax())
        next_pos = 1 if action == 1 else 0
        reward = price - prev if next_pos == 1 else 0.0
        next_state = np.array([[price], [next_pos]])
        td_target = reward + gamma * (next_state.T @ weights).max()
        td_error = td_target - q_vals[0, action]
        weights[:, action] += lr * td_error * state[:, 0]
        rewards.append(reward)
        pos = next_pos
        prev = price
    return rewards
