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
        "price": 123,
        "exchange": "BINANCE",
        "strategies": ["s1"],
        "strategy": {"order_action": "buy", "order_contracts": 2},
    }
    data = signal_handler.parse_tradingview_payload(payload)
    assert data["volume"] == 1.5
    assert data["vars"]["foo"] == 1
    assert data["price"] == 123
    assert data["exchange"] == "BINANCE"
    assert data["size"] == 2
    assert data["strategies"] == ["s1"]


def test_execute_strategies():
    called = []

    def s1(p):
        called.append("s1")

    def s2(p):
        called.append("s2")

    signal_handler.execute_strategies(
        {"s1": s1, "s2": s2},
        {"strategies": ["s1"], "a": 1},
    )
    assert called == ["s1"]
