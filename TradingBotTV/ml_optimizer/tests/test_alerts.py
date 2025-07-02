import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from TradingBotTV.ml_optimizer import alerts  # noqa: E402


def test_send_discord_message(monkeypatch):
    called = {}

    def fake_post(url, json, timeout):
        called['url'] = url
        called['data'] = json
        return type('Resp', (), {'status_code': 200})()

    monkeypatch.setattr("requests.post", fake_post)
    alerts.send_discord_message("hi", webhook_url="hook")
    assert called['data']['content'] == "hi"
