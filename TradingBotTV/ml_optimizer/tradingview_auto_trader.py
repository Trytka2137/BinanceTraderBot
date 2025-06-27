"""Fetch TradingView analysis and optionally trigger trades via a local
webhook."""

from __future__ import annotations

import requests
from requests.adapters import HTTPAdapter, Retry
import time
import asyncio
from tradingview_ta import TA_Handler, Interval

from .logger import get_logger


logger = get_logger(__name__)


def get_tv_recommendation(symbol: str) -> str:
    """Return TradingView recommendation for *symbol* or ``"ERROR"`` on
    failure."""
    handler = TA_Handler(
        symbol=symbol,
        screener="crypto",
        exchange="BINANCE",
        interval=Interval.INTERVAL_1_HOUR,
    )
    try:
        analysis = handler.get_analysis()
    except Exception as exc:  # pragma: no cover - network failure case
        logger.error("Error fetching TradingView analysis: %s", exc)
        return "ERROR"
    return analysis.summary.get("RECOMMENDATION", "NEUTRAL")


def send_webhook(
    signal: str,
    symbol: str,
    url: str = "http://localhost:5000/webhook",
) -> None:
    """Send trading ``signal`` for ``symbol`` to webhook ``url`` with
    retries."""

    data = {
        "ticker": symbol,
        "strategy": {"order_action": signal.lower()},
    }
    session = requests.Session()
    session.mount(
        "http://",
        HTTPAdapter(
            max_retries=Retry(
                total=3,
                backoff_factor=1,
                status_forcelist=[500, 502, 503, 504],
                allowed_methods=["POST"],
            )
        ),
    )
    for attempt in range(3):
        try:
            resp = session.post(url, json=data, timeout=5)
            logger.info("Webhook status: %s", resp.status_code)
            break
        except requests.RequestException as exc:  # pragma: no cover - network
            logger.error(
                "Error sending webhook (attempt %s/3): %s", attempt + 1, exc
            )
            if attempt == 2:
                break
            time.sleep(2 ** attempt)


def auto_trade_from_tv(symbol: str) -> None:
    """Fetch TradingView recommendation and send trade signal if
    appropriate."""
    rec = get_tv_recommendation(symbol)
    logger.info("TradingView recommendation for %s: %s", symbol, rec)
    if rec in {"STRONG_BUY", "BUY"}:
        send_webhook("buy", symbol)
    elif rec in {"STRONG_SELL", "SELL"}:
        send_webhook("sell", symbol)


async def async_auto_trade_from_tv(symbols: list[str]) -> None:
    """Run :func:`auto_trade_from_tv` concurrently for ``symbols``."""

    tasks = [asyncio.to_thread(auto_trade_from_tv, s) for s in symbols]
    await asyncio.gather(*tasks)


if __name__ == "__main__":  # pragma: no cover - manual run helper
    import argparse

    parser = argparse.ArgumentParser(description="TradingView auto trader")
    parser.add_argument(
        "symbols",
        help="Single symbol or comma-separated list for concurrent mode",
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging verbosity",
    )
    args = parser.parse_args()

    logger.setLevel(args.log_level)

    if "," in args.symbols:
        symbols = [s.strip() for s in args.symbols.split(",") if s.strip()]
        asyncio.run(async_auto_trade_from_tv(symbols))
    else:
        auto_trade_from_tv(args.symbols)
