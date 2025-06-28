"""Simple high frequency trading utilities."""
from typing import Dict, List

from .orderbook import compute_order_flow_imbalance


def midprice(snapshot: Dict[str, List[List[float]]]) -> float:
    """Return order book midprice from snapshot."""
    bids = snapshot.get("bids")
    asks = snapshot.get("asks")
    if not bids or not asks:
        raise ValueError("snapshot must contain bids and asks")
    best_bid = max(bids, key=lambda x: x[0])[0]
    best_ask = min(asks, key=lambda x: x[0])[0]
    return (best_bid + best_ask) / 2


def generate_hft_signal(snapshot: Dict[str, List[List[float]]]) -> int:
    """Generate a simple HFT signal using order flow imbalance."""
    bids = [b[1] for b in snapshot.get("bids", [])]
    asks = [a[1] for a in snapshot.get("asks", [])]
    imbalance = compute_order_flow_imbalance(bids, asks)
    if imbalance > 0.1:
        return 1
    if imbalance < -0.1:
        return -1
    return 0
