import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from TradingBotTV.ml_optimizer import fundamental  # noqa: E402


def test_cache_fundamental_data(monkeypatch, tmp_path):
    monkeypatch.setattr(
        "TradingBotTV.ml_optimizer.fundamental.fetch_coinmarketcap_data",
        lambda s: {"price": 1},
    )
    monkeypatch.setattr(
        "TradingBotTV.ml_optimizer.fundamental.fetch_coingecko_market_data",
        lambda s: {"price": 1},
    )
    path = tmp_path / "data.json"
    data = fundamental.cache_fundamental_data("BTC", path)
    assert path.exists()
    assert "cmc" in data and "cg" in data
