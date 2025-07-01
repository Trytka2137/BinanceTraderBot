import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from TradingBotTV.ml_optimizer import alerts  # noqa: E402


def test_send_telegram_message(monkeypatch):
    called = {}

    def fake_post(url, data, timeout):
        called['url'] = url
        called['data'] = data
        return type('Resp', (), {'status_code': 200})()

    monkeypatch.setattr("requests.post", fake_post)
    alerts.send_telegram_message("hi", token="t", chat_id="c")
    assert called['data']['text'] == "hi"
