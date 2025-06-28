import pandas as pd


def bollinger_bands(
    series: pd.Series, window: int = 20, num_std: int = 2
) -> pd.DataFrame:
    """Return Bollinger Bands for ``series``."""
    sma = series.rolling(window=window).mean()
    std = series.rolling(window=window).std()
    upper = sma + num_std * std
    lower = sma - num_std * std
    return pd.DataFrame({'sma': sma, 'upper': upper, 'lower': lower})


def stochastic_oscillator(
    high: pd.Series,
    low: pd.Series,
    close: pd.Series,
    k_period: int = 14,
    d_period: int = 3,
) -> pd.DataFrame:
    """Return Stochastic Oscillator %K and %D."""
    lowest_low = low.rolling(window=k_period).min()
    highest_high = high.rolling(window=k_period).max()
    percent_k = 100 * (close - lowest_low) / (highest_high - lowest_low)
    percent_d = percent_k.rolling(window=d_period).mean()
    return pd.DataFrame({'%K': percent_k, '%D': percent_d})


def order_book_imbalance(bids: pd.Series, asks: pd.Series) -> float:
    """Return simple order book imbalance from bid/ask volumes."""
    total_bid = bids.sum()
    total_ask = asks.sum()
    if total_bid + total_ask == 0:
        return 0.0
    return (total_bid - total_ask) / (total_bid + total_ask)
