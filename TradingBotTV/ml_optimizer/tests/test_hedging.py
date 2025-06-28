import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from TradingBotTV.ml_optimizer import hedging  # noqa: E402


def test_hedge_ratio():
    ratio = hedging.hedge_ratio(1, 20000, 20050)
    assert round(ratio, 6) == round(20000 / 20050, 6)
