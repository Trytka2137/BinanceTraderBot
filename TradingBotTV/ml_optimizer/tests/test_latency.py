import asyncio
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from TradingBotTV.ml_optimizer.hft import measure_latency  # noqa: E402


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
    latency = asyncio.run(measure_latency("http://example.com"))
    assert latency >= 0
