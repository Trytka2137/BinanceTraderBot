"""Option pricing utilities using Black-Scholes."""
from math import log, sqrt, exp
from typing import Dict

from scipy.stats import norm


def black_scholes_price(
    spot: float,
    strike: float,
    time: float,
    rate: float,
    vol: float,
    option_type: str = "call",
) -> float:
    """Return Black-Scholes option price for a European option."""
    if time <= 0 or vol <= 0:
        raise ValueError("time and vol must be positive")
    d1 = (
        log(spot / strike) + (rate + vol ** 2 / 2) * time
    ) / (vol * sqrt(time))
    d2 = d1 - vol * sqrt(time)
    if option_type == "call":
        return spot * norm.cdf(d1) - strike * exp(-rate * time) * norm.cdf(d2)
    elif option_type == "put":
        return (
            strike * exp(-rate * time) * norm.cdf(-d2)
            - spot * norm.cdf(-d1)
        )
    else:
        raise ValueError("option_type must be 'call' or 'put'")


def straddle_strategy(
    spot: float,
    strike: float,
    time: float,
    rate: float,
    vol: float,
) -> Dict[str, float]:
    """Return prices for a straddle (call + put)."""
    call = black_scholes_price(spot, strike, time, rate, vol, "call")
    put = black_scholes_price(spot, strike, time, rate, vol, "put")
    return {"call": call, "put": put, "total": call + put}


def option_greeks(
    spot: float,
    strike: float,
    time: float,
    rate: float,
    vol: float,
    option_type: str = "call",
) -> Dict[str, float]:
    """Return basic option Greeks for a European option."""
    if time <= 0 or vol <= 0:
        raise ValueError("time and vol must be positive")
    d1 = (
        log(spot / strike) + (rate + vol ** 2 / 2) * time
    ) / (vol * sqrt(time))
    d2 = d1 - vol * sqrt(time)
    delta = norm.cdf(d1) if option_type == "call" else norm.cdf(d1) - 1
    gamma = norm.pdf(d1) / (spot * vol * sqrt(time))
    vega = spot * norm.pdf(d1) * sqrt(time)
    if option_type == "call":
        theta = (
            -spot * norm.pdf(d1) * vol / (2 * sqrt(time))
            - rate * strike * exp(-rate * time) * norm.cdf(d2)
        )
        rho = strike * time * exp(-rate * time) * norm.cdf(d2)
    elif option_type == "put":
        theta = (
            -spot * norm.pdf(d1) * vol / (2 * sqrt(time))
            + rate * strike * exp(-rate * time) * norm.cdf(-d2)
        )
        rho = -strike * time * exp(-rate * time) * norm.cdf(-d2)
    else:
        raise ValueError("option_type must be 'call' or 'put'")
    return {
        "delta": delta,
        "gamma": gamma,
        "vega": vega,
        "theta": theta,
        "rho": rho,
    }
