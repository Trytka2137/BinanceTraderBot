"""Utilities for handling TradingView webhook signals."""

from __future__ import annotations

from typing import Any, Callable, Dict, Iterable


def parse_tradingview_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Return normalized payload with optional volume and strategy vars."""
    data = {
        "ticker": payload.get("ticker"),
        "action": payload.get("strategy", {}).get("order_action"),
    }
    if "volume" in payload:
        data["volume"] = float(payload["volume"])
    if "vars" in payload:
        data["vars"] = payload["vars"]
    return data


def execute_strategies(
    strategies: Iterable[Callable[[Dict[str, Any]], None]],
    payload: Dict[str, Any],
) -> None:
    """Call each strategy function with *payload*."""
    for strategy in strategies:
        strategy(payload)
