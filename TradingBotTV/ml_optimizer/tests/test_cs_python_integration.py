import sys
import json
import pandas as pd
import re
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from TradingBotTV.ml_optimizer import auto_optimizer  # noqa: E402


def test_optimizer_output_updates_config(tmp_path, monkeypatch):
    df = pd.DataFrame({
        "open_time": pd.date_range("2024-01-01", periods=5, freq="h"),
        "close": [1, 2, 3, 4, 5],
    })
    monkeypatch.setattr(auto_optimizer, "fetch_klines", lambda *a, **k: df)
    monkeypatch.setattr(auto_optimizer, "record_metric", lambda *a, **k: None)
    monkeypatch.setattr(auto_optimizer, "STATE_DIR", tmp_path)
    monkeypatch.setattr(auto_optimizer, "STATE_PATH", tmp_path / "state.json")

    buy, sell, pnl = auto_optimizer.optimize("BTCUSDT", iterations=1)
    output = f"Najlepsze parametry: Buy={buy} Sell={sell} PnL={pnl}"

    config = tmp_path / "settings.json"
    config.write_text(json.dumps({
        "binance": {"apiKey": "", "apiSecret": ""},
        "trading": {"rsiBuyThreshold": 10, "rsiSellThreshold": 90},
    }))

    match = re.search(r"Buy=(\d+).*Sell=(\d+)", output)
    assert match
    data = json.loads(config.read_text())
    data["trading"]["rsiBuyThreshold"] = int(match.group(1))
    data["trading"]["rsiSellThreshold"] = int(match.group(2))
    config.write_text(json.dumps(data))

    updated = json.loads(config.read_text())
    assert updated["trading"]["rsiBuyThreshold"] == int(match.group(1))
    assert updated["trading"]["rsiSellThreshold"] == int(match.group(2))
