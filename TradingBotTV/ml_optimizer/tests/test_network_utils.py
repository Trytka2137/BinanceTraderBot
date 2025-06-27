import sys
from pathlib import Path
from requests import RequestException

ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from TradingBotTV.ml_optimizer.network_utils import (  # noqa: E402
    check_connectivity,
)




def test_check_connectivity_success(monkeypatch):
    def head(url, timeout):
        class Resp:
            status_code = 200
        return Resp()
    session = type('S', (), {
        'head': staticmethod(head),
        'mount': lambda *a, **k: None,
    })
    monkeypatch.setattr('requests.Session', lambda: session)
    assert check_connectivity('http://example.com')


def test_check_connectivity_failure(monkeypatch):
    def head(url, timeout):
        raise RequestException('fail')
    session = type('S', (), {
        'head': staticmethod(head),
        'mount': lambda *a, **k: None,
    })
    monkeypatch.setattr('requests.Session', lambda: session)
    assert not check_connectivity('http://example.com', retries=2)

