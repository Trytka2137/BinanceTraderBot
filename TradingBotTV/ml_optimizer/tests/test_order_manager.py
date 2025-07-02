from TradingBotTV.ml_optimizer import (
    limit_price_from_spread,
    adjust_order_price,
)


def test_limit_price_from_spread_buy():
    price = limit_price_from_spread(100.0, 101.0, "buy", 0.5)
    assert 100.0 < price <= 101.0


def test_adjust_order_price_no_change():
    new_price = adjust_order_price(100.5, 100.0, 101.0, "buy", 0.1)
    assert new_price >= 100.5
