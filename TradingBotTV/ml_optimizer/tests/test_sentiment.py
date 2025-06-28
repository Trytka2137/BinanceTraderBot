import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from TradingBotTV.ml_optimizer import sentiment  # noqa: E402


class DummyResponse:
    def __init__(self, data):
        self._data = data

    def raise_for_status(self):
        pass

    def json(self):
        return self._data


def test_fetch_fear_greed_index(monkeypatch):
    def dummy_get(url, timeout=10):
        return DummyResponse({"data": [{"value": "55"}]})

    monkeypatch.setattr("requests.get", dummy_get)
    assert sentiment.fetch_fear_greed_index() == 55


def test_fetch_lunarcrush_score(monkeypatch):
    def dummy_get(url, params=None, timeout=10):
        return DummyResponse({"data": [{"galaxy_score": 67.0}]})

    monkeypatch.setattr("requests.get", dummy_get)
    score = sentiment.fetch_lunarcrush_score("BTC")
    assert score == 67.0
