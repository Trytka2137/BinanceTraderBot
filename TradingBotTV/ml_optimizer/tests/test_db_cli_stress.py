import os
import sys
import sqlite3
import subprocess
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[3]


def _run_cli(args, env):
    cmd = [sys.executable, '-m', 'TradingBotTV.ml_optimizer.db_cli'] + args
    subprocess.run(cmd, check=True, env=env)


def test_db_cli_handles_many_trades(tmp_path):
    db = tmp_path / 'db.sqlite'
    env = os.environ.copy()
    env['PYTHONPATH'] = str(ROOT_DIR)
    _run_cli(['init', '--path', str(db)], env)
    for i in range(50):
        _run_cli([
            'trade', f'2024-01-01T00:00:{i:02d}', 'BTCUSDT', 'BUY', '1', '100',
            '--path', str(db)
        ], env)
    with sqlite3.connect(db) as conn:
        count = conn.execute('SELECT COUNT(*) FROM trades').fetchone()[0]
    assert count == 50
