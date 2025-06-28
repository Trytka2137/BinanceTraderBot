import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from TradingBotTV.ml_optimizer import arbitrage  # noqa: E402


def test_price_spread():
    spread = arbitrage.price_spread(101, 100)
    assert spread == 1
