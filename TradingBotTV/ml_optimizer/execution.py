"""Execution algorithms such as TWAP and VWAP."""
from typing import List


def twap_order(prices: List[float], qty: float, slices: int) -> List[float]:
    """Simulate executing an order using Time-Weighted Average Price."""
    if slices <= 0:
        raise ValueError("slices must be positive")
    if len(prices) < slices:
        raise ValueError("not enough price points for given slices")
    slice_qty = qty / slices
    fills = []
    for i in range(slices):
        fills.append(prices[i] * slice_qty)
    return fills


def vwap_order(
    prices: List[float],
    volumes: List[float],
    qty: float,
) -> List[float]:
    """Simulate executing an order using Volume-Weighted Average Price."""
    if len(prices) != len(volumes):
        raise ValueError("prices and volumes must be same length")
    total_vol = sum(volumes)
    if total_vol == 0:
        raise ValueError("volumes must sum to > 0")
    fills = []
    for price, vol in zip(prices, volumes):
        portion = qty * (vol / total_vol)
        fills.append(price * portion)
    return fills
