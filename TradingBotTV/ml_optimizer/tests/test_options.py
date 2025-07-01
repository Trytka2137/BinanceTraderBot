import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from TradingBotTV.ml_optimizer import options  # noqa: E402


def test_black_scholes_price():
    price = options.black_scholes_price(100, 100, 1, 0.05, 0.2)
    assert price > 0


def test_straddle_strategy():
    res = options.straddle_strategy(100, 100, 1, 0.05, 0.2)
    assert res["total"] == res["call"] + res["put"]


def test_option_greeks():
    greeks = options.option_greeks(100, 100, 1, 0.05, 0.2)
    assert all(k in greeks for k in ["delta", "gamma", "vega", "theta", "rho"])
    assert greeks["gamma"] > 0
