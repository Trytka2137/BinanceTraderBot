import numpy as np
import pandas as pd

def compute_rsi(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def backtest_strategy(df, rsi_buy_threshold=30, rsi_sell_threshold=70):
    df['rsi'] = compute_rsi(df['close'])
    position = 0  # 0 - neutral, 1 - long, -1 - short
    pnl = 0
    entry_price = 0

    for i in range(1, len(df)):
        if position == 0:
            if df['rsi'].iloc[i] < rsi_buy_threshold:
                position = 1
                entry_price = df['close'].iloc[i]
            elif df['rsi'].iloc[i] > rsi_sell_threshold:
                position = -1
                entry_price = df['close'].iloc[i]
        elif position == 1 and df['rsi'].iloc[i] > rsi_sell_threshold:
            pnl += df['close'].iloc[i] - entry_price
            position = 0
        elif position == -1 and df['rsi'].iloc[i] < rsi_buy_threshold:
            pnl += entry_price - df['close'].iloc[i]
            position = 0

    return pnl


def compute_macd(series, short=12, long=26, signal=9):
    exp1 = series.ewm(span=short, adjust=False).mean()
    exp2 = series.ewm(span=long, adjust=False).mean()
    macd = exp1 - exp2
    signal_line = macd.ewm(span=signal, adjust=False).mean()
    return macd, signal_line


def compute_ema(series, period=20):
    """Return exponential moving average for the given ``series``."""
    return series.ewm(span=period, adjust=False).mean()


def compute_atr(high, low, close, period=14):
    hl = high - low
    hc = (high - close.shift()).abs()
    lc = (low - close.shift()).abs()
    tr = pd.concat([hl, hc, lc], axis=1).max(axis=1)
    atr = tr.rolling(window=period).mean()
    return atr


def backtest_macd_strategy(df, short=12, long=26, signal=9):
    macd, signal_line = compute_macd(df['close'], short, long, signal)
    position = 0
    entry_price = 0
    pnl = 0

    for i in range(1, len(df)):
        if position == 0:
            if macd.iloc[i] > signal_line.iloc[i]:
                position = 1
                entry_price = df['close'].iloc[i]
            elif macd.iloc[i] < signal_line.iloc[i]:
                position = -1
                entry_price = df['close'].iloc[i]
        elif position == 1 and macd.iloc[i] < signal_line.iloc[i]:
            pnl += df['close'].iloc[i] - entry_price
            position = 0
        elif position == -1 and macd.iloc[i] > signal_line.iloc[i]:
            pnl += entry_price - df['close'].iloc[i]
            position = 0

    return pnl


def compare_strategies(df):
    rsi_pnl = backtest_strategy(df)
    macd_pnl = backtest_macd_strategy(df)
    return {
        'rsi': rsi_pnl,
        'macd': macd_pnl
    }
