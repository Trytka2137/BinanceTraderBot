import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from TradingBotTV.ml_optimizer import portfolio  # noqa: E402


def test_allocate_equal_weight():
    alloc = portfolio.allocate_equal_weight(["BTCUSDT", "ETHUSDT"], 1000)
    assert alloc["BTCUSDT"] == 500 and alloc["ETHUSDT"] == 500


def test_calculate_position_sizes():
    prices = {"BTCUSDT": 20000, "ETHUSDT": 1000}
    sizes = portfolio.calculate_position_sizes(prices, 10000, 0.1)
    assert sizes["BTCUSDT"] > 0 and sizes["ETHUSDT"] > 0
