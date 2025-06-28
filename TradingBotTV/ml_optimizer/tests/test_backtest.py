import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from TradingBotTV.ml_optimizer import (  # noqa: E402
    compute_rsi,
    compute_macd,
    compute_atr,
    compute_ema,
    compute_sma,
    backtest_strategy,
)


def test_compute_rsi_basic_uptrend():
    series = pd.Series([1, 2, 3, 4, 5])
    rsi = compute_rsi(series, period=2)
    expected = pd.Series([np.nan, np.nan, 100.0, 100.0, 100.0])
    pd.testing.assert_series_equal(rsi.reset_index(drop=True), expected)


def test_compute_rsi_balanced_movements():
    series = pd.Series([1, 2, 1, 2, 1])
    rsi = compute_rsi(series, period=2)
    expected = pd.Series([np.nan, np.nan, 50.0, 50.0, 50.0])
    pd.testing.assert_series_equal(rsi.reset_index(drop=True), expected)


def test_compute_macd_known_values():
    series = pd.Series(range(1, 11))
    macd, signal = compute_macd(series, short=3, long=6, signal=2)
    exp1 = series.ewm(span=3, adjust=False).mean()
    exp2 = series.ewm(span=6, adjust=False).mean()
    macd_expected = exp1 - exp2
    signal_expected = macd_expected.ewm(span=2, adjust=False).mean()
    pd.testing.assert_series_equal(macd.round(6), macd_expected.round(6))
    pd.testing.assert_series_equal(signal.round(6), signal_expected.round(6))


def test_backtest_strategy_simple_scenario():
    series = pd.Series(
        list(range(1, 16)) + list(range(15, 5, -1)) + list(range(6, 16))
    )
    df = pd.DataFrame({"close": series})
    pnl = backtest_strategy(df)
    assert pnl == 9


def test_compute_atr_basic():
    high = pd.Series([10, 11, 12, 13])
    low = pd.Series([9, 10, 11, 12])
    close = pd.Series([9.5, 10.5, 11.5, 12.5])
    atr = compute_atr(high, low, close, period=2)
    assert len(atr) == 4
    assert atr.iloc[1] > 0


def test_compute_ema_simple():
    series = pd.Series([1, 2, 3, 4])
    ema = compute_ema(series, period=2)
    expected = series.ewm(span=2, adjust=False).mean()
    pd.testing.assert_series_equal(ema.round(6), expected.round(6))


def test_compute_sma_simple():
    series = pd.Series([1, 2, 3, 4])
    sma = compute_sma(series, period=2)
    expected = series.rolling(window=2).mean()
    pd.testing.assert_series_equal(sma, expected)


def test_backtest_strategy_stop_loss(monkeypatch):
    df = pd.DataFrame({"close": [10, 9, 8, 7]})

    def dummy_rsi(series):
        return pd.Series([50, 20, 20, 20])

    monkeypatch.setattr(
        "TradingBotTV.ml_optimizer.backtest.compute_rsi",
        dummy_rsi,
    )

    pnl = backtest_strategy(df, stop_loss_pct=5)
    assert pnl == -1
