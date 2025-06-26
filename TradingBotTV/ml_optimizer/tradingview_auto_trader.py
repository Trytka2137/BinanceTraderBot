"""Fetch TradingView analysis and optionally trigger trades via a local
webhook."""

from __future__ import annotations

import requests
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
    """Send trading ``signal`` for ``symbol`` to webhook ``url``."""
    data = {
        "ticker": symbol,
        "strategy": {"order_action": signal.lower()},
    }
    try:
        resp = requests.post(url, json=data, timeout=5)
        logger.info("Webhook status: %s", resp.status_code)
    # pragma: no cover - network failure
    except requests.RequestException as exc:
        logger.error("Error sending webhook: %s", exc)


def auto_trade_from_tv(symbol: str) -> None:
    """Fetch TradingView recommendation and send trade signal if
    appropriate."""
    rec = get_tv_recommendation(symbol)
    logger.info("TradingView recommendation for %s: %s", symbol, rec)
    if rec in {"STRONG_BUY", "BUY"}:
        send_webhook("buy", symbol)
    elif rec in {"STRONG_SELL", "SELL"}:
        send_webhook("sell", symbol)


if __name__ == "__main__":  # pragma: no cover - manual run helper
    import sys
    if len(sys.argv) < 2:
        logger.error("Usage: python tradingview_auto_trader.py <symbol>")
        raise SystemExit(1)
    auto_trade_from_tv(sys.argv[1])
