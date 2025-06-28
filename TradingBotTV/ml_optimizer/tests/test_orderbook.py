import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from TradingBotTV.ml_optimizer import orderbook  # noqa: E402


def test_best_bid_ask():
    snapshot = {"bids": [[100, 1], [99, 2]], "asks": [[101, 1], [102, 2]]}
    bid, ask = orderbook.best_bid_ask(snapshot)
    assert bid == 100 and ask == 101


def test_compute_order_flow_imbalance():
    imbalance = orderbook.compute_order_flow_imbalance([1, 1], [1, 1])
    assert imbalance == 0
