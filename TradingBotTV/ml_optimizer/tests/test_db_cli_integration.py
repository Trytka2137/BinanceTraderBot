import os
import sys
import sqlite3
import subprocess
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[3]


def _run_cli(args, env):
    cmd = [sys.executable, '-m', 'TradingBotTV.ml_optimizer.db_cli'] + args
    subprocess.run(cmd, check=True, env=env)


def test_db_cli_creates_and_stores(tmp_path):
    db = tmp_path / 'db.sqlite'
    env = os.environ.copy()
    env['PYTHONPATH'] = str(ROOT_DIR)
    _run_cli(['init', '--path', str(db)], env)
    _run_cli(
        [
            'trade',
            '2024-01-01T00:00:00',
            'BTCUSDT',
            'BUY',
            '1',
            '100',
            '--path',
            str(db),
        ],
        env,
    )
    _run_cli(
        [
            'metric',
            '2024-01-01T00:00:00',
            'pnl',
            '1',
            '--path',
            str(db),
        ],
        env,
    )
    with sqlite3.connect(db) as conn:
        trades = conn.execute('SELECT symbol, side FROM trades').fetchone()
        metrics = conn.execute('SELECT name, value FROM metrics').fetchone()
    assert trades == ('BTCUSDT', 'BUY')
    assert metrics == ('pnl', 1.0)
