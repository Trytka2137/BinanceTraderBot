"""Simple database utilities for storing trades and metrics."""

from __future__ import annotations

import sqlite3
from pathlib import Path


DB_FILE = Path(__file__).resolve().parent / "state" / "metrics.db"


def init_db(db_path: str | Path = DB_FILE) -> None:
    """Create tables for trades and metrics if they do not exist."""
    db_path = Path(db_path)
    db_path.parent.mkdir(exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        cur.execute(
            "CREATE TABLE IF NOT EXISTS trades ("
            "id INTEGER PRIMARY KEY, "
            "timestamp TEXT, symbol TEXT, side TEXT, "
            "quantity REAL, price REAL)"
        )
        cur.execute(
            "CREATE TABLE IF NOT EXISTS metrics ("
            "id INTEGER PRIMARY KEY, timestamp TEXT, name TEXT, value REAL)"
        )
        conn.commit()


def store_trade(
    timestamp: str,
    symbol: str,
    side: str,
    quantity: float,
    price: float,
    db_path: str | Path = DB_FILE,
) -> None:
    """Insert a trade record into the database."""
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            "INSERT INTO trades(timestamp, symbol, side, quantity, price)"
            " VALUES (?, ?, ?, ?, ?)",
            (timestamp, symbol, side, quantity, price),
        )
        conn.commit()


def store_metric(
    timestamp: str,
    name: str,
    value: float,
    db_path: str | Path = DB_FILE,
) -> None:
    """Insert a metric record into the database."""
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            "INSERT INTO metrics(timestamp, name, value)"
            " VALUES (?, ?, ?)",
            (timestamp, name, value),
        )
        conn.commit()
