import sys
import asyncio
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from TradingBotTV.ml_optimizer import tradingview_auto_trader  # noqa: E402
tv = tradingview_auto_trader


def test_get_tv_recommendation_error(monkeypatch):

    class DummyHandler:
        def __init__(self, *a, **kw):
            pass

        def get_analysis(self):
            raise Exception("fail")
    monkeypatch.setattr(tv, "TA_Handler", DummyHandler)
    rec = tv.get_tv_recommendation("BTCUSDT")
    assert rec == "ERROR"


def test_auto_trade_from_tv_triggers_webhook(monkeypatch):
    called = {}
    monkeypatch.setattr(tv, "get_tv_recommendation", lambda s: "BUY")

    def fake_send(sig, symbol, url="http://localhost:5000/webhook"):
        called["sig"] = sig
        called["symbol"] = symbol
    monkeypatch.setattr(tv, "send_webhook", fake_send)

    tv.auto_trade_from_tv("TEST")

    assert called == {'sig': 'buy', 'symbol': 'TEST'}


def test_async_auto_trade_from_tv(monkeypatch):
    calls = []
    monkeypatch.setattr(tv, "auto_trade_from_tv", lambda s: calls.append(s))

    asyncio.run(tv.async_auto_trade_from_tv(["A", "B"]))

    assert set(calls) == {"A", "B"}
