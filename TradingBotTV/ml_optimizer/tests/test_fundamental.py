import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from TradingBotTV.ml_optimizer import fundamental  # noqa: E402


class DummyResponse:
    def __init__(self, data):
        self._data = data

    def raise_for_status(self):
        pass

    def json(self):
        return self._data


def test_fetch_coinmarketcap_data(monkeypatch):
    def dummy_get(url, headers=None, params=None, timeout=10):
        payload = {"data": {"BTC": {"quote": {"USD": {"price": 100}}}}}
        return DummyResponse(payload)

    monkeypatch.setattr("requests.get", dummy_get)
    data = fundamental.fetch_coinmarketcap_data("BTC", api_key="x")
    assert "data" in data


def test_fetch_github_activity(monkeypatch):
    def dummy_get(url, timeout=10):
        payload = {
            "stargazers_count": 1,
            "forks_count": 2,
            "open_issues_count": 0,
        }
        return DummyResponse(payload)

    monkeypatch.setattr("requests.get", dummy_get)
    stats = fundamental.fetch_github_activity("octocat/Hello-World")
    assert stats["stars"] == 1
