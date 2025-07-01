import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from TradingBotTV.ml_optimizer import signal_handler  # noqa: E402


def test_parse_payload():
    payload = {
        "ticker": "BTCUSDT",
        "volume": "1.5",
        "vars": {"foo": 1},
        "strategy": {"order_action": "buy"},
    }
    data = signal_handler.parse_tradingview_payload(payload)
    assert data["volume"] == 1.5
    assert data["vars"]["foo"] == 1


def test_execute_strategies():
    called = []

    def strat(p):
        called.append(p)

    signal_handler.execute_strategies([strat], {"a": 1})
    assert called and called[0]["a"] == 1
