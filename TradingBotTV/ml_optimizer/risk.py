import pandas as pd


def kelly_fraction(win_prob: float, win_loss_ratio: float) -> float:
    """Return Kelly optimal fraction of capital to risk."""
    if not 0 < win_prob < 1:
        raise ValueError("win_prob must be in (0, 1)")
    if win_loss_ratio <= 0:
        raise ValueError("win_loss_ratio must be positive")
    q = 1 - win_prob
    return (win_prob / win_loss_ratio) - (q / win_loss_ratio)


def value_at_risk(returns: pd.Series, level: float = 0.05) -> float:
    """Return Value at Risk (VaR) at given confidence level."""
    if not 0 < level < 1:
        raise ValueError("level must be in (0, 1)")
    if returns.empty:
        raise ValueError("returns series is empty")
    return -returns.quantile(level)
