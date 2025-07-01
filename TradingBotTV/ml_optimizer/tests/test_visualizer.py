import sys
import pandas as pd
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from TradingBotTV.ml_optimizer.visualizer import plot_metrics  # noqa: E402


def test_plot_metrics(tmp_path):
    csv = tmp_path / "metrics.csv"
    df = pd.DataFrame(
        {"timestamp": ["2024-01-01T00:00:00"], "name": ["test"], "value": [1]}
    )
    df.to_csv(csv, index=False, header=False)
    fig = plot_metrics(csv)
    assert fig is not None
