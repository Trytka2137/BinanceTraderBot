import sys
from pathlib import Path
import asyncio
from requests import RequestException

ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from TradingBotTV.ml_optimizer.network_utils import (  # noqa: E402
    check_connectivity,
    async_check_connectivity,
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

def test_async_check_connectivity_success(monkeypatch):
    class Session:
        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            pass

        def head(self, url, timeout):
            class Resp:
                status = 200

                async def __aenter__(self_inner):
                    return self_inner

                async def __aexit__(self_inner, exc_type, exc, tb):
                    pass

            return Resp()

    monkeypatch.setattr('aiohttp.ClientSession', lambda: Session())
    assert asyncio.run(async_check_connectivity('http://example.com'))


def test_async_check_connectivity_failure(monkeypatch):
    class Session:
        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            pass

        def head(self, url, timeout):
            class Resp:
                async def __aenter__(self_inner):
                    raise Exception('fail')

                async def __aexit__(self_inner, exc_type, exc, tb):
                    pass

            return Resp()

    monkeypatch.setattr('aiohttp.ClientSession', lambda: Session())
    assert not asyncio.run(
        async_check_connectivity('http://example.com', retries=2)
    )