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
