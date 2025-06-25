import json
import os
import subprocess
import sys
from pathlib import Path

import pandas as pd

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from TradingBotTV.ml_optimizer import github_strategy_simulator


def test_simulate_strategy_local_repo(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    subprocess.run(["git", "init", repo], check=True)
    strategy = {"rsi_buy_threshold": 25, "rsi_sell_threshold": 75}
    (repo / "strategy.json").write_text(json.dumps(strategy))
    subprocess.run(["git", "-C", str(repo), "add", "strategy.json"], check=True)
    env = dict(os.environ,
               GIT_AUTHOR_NAME="a",
               GIT_AUTHOR_EMAIL="a@b.c",
               GIT_COMMITTER_NAME="a",
               GIT_COMMITTER_EMAIL="a@b.c")
    subprocess.run(["git", "-C", str(repo), "commit", "-m", "init"], check=True, env=env)

    df = pd.DataFrame({"close": [1, 2, 3, 4, 5]})
    monkeypatch.setattr(github_strategy_simulator, "fetch_klines", lambda *a, **k: df)
    results = []
    monkeypatch.setattr(github_strategy_simulator, "backtest_strategy",
                        lambda data, rsi_buy_threshold, rsi_sell_threshold: 42)
    import builtins
    monkeypatch.setattr(builtins, "print",
                        lambda *args, **kwargs: results.append(" ".join(map(str, args))))

    github_strategy_simulator.simulate_strategy(str(repo), "BTCUSDT")

    assert any("PnL" in r for r in results)
