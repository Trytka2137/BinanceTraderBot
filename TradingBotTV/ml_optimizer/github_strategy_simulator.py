"""Clone an external GitHub repo with a simple strategy definition and run a
backtest using local market data.

Expected repository layout:
    strategy.json

strategy.json example::
    {
        "rsi_buy_threshold": 30,
        "rsi_sell_threshold": 70
    }

Usage:
    python github_strategy_simulator.py <repo_url> <symbol>

If the environment lacks network access, you can provide a local path
instead of a URL.
"""

import json
import os
import subprocess
import sys
from tempfile import TemporaryDirectory

from .data_fetcher import fetch_klines
from .backtest import backtest_strategy
from .logger import get_logger


logger = get_logger(__name__)


def clone_repo(src: str, dst: str) -> None:
    """Clone *src* into directory *dst*.

    If *src* is a local path, it is copied using ``git clone`` as well.
    Errors are printed and propagated as
    :class:`subprocess.CalledProcessError`.
    """
    logger.info("Cloning repository %s...", src)
    subprocess.run(["git", "clone", "--depth", "1", src, dst], check=True)


def load_strategy(repo_path: str) -> dict:
    """Return strategy configuration loaded from ``strategy.json``."""
    path = os.path.join(repo_path, "strategy.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def simulate_strategy(repo: str, symbol: str) -> None:
    """Backtest strategy from *repo* for the given *symbol* and print PnL."""
    with TemporaryDirectory() as tmp:
        try:
            clone_repo(repo, tmp)
        except subprocess.CalledProcessError as exc:
            logger.error("Error cloning repo: %s", exc)
            return
        try:
            cfg = load_strategy(tmp)
        except FileNotFoundError:
            logger.error("strategy.json not found in repository")
            return

        buy = int(cfg.get("rsi_buy_threshold", 30))
        sell = int(cfg.get("rsi_sell_threshold", 70))

        df = fetch_klines(symbol, interval="1h", limit=500)
        if df.empty:
            logger.warning("No data fetched for backtest")
            return
        pnl = backtest_strategy(
            df,
            rsi_buy_threshold=buy,
            rsi_sell_threshold=sell,
        )
        logger.info("Backtest result for %s: PnL=%s", symbol, pnl)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        logger.error(
            "Usage: python github_strategy_simulator.py <repo_url> <symbol>"
        )
        sys.exit(1)
    simulate_strategy(sys.argv[1], sys.argv[2])
