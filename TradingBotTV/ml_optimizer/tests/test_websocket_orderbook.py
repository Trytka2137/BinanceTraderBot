import asyncio
import json
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from TradingBotTV.ml_optimizer import websocket_orderbook  # noqa: E402


class _WS:
    def __init__(self, messages):
        self._messages = messages
        self._iter = iter(messages)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        pass

    def __aiter__(self):
        async def gen():
            for m in self._messages:
                msg = type('Msg', (), {'type': 1, 'data': json.dumps(m)})()
                yield msg
        return gen()

    async def close(self):
        pass


class _Session:
    def __init__(self, messages):
        self._messages = messages

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        pass

    def ws_connect(self, url):
        return _WS(self._messages)


async def _run(monkeypatch):
    monkeypatch.setattr(
        "aiohttp.ClientSession",
        lambda: _Session([{"bids": [[1, 1]], "asks": [[2, 1]]}]),
    )
    gen = websocket_orderbook.stream_order_book("BTCUSDT")
    async for snap in gen:
        assert "bids" in snap
        break


def test_stream_order_book(monkeypatch):
    asyncio.run(_run(monkeypatch))
