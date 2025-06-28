import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from TradingBotTV.ml_optimizer import hft  # noqa: E402


def test_midprice():
    snap = {"bids": [[100, 1]], "asks": [[102, 1]]}
    assert hft.midprice(snap) == 101


def test_generate_hft_signal():
    snap = {"bids": [[100, 10]], "asks": [[101, 1]]}
    assert hft.generate_hft_signal(snap) == 1
