import sys
import sqlite3
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from TradingBotTV.ml_optimizer import database  # noqa: E402


def test_store_metric(tmp_path):
    db = tmp_path / "m.db"
    database.init_db(db)
    database.store_metric("2024-01-01", "m", 1.0, db)
    with sqlite3.connect(db) as conn:
        row = conn.execute("SELECT name, value FROM metrics").fetchone()
    assert row == ("m", 1.0)
