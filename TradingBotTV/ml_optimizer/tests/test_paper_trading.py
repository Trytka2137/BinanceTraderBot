import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from TradingBotTV.ml_optimizer.paper_trading import PaperAccount  # noqa: E402


def test_buy_and_sell_updates_balance_and_position():
    account = PaperAccount(100)
    account.execute_order("BTCUSDT", "BUY", 1, 10)
    assert account.balance == 90
    assert account.get_position("BTCUSDT") == 1
    account.execute_order("BTCUSDT", "SELL", 1, 12)
    assert account.balance == 102
    assert account.get_position("BTCUSDT") == 0


def test_stress_many_orders():
    account = PaperAccount(1000)
    price = 5
    for _ in range(50):
        account.execute_order("ETHUSDT", "BUY", 1, price)
        account.execute_order("ETHUSDT", "SELL", 1, price)
    assert account.balance == 1000
    assert account.get_position("ETHUSDT") == 0
