import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from TradingBotTV.ml_optimizer import monitor  # noqa: E402


def test_record_metric_writes_file(tmp_path, monkeypatch):
    path = tmp_path / "metrics.csv"
    monkeypatch.setattr(monitor, "MONITOR_FILE", path)
    monitor.record_metric("pnl", 1.23)
    assert path.exists()
    lines = path.read_text().strip().splitlines()
    assert lines and "pnl" in lines[0]
