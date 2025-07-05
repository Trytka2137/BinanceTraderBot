import pandas as pd
from sklearn.ensemble import IsolationForest

try:  # TensorFlow 2.x exposes Keras as a submodule
    from tensorflow import keras
    from tensorflow.keras import layers
except Exception:  # pragma: no cover - fall back to standalone Keras
    import keras  # type: ignore
    from keras import layers


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


def detect_price_anomalies(
    series: pd.Series, contamination: float = 0.05
) -> pd.Series:
    """Return boolean flags marking anomalies detected by IsolationForest."""
    if series.empty:
        raise ValueError("price series cannot be empty")
    model = IsolationForest(contamination=contamination, random_state=0)
    labels = model.fit_predict(series.values.reshape(-1, 1))
    return pd.Series(labels == -1, index=series.index)


def autoencoder_anomaly_scores(
    series: pd.Series, window: int = 10, epochs: int = 3
) -> pd.Series:
    """Return reconstruction errors from a simple autoencoder."""
    if len(series) <= window:
        raise ValueError("price series too short")
    X = []
    values = series.values.astype(float)
    for i in range(len(values) - window):
        X.append(values[i:i + window])
    X = pd.DataFrame(X).values
    model = keras.Sequential([
        layers.Dense(window // 2, activation="relu", input_shape=(window,)),
        layers.Dense(window, activation="linear"),
    ])
    model.compile(optimizer="adam", loss="mse")
    model.fit(X, X, epochs=epochs, verbose=0)
    reconstructed = model.predict(X, verbose=0)
    errors = ((X - reconstructed) ** 2).mean(axis=1)
    return pd.Series(errors, index=series.index[window:])
