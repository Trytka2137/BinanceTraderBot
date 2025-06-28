from typing import Dict, List


def allocate_equal_weight(
    symbols: List[str], capital: float
) -> Dict[str, float]:
    """Allocate capital equally across all symbols."""
    if not symbols or capital <= 0:
        raise ValueError("symbols and capital must be provided")
    allocation = capital / len(symbols)
    return {sym: allocation for sym in symbols}


def calculate_position_sizes(
    prices: Dict[str, float], capital: float, risk_percent: float = 0.01
) -> Dict[str, float]:
    """Return position size for each symbol based on risk percentage."""
    if not prices or capital <= 0 or risk_percent <= 0:
        raise ValueError("invalid inputs")
    alloc = capital * risk_percent / len(prices)
    return {sym: alloc / price for sym, price in prices.items() if price > 0}
