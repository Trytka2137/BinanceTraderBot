import sys
import pandas as pd
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from TradingBotTV.ml_optimizer.visualizer import (  # noqa: E402
    plot_metrics,
    plot_performance_and_risk,
    plot_risk_indicators,
)


def test_plot_metrics(tmp_path):
    csv = tmp_path / "metrics.csv"
    df = pd.DataFrame(
        {"timestamp": ["2024-01-01T00:00:00"], "name": ["test"], "value": [1]}
    )
    df.to_csv(csv, index=False, header=False)
    fig = plot_metrics(csv)
    assert fig is not None


def test_plot_performance_and_risk():
    returns = pd.Series([0.01, -0.02, 0.03])
    fig = plot_performance_and_risk(returns)
    assert fig is not None


def test_plot_risk_indicators(tmp_path):
    csv = tmp_path / "metrics.csv"
    df = pd.DataFrame(
        {
            "timestamp": ["2024-01-01T00:00:00", "2024-01-01T01:00:00"],
            "name": ["pnl", "pnl"],
            "value": [1.0, -0.5],
        }
    )
    df.to_csv(csv, index=False, header=False)
    fig = plot_risk_indicators(csv)
    assert fig is not None
