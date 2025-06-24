import os
import sys
import pandas as pd
import numpy as np

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from TradingBotTV.ml_optimizer import compute_rsi, compute_macd, backtest_strategy


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
    series = pd.Series(list(range(1,16)) + list(range(15,5,-1)) + list(range(6,16)))
    df = pd.DataFrame({'close': series})
    pnl = backtest_strategy(df)
    assert pnl == 9

