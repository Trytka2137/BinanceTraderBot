import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from TradingBotTV.ml_optimizer import database  # noqa: E402


def test_fetch_functions(tmp_path):
    db = tmp_path / "db.sqlite"
    database.init_db(db)
    database.store_trade("t", "BTC", "BUY", 1.0, 100.0, db)
    database.store_metric("t", "pnl", 1.0, db)
    trades = database.fetch_trades(db)
    metrics = database.fetch_metrics(db)
    assert trades[0][1:3] == ("BTC", "BUY")
    assert metrics[0][1:] == ("pnl", 1.0)
