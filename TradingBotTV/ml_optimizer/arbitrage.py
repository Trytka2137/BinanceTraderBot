"""Utilities for simple price arbitrage calculations."""


def price_spread(price_a: float, price_b: float) -> float:
    """Return price difference between two markets."""
    return price_a - price_b
