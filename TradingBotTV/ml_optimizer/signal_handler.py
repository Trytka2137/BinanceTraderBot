"""Utilities for handling TradingView webhook signals."""

from __future__ import annotations

from typing import Any, Callable, Dict, Iterable, Mapping


def parse_tradingview_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Return normalized payload with optional volume and extended fields."""
    data = {
        "ticker": payload.get("ticker"),
        "action": payload.get("strategy", {}).get("order_action")
        or payload.get("action")
        or payload.get("signal"),
    }
    if "volume" in payload:
        data["volume"] = float(payload["volume"])
    if "vars" in payload:
        data["vars"] = payload["vars"]
    for field in ("exchange", "interval", "comment", "price"):
        if field in payload:
            data[field] = payload[field]
    if "strategy" in payload and "order_contracts" in payload["strategy"]:
        data["size"] = payload["strategy"]["order_contracts"]
    if "strategies" in payload:
        data["strategies"] = payload["strategies"]
    return data


def execute_strategies(
    strategies: Iterable[Callable[[Dict[str, Any]], None]]
    | Mapping[str, Callable[[Dict[str, Any]], None]],
    payload: Dict[str, Any],
) -> None:
    """Call strategy functions with *payload*.

    ``strategies`` may be an iterable of callables or a mapping from name
    to callable. If a mapping is provided and ``payload`` has a ``strategies``
    list, only the named strategies will be executed.
    """
    if isinstance(strategies, Mapping) and payload.get("strategies"):
        for name in payload["strategies"]:
            func = strategies.get(name)
            if func:
                func(payload)
    else:
        for strategy in strategies:
            strategy(payload)
