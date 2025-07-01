import sys
import pandas as pd
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from TradingBotTV.ml_optimizer import portfolio  # noqa: E402


def test_risk_parity_weights():
    data = pd.DataFrame({
        "BTC": [0.01, -0.02, 0.03],
        "ETH": [0.02, 0.01, -0.01],
    })
    weights = portfolio.risk_parity_weights(data)
    assert abs(sum(weights.values()) - 1) < 1e-6
