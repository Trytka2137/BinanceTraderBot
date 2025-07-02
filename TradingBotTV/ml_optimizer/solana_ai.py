import pandas as pd

from .data_fetcher import fetch_klines
from .compare_strategies import compare_strategies
from .advanced_rl import LSTMTrendModel


SYMBOL = "SOLUSDC"


def load_sol_data(limit: int = 500) -> pd.DataFrame:
    """Return historical klines for SOLUSDC, using cached CSV if available."""
    df = fetch_klines(SYMBOL, interval="1h", limit=limit)
    return df


def analyze_strategies(df: pd.DataFrame) -> dict[str, float]:
    """Return PnL for supported strategies on provided data."""
    if df.empty:
        raise ValueError("no data for analysis")
    return compare_strategies(df)


def ai_trade_decision(df: pd.DataFrame) -> str:
    """Return 'BUY' or 'SELL' based on LSTM price prediction."""
    if len(df) < 10:
        raise ValueError("insufficient data for AI decision")
    model = LSTMTrendModel.create(window=5)
    closes = df["close"].astype(float)
    model.fit(closes, epochs=1)
    pred = model.predict_next(closes.iloc[-5:])
    last_close = float(closes.iloc[-1])
    return "BUY" if pred > last_close else "SELL"
