from TradingBotTV.ml_optimizer import (
    grid_levels,
    dca_schedule,
    scalp_signal,
    choose_strategy,
)


def test_grid_levels_length_and_order():
    levels = grid_levels(100.0, 1.0, 2)
    assert len(levels) == 4
    assert levels[0] < 100.0 < levels[-1]


def test_dca_schedule_sum():
    sched = dca_schedule(100.0, 4)
    assert len(sched) == 4
    assert abs(sum(sched) - 100.0) < 1e-9


def test_scalp_signal_buy_sell():
    prices = [1.0, 1.0, 1.0, 1.1]
    assert scalp_signal(prices, window=2) == 1
    prices[-1] = 0.9
    assert scalp_signal(prices, window=2) == -1


def test_choose_strategy_branches():
    assert choose_strategy(0.06, 0.1) == "scalping"
    assert choose_strategy(0.03, 0.1) == "grid"
    assert choose_strategy(0.01, 0.6) == "arbitrage"
    assert choose_strategy(0.01, 0.1) == "dca"
