"""Helpers for limit order management based on bid/ask spreads."""

from __future__ import annotations


def limit_price_from_spread(
    best_bid: float,
    best_ask: float,
    side: str,
    spread_pct: float = 0.25,
) -> float:
    """Return limit price placed inside the spread.

    ``spread_pct`` is a fraction of the spread added or subtracted from the
    bid/ask price. ``side`` must be ``"buy"`` or ``"sell"``.
    """
    if best_ask <= best_bid:
        raise ValueError("ask must be greater than bid")
    if not 0 <= spread_pct <= 1:
        raise ValueError("spread_pct must be between 0 and 1")
    spread = best_ask - best_bid
    if side == "buy":
        return min(best_bid + spread * spread_pct, best_ask)
    if side == "sell":
        return max(best_ask - spread * spread_pct, best_bid)
    raise ValueError("side must be 'buy' or 'sell'")


def adjust_order_price(
    current_price: float,
    best_bid: float,
    best_ask: float,
    side: str,
    threshold_pct: float = 0.1,
) -> float:
    """Return updated order price when spread widens significantly."""
    target = limit_price_from_spread(
        best_bid,
        best_ask,
        side,
        threshold_pct,
    )
    if side == "buy" and target > current_price:
        return target
    if side == "sell" and target < current_price:
        return target
    return current_price
