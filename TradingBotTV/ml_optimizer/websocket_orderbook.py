"""WebSocket utilities for streaming Binance order book data."""

from __future__ import annotations

import aiohttp
import json
from typing import AsyncGenerator


async def stream_order_book(
    symbol: str, depth: int = 20
) -> AsyncGenerator[dict, None]:
    """Yield order book snapshots via Binance WebSocket."""
    url = (
        "wss://stream.binance.com:9443/ws/"
        f"{symbol.lower()}@depth{depth}@100ms"
    )
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(url) as ws:
            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    yield json.loads(msg.data)
                elif msg.type in (
                    aiohttp.WSMsgType.CLOSE,
                    aiohttp.WSMsgType.ERROR,
                ):
                    break
