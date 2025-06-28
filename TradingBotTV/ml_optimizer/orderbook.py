from typing import Dict, List, Tuple


def best_bid_ask(
    order_book: Dict[str, List[List[float]]],
) -> Tuple[float, float]:
    """Return best bid and ask price from order book snapshot."""
    bids = order_book.get("bids")
    asks = order_book.get("asks")
    if not bids or not asks:
        raise ValueError("order book must contain bids and asks")
    best_bid = max(bids, key=lambda x: x[0])[0]
    best_ask = min(asks, key=lambda x: x[0])[0]
    return best_bid, best_ask


def compute_order_flow_imbalance(
    bids: List[float], asks: List[float]
) -> float:
    """Calculate order flow imbalance between bids and asks."""
    bid_sum = sum(bids)
    ask_sum = sum(asks)
    total = bid_sum + ask_sum
    if total == 0:
        return 0.0
    return (bid_sum - ask_sum) / total
