"""Basic trading strategies and a simple selector."""

from __future__ import annotations

from typing import Sequence, List


def grid_levels(price: float, step: float, levels: int) -> List[float]:
    """Return buy and sell price levels around ``price``.

    The function generates symmetric levels above and below ``price`` spaced by
    ``step``. ``levels`` must be positive.
    """
    if step <= 0 or levels <= 0:
        raise ValueError("step and levels must be positive")
    return [
        price + step * i if i > 0 else price - step * (-i)
        for i in range(-levels, levels + 1)
        if i != 0
    ]


def dca_schedule(amount: float, periods: int) -> List[float]:
    """Return equal investment amounts for dollar-cost averaging."""
    if periods <= 0 or amount <= 0:
        raise ValueError("amount and periods must be positive")
    slice_amt = amount / periods
    return [slice_amt for _ in range(periods)]


def scalp_signal(prices: Sequence[float], window: int = 3) -> int:
    """Return 1 to buy, -1 to sell or 0 to hold based on a simple MA cross."""
    if len(prices) <= window:
        raise ValueError("not enough price data")
    ma = sum(prices[-window - 1:-1]) / window
    last = prices[-1]
    if last > ma * 1.001:
        return 1
    if last < ma * 0.999:
        return -1
    return 0


def choose_strategy(volatility: float, spread: float) -> str:
    """Select trading strategy based on market conditions."""
    if spread > 0.5:
        return "arbitrage"
    if volatility > 0.05:
        return "scalping"
    if volatility > 0.02:
        return "grid"
    return "dca"
