import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from TradingBotTV.ml_optimizer import data_fetcher  # noqa: E402


def test_fetch_coingecko_market_chart(monkeypatch):
    class DummyResp:
        def __init__(self, data):
            self._data = data

        def raise_for_status(self):
            pass

        def json(self):
            return self._data

    class DummySession:
        def mount(self, *a, **kw):
            pass

        def get(self, url, timeout=10):
            assert "market_chart" in url
            return DummyResp({"prices": [[0, 10], [1, 11]]})

    monkeypatch.setattr(
        data_fetcher.requests,
        "Session",
        lambda: DummySession(),
    )
    df = data_fetcher.fetch_coingecko_market_chart("bitcoin")
    assert list(df["close"]) == [10, 11]
