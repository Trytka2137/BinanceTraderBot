"""Network connectivity helpers for `ml_optimizer`."""

from __future__ import annotations

import time
import asyncio
import aiohttp
import requests
from requests.adapters import HTTPAdapter, Retry

from .logger import get_logger

logger = get_logger(__name__)


def check_connectivity(url: str, retries: int = 3, timeout: int = 5) -> bool:
    """Return ``True`` if ``url`` responds within ``timeout`` seconds.

    The request is retried ``retries`` times on failures. Only a HEAD
    request is sent to keep traffic minimal.
    """
    session = requests.Session()
    session.mount(
        "http://",
        HTTPAdapter(
            max_retries=Retry(
                total=retries,
                backoff_factor=1,
                status_forcelist=[500, 502, 503, 504],
                allowed_methods=["HEAD", "GET"],
            )
        ),
    )
    session.mount(
        "https://",
        HTTPAdapter(
            max_retries=Retry(
                total=retries,
                backoff_factor=1,
                status_forcelist=[500, 502, 503, 504],
                allowed_methods=["HEAD", "GET"],
            )
        ),
    )

    for attempt in range(retries):
        try:
            resp = session.head(url, timeout=timeout)
            logger.debug(
                "Connectivity check to %s status %s",
                url,
                resp.status_code,
            )
            return True
        except requests.RequestException as exc:  # pragma: no cover - network
            logger.error(
                "Connectivity check failed (attempt %s/%s) for %s: %s",
                attempt + 1,
                retries,
                url,
                exc,
            )
            if attempt == retries - 1:
                return False
            time.sleep(2 ** attempt)
    return False

async def async_check_connectivity(
    url: str,
    retries: int = 3,
    timeout: int = 5,
) -> bool:
    """Asynchronous version of :func:`check_connectivity`."""

    for attempt in range(retries):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.head(url, timeout=timeout) as resp:
                    logger.debug(
                        "Connectivity check to %s status %s",
                        url,
                        resp.status,
                    )
                    return True
        except Exception as exc:  # pragma: no cover - network
            logger.error(
                "Async connectivity check failed (attempt %s/%s) for %s: %s",
                attempt + 1,
                retries,
                url,
                exc,
            )
            if attempt == retries - 1:
                return False
            await asyncio.sleep(2 ** attempt)
    return False

if __name__ == "__main__":  # pragma: no cover - manual usage
    import argparse

    parser = argparse.ArgumentParser(description="Check network access")
    parser.add_argument("url", help="Endpoint URL to test")
    args = parser.parse_args()

    ok = check_connectivity(args.url)
    if ok:
        print(f"Connection to {args.url} succeeded")
    else:
        print(f"Unable to reach {args.url}")
