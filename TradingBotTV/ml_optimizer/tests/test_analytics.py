import pandas as pd
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from TradingBotTV.ml_optimizer import analytics  # noqa: E402


def test_bollinger_bands_shapes():
    data = pd.Series(range(30))
    bands = analytics.bollinger_bands(data, window=5)
    assert set(bands.columns) == {"sma", "upper", "lower"}
    assert len(bands) == 30


def test_stochastic_oscillator_returns_values():
    high = pd.Series([5, 6, 7, 8, 9])
    low = pd.Series([1, 2, 3, 4, 5])
    close = pd.Series([3, 4, 5, 6, 7])
    osc = analytics.stochastic_oscillator(high, low, close, k_period=3)
    assert "%K" in osc.columns and "%D" in osc.columns


def test_order_book_imbalance_balanced():
    bids = pd.Series([10, 20])
    asks = pd.Series([10, 20])
    assert analytics.order_book_imbalance(bids, asks) == 0


def test_detect_price_anomalies_flags():
    series = pd.Series([1.0]*5 + [10.0] + [1.0]*5)
    flags = analytics.detect_price_anomalies(series, contamination=0.1)
    assert flags.any()


def test_autoencoder_anomaly_scores_length():
    series = pd.Series([1.0] * 15)
    scores = analytics.autoencoder_anomaly_scores(series, window=5, epochs=1)
    assert len(scores) == len(series) - 5
