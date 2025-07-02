import pandas as pd


def kelly_fraction(win_prob: float, win_loss_ratio: float) -> float:
    """Return Kelly optimal fraction of capital to risk.

    The formula used follows ``p - (1 - p) / b`` where ``p`` is the probability
    of winning and ``b`` is the win/loss ratio. Previous versions incorrectly
    divided both terms by ``b`` which underestimated the fraction when
    ``b`` was not ``1``.
    """

    if not 0 < win_prob < 1:
        raise ValueError("win_prob must be in (0, 1)")
    if win_loss_ratio <= 0:
        raise ValueError("win_loss_ratio must be positive")

    q = 1 - win_prob
    return win_prob - q / win_loss_ratio


def value_at_risk(returns: pd.Series, level: float = 0.05) -> float:
    """Return Value at Risk (VaR) at given confidence level."""
    if not 0 < level < 1:
        raise ValueError("level must be in (0, 1)")
    if returns.empty:
        raise ValueError("returns series is empty")
    return -returns.quantile(level)


def max_drawdown(prices: pd.Series) -> float:
    """Return maximum drawdown for ``prices``."""
    if prices.empty:
        raise ValueError("prices series is empty")
    cumulative_max = prices.cummax()
    drawdowns = (prices - cumulative_max) / cumulative_max
    return drawdowns.min()


def adaptive_stop_levels(
    prices: pd.Series,
    atr_period: int = 14,
    stop_factor: float = 2.0,
    take_factor: float = 3.0,
) -> dict:
    """Return adaptive stop-loss and take-profit based on ATR."""
    if prices.empty or len(prices) < atr_period + 1:
        raise ValueError("not enough price data")
    from .backtest import compute_atr

    high = prices.shift().fillna(prices)
    low = prices.shift().fillna(prices)
    atr = compute_atr(high, low, prices, period=atr_period).iloc[-1]
    last_price = prices.iloc[-1]
    stop_loss = last_price - stop_factor * atr
    take_profit = last_price + take_factor * atr
    return {"stop_loss": stop_loss, "take_profit": take_profit}


def position_size_from_var(
    returns: pd.Series,
    capital: float,
    var_limit: float = 0.02,
    level: float = 0.05,
) -> float:
    """Return position size constrained by VaR.

    ``var_limit`` expresses the fraction of ``capital`` that may be lost with
    the given confidence level.
    """
    if capital <= 0:
        raise ValueError("capital must be positive")
    if not 0 < var_limit < 1:
        raise ValueError("var_limit must be in (0, 1)")
    var = value_at_risk(returns, level=level)
    if var <= 0:
        raise ValueError("returns must yield positive VaR")
    fraction = min(var_limit / var, 1.0)
    return capital * fraction
