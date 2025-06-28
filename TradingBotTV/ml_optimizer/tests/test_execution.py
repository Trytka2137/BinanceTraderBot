import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from TradingBotTV.ml_optimizer import execution  # noqa: E402


def test_twap_order():
    fills = execution.twap_order([1, 2, 3], 3, 3)
    assert len(fills) == 3
    assert fills[0] == 1


def test_vwap_order():
    fills = execution.vwap_order([1, 2, 3], [1, 1, 2], 4)
    assert len(fills) == 3
    assert abs(sum(fills) - (1*1 + 2*1 + 3*2)) < 1e-6
