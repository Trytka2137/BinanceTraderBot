import asyncio
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from TradingBotTV.ml_optimizer.hft import fast_market_order  # noqa: E402


class _Resp:
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        pass

    async def json(self):
        return {"status": "ok"}


class _Session:
    def post(self, url, params=None):
        return _Resp()


async def _run():
    result = await fast_market_order(_Session(), "BTCUSDT", "BUY", 1.0)
    assert result == {"status": "ok"}


def test_fast_market_order():
    asyncio.run(_run())
