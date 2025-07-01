import sys
import time
import threading
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from TradingBotTV.ml_optimizer import fundamental  # noqa: E402


def test_cache_fundamental_data_regularly(monkeypatch, tmp_path):
    calls = []

    def fake_cache(symbol, path):
        calls.append((symbol, path))

    monkeypatch.setattr(fundamental, "cache_fundamental_data", fake_cache)
    stop = threading.Event()
    thread = fundamental.cache_fundamental_data_regularly(
        "BTC",
        tmp_path / "fund.json",
        interval=0.1,
        stop_event=stop,
    )
    time.sleep(0.25)
    stop.set()
    thread.join(timeout=1)
    assert len(calls) >= 2
