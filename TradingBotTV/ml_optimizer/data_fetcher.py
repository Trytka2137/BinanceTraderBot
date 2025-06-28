from pathlib import Path

import aiohttp
import pandas as pd
import requests
from requests.adapters import HTTPAdapter, Retry
import time
import asyncio

from .logger import get_logger

logger = get_logger(__name__)

DATA_DIR = Path(__file__).with_name('data')


def fetch_klines(
    symbol: str,
    interval: str = "1h",
    limit: int = 1000,
    retries: int = 3,
):
    """Return OHLC data for ``symbol``.

    When network calls fail ``retries`` times, cached CSV data is used if
    available. Returned DataFrame always contains ``open_time`` and ``close``
    columns.
    """
    url = (
        "https://api.binance.com/api/v3/klines"
        f"?symbol={symbol}&interval={interval}&limit={limit}"
    )
    csv_path = DATA_DIR / f"{symbol}_{interval}.csv"
    session = requests.Session()
    session.mount(
        "https://",
        HTTPAdapter(
            max_retries=Retry(
                total=retries,
                backoff_factor=1,
                status_forcelist=[500, 502, 503, 504],
                allowed_methods=["GET"],
            )
        ),
    )
    for attempt in range(retries):
        try:
            response = session.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            break
        except requests.RequestException as e:
            logger.error(
                "Error fetching klines (attempt %s/%s): %s",
                attempt + 1,
                retries,
                e,
            )
            if attempt == retries - 1:
                if csv_path.exists():
                    logger.info("Loading cached data from %s", csv_path)
                    df = pd.read_csv(csv_path)
                    df["open_time"] = pd.to_datetime(df["open_time"])
                    return df[["open_time", "close"]]
                return pd.DataFrame(columns=["open_time", "close"])
            time.sleep(2 ** attempt)

    df = pd.DataFrame(
        data,
        columns=[
            "open_time",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "close_time",
            "quote_asset_volume",
            "number_of_trades",
            "taker_buy_base_asset_volume",
            "taker_buy_quote_asset_volume",
            "ignore",
        ],
    )

    df['close'] = df['close'].astype(float)
    df['open_time'] = pd.to_datetime(df['open_time'], unit='ms')
    DATA_DIR.mkdir(exist_ok=True)
    df.to_csv(csv_path, index=False)
    return df[['open_time', 'close']]


async def async_fetch_klines(
    symbol: str,
    interval: str = "1h",
    limit: int = 1000,
    retries: int = 3,
):
    """Async version of :func:`fetch_klines` supporting ``retries``."""
    url = (
        "https://api.binance.com/api/v3/klines"
        f"?symbol={symbol}&interval={interval}&limit={limit}"
    )
    csv_path = DATA_DIR / f"{symbol}_{interval}.csv"
    data = None
    for attempt in range(retries):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=10) as resp:
                    resp.raise_for_status()
                    data = await resp.json()
            break
        except Exception as e:  # pragma: no cover - network failure
            logger.error(
                "Error fetching klines (attempt %s/%s): %s",
                attempt + 1,
                retries,
                e,
            )
            if attempt == retries - 1:
                if csv_path.exists():
                    logger.info("Loading cached data from %s", csv_path)
                    df = pd.read_csv(csv_path)
                    df["open_time"] = pd.to_datetime(df["open_time"])
                    return df[["open_time", "close"]]
                return pd.DataFrame(columns=["open_time", "close"])
            await asyncio.sleep(2 ** attempt)

    df = pd.DataFrame(
        data,
        columns=[
            "open_time",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "close_time",
            "quote_asset_volume",
            "number_of_trades",
            "taker_buy_base_asset_volume",
            "taker_buy_quote_asset_volume",
            "ignore",
        ],
    )
    df["close"] = df["close"].astype(float)
    df["open_time"] = pd.to_datetime(df["open_time"], unit="ms")
    DATA_DIR.mkdir(exist_ok=True)
    df.to_csv(csv_path, index=False)
    return df[["open_time", "close"]]


def fetch_coingecko_market_chart(
    coin_id: str,
    vs_currency: str = "usd",
    days: int = 1,
    interval: str = "hourly",
    retries: int = 3,
) -> pd.DataFrame:
    """Return price data from CoinGecko market chart endpoint.

    The data is cached to ``data/`` so repeated calls work offline if the
    network is unavailable.
    """
    url = (
        "https://api.coingecko.com/api/v3/coins/"
        f"{coin_id}/market_chart"
        f"?vs_currency={vs_currency}&days={days}&interval={interval}"
    )
    csv_path = DATA_DIR / (
        f"coingecko_{coin_id}_{vs_currency}_{days}_{interval}.csv"
    )
    session = requests.Session()
    session.mount(
        "https://",
        HTTPAdapter(
            max_retries=Retry(
                total=retries,
                backoff_factor=1,
                status_forcelist=[500, 502, 503, 504],
                allowed_methods=["GET"],
            )
        ),
    )
    data = None
    # Try network request with retries and fall back to cached CSV
    for attempt in range(retries):
        try:
            resp = session.get(url, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            break
        except requests.RequestException as exc:
            logger.error(
                "Error fetching CoinGecko data (attempt %s/%s): %s",
                attempt + 1,
                retries,
                exc,
            )
            if attempt == retries - 1:
                if csv_path.exists():
                    logger.info("Loading cached data from %s", csv_path)
                    df = pd.read_csv(csv_path)
                    df["open_time"] = pd.to_datetime(df["open_time"])
                    return df[["open_time", "close"]]
                return pd.DataFrame(columns=["open_time", "close"])
            time.sleep(2 ** attempt)
    prices = data.get("prices", []) if data else []
    df = pd.DataFrame(prices, columns=["timestamp", "close"])
    df["open_time"] = pd.to_datetime(df["timestamp"], unit="ms")
    DATA_DIR.mkdir(exist_ok=True)
    df[["open_time", "close"]].to_csv(csv_path, index=False)
    return df[["open_time", "close"]]
