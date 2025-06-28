"""Simple hedging utilities."""


def hedge_ratio(
    spot_qty: float, spot_price: float, futures_price: float
) -> float:
    """Calculate futures quantity needed to hedge spot position."""
    if spot_qty <= 0 or spot_price <= 0 or futures_price <= 0:
        raise ValueError("invalid inputs")
    return spot_qty * spot_price / futures_price
