import asyncio
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from TradingBotTV.ml_optimizer import hft  # noqa: E402


class _Resp:
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        pass

    async def text(self):
        return "{}"


class _Session:
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        pass

    def get(self, url):
        return _Resp()


def test_measure_latency(monkeypatch):
    monkeypatch.setattr("aiohttp.ClientSession", lambda: _Session())
    latency = asyncio.run(hft.measure_latency("http://example.com"))
    assert latency >= 0


def test_monitor_latency(monkeypatch):
    monkeypatch.setattr("aiohttp.ClientSession", lambda: _Session())
    result = asyncio.run(hft.monitor_latency(["http://a", "http://b"]))
    assert set(result.keys()) == {"http://a", "http://b"}
    assert all(v >= 0 for v in result.values())
