"""Visualization utilities for optimizer metrics."""

from __future__ import annotations

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

from .monitor import MONITOR_FILE


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
