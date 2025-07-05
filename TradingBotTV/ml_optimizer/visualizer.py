"""Visualization utilities for optimizer metrics."""

from __future__ import annotations

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

from .monitor import MONITOR_FILE
from .risk import value_at_risk, max_drawdown


def plot_metrics(
    path: str | Path = MONITOR_FILE,
    recent: int | None = 500,
) -> plt.Figure:
    """Return a matplotlib figure with metrics plotted over time."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(path)

    df = pd.read_csv(path, names=["timestamp", "name", "value"])
    if recent:
        df = df.tail(recent)
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


def plot_risk_indicators(path: str | Path = MONITOR_FILE) -> plt.Figure:
    """Plot cumulative PnL with Value at Risk and drawdown levels."""
    df = pd.read_csv(path, names=["timestamp", "name", "value"])
    if df.empty:
        raise ValueError("metrics file is empty")
    df = df[df["name"] == "pnl"].copy()
    if df.empty:
        raise ValueError("no pnl data in metrics file")
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df.sort_values("timestamp", inplace=True)
    pnl = df["value"].cumsum()
    var = value_at_risk(df["value"])
    dd = max_drawdown(pnl)
    fig, ax = plt.subplots()
    pnl.plot(ax=ax, label="Cumulative PnL")
    ax.axhline(-var, color="red", linestyle="--", label=f"VaR 5%: {var:.2f}")
    ax.axhline(dd, color="orange", linestyle=":", label=f"Max DD: {dd:.2f}")
    ax.set_xlabel("Time")
    ax.set_ylabel("PnL")
    ax.set_title("PnL and Risk Indicators")
    ax.legend()
    return fig
