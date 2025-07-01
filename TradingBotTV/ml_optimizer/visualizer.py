"""Visualization utilities for optimizer metrics."""

from __future__ import annotations

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

from .monitor import MONITOR_FILE
from .risk import value_at_risk


def plot_metrics(path: str | Path = MONITOR_FILE) -> plt.Figure:
    """Return a matplotlib figure with metrics plotted over time."""
    df = pd.read_csv(path, names=["timestamp", "name", "value"])
    if df.empty:
        raise ValueError("metrics file is empty")
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    pivot = df.pivot(index="timestamp", columns="name", values="value")
    fig, ax = plt.subplots()
    pivot.plot(ax=ax)
    ax.set_xlabel("Time")
    ax.set_ylabel("Value")
    ax.set_title("Optimizer metrics")
    return fig


def plot_performance_and_risk(returns: pd.Series) -> plt.Figure:
    """Plot cumulative returns and Value at Risk."""
    if returns.empty:
        raise ValueError("returns series is empty")
    cumulative = (1 + returns).cumprod() - 1
    var = value_at_risk(returns)
    fig, ax = plt.subplots()
    cumulative.plot(ax=ax, label="Cumulative Return")
    ax.axhline(-var, color="red", linestyle="--", label=f"VaR 5%: {var:.2f}")
    ax.set_xlabel("Step")
    ax.set_ylabel("Return")
    ax.set_title("Performance and Risk")
    ax.legend()
    return fig
