import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV


def _create_features(series: pd.Series) -> pd.DataFrame:
    """Return simple return-based features for ``series``."""
    return pd.DataFrame({
        "ret_1": series.pct_change(),
        "ret_5": series.pct_change(5),
    }).fillna(0)


def train_predictive_model(df: pd.DataFrame) -> RandomForestClassifier:
    """Train a RandomForest model predicting next price direction."""
    X = _create_features(df["close"])
    y = (df["close"].shift(-1) > df["close"]).astype(int)[:-1]
    X = X[:-1]
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    return model


def optimize_predictive_model(
    df: pd.DataFrame,
    param_grid: dict,
) -> RandomForestClassifier:
    """Grid search best parameters for a RandomForest model."""
    X = _create_features(df["close"])
    y = (df["close"].shift(-1) > df["close"]).astype(int)[:-1]
    X = X[:-1]
    base = RandomForestClassifier(random_state=42)
    search = GridSearchCV(base, param_grid, cv=3, n_jobs=1)
    search.fit(X, y)
    return search.best_estimator_


def backtest_tick_strategy(
    df: pd.DataFrame,
    model,
    slippage: float = 0.0,
    fee: float = 0.0,
) -> float:
    """Backtest predictions on tick/1-second data with slippage and fees."""
    features = _create_features(df["price"])
    preds = model.predict(features)
    pnl = 0.0
    position = 0
    entry = 0.0
    for i in range(len(preds) - 1):
        price = df["price"].iloc[i]
        if position == 0 and preds[i] == 1:
            entry = price * (1 + slippage)
            pnl -= entry * fee
            position = 1
        elif position == 1 and preds[i] == 0:
            exit_price = price * (1 - slippage)
            pnl += exit_price - entry - exit_price * fee
            position = 0
    if position == 1:
        exit_price = df["price"].iloc[-1] * (1 - slippage)
        pnl += exit_price - entry - exit_price * fee
    return pnl
