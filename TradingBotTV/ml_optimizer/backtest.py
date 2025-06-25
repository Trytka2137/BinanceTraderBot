import pandas as pd


def compute_rsi(series: pd.Series, period: int = 14) -> pd.Series:
    """Return RSI indicator for ``series``."""
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def backtest_strategy(
    df: pd.DataFrame,
    rsi_buy_threshold: int = 30,
    rsi_sell_threshold: int = 70,
) -> float:
    """Simple RSI strategy backtest."""
    df = df.copy()
    df["rsi"] = compute_rsi(df["close"])
    position = 0
    pnl = 0.0
    entry_price = 0.0

    for i in range(1, len(df)):
        if position == 0:
            if df["rsi"].iloc[i] < rsi_buy_threshold:
                position = 1
                entry_price = df["close"].iloc[i]
            elif df["rsi"].iloc[i] > rsi_sell_threshold:
                position = -1
                entry_price = df["close"].iloc[i]
        elif position == 1 and df["rsi"].iloc[i] > rsi_sell_threshold:
            pnl += df["close"].iloc[i] - entry_price
            position = 0
        elif position == -1 and df["rsi"].iloc[i] < rsi_buy_threshold:
            pnl += entry_price - df["close"].iloc[i]
            position = 0

    return pnl


def compute_macd(
    series: pd.Series,
    short: int = 12,
    long: int = 26,
    signal: int = 9,
):
    """Return MACD and signal line."""
    exp1 = series.ewm(span=short, adjust=False).mean()
    exp2 = series.ewm(span=long, adjust=False).mean()
    macd = exp1 - exp2
    signal_line = macd.ewm(span=signal, adjust=False).mean()
    return macd, signal_line


def compute_ema(series: pd.Series, period: int = 20) -> pd.Series:
    """Return exponential moving average for ``series``."""
    return series.ewm(span=period, adjust=False).mean()


def compute_atr(
    high: pd.Series,
    low: pd.Series,
    close: pd.Series,
    period: int = 14,
) -> pd.Series:
    """Return Average True Range indicator."""
    hl = high - low
    hc = (high - close.shift()).abs()
    lc = (low - close.shift()).abs()
    tr = pd.concat([hl, hc, lc], axis=1).max(axis=1)
    return tr.rolling(window=period).mean()


def backtest_macd_strategy(
    df: pd.DataFrame,
    short: int = 12,
    long: int = 26,
    signal: int = 9,
) -> float:
    """Backtest simple MACD crossover strategy."""
    macd, signal_line = compute_macd(df["close"], short, long, signal)
    position = 0
    entry_price = 0.0
    pnl = 0.0

    for i in range(1, len(df)):
        if position == 0:
            if macd.iloc[i] > signal_line.iloc[i]:
                position = 1
                entry_price = df["close"].iloc[i]
            elif macd.iloc[i] < signal_line.iloc[i]:
                position = -1
                entry_price = df["close"].iloc[i]
        elif position == 1 and macd.iloc[i] < signal_line.iloc[i]:
            pnl += df["close"].iloc[i] - entry_price
            position = 0
        elif position == -1 and macd.iloc[i] > signal_line.iloc[i]:
            pnl += entry_price - df["close"].iloc[i]
            position = 0

    return pnl


def compare_strategies(df: pd.DataFrame) -> dict:
    """Return PnL for RSI and MACD strategies on ``df``."""
    rsi_pnl = backtest_strategy(df)
    macd_pnl = backtest_macd_strategy(df)
    return {"rsi": rsi_pnl, "macd": macd_pnl}
