from pathlib import Path

import aiohttp
import pandas as pd
import requests

from .logger import get_logger

logger = get_logger(__name__)

DATA_DIR = Path(__file__).with_name('data')


def fetch_klines(symbol: str, interval: str = "1h", limit: int = 1000, retries: int = 3):
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
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            break
        except requests.RequestException as e:
            logger.error("Error fetching klines (attempt %s/%s): %s", attempt + 1, retries, e)
            if attempt == retries - 1:
                if csv_path.exists():
                    logger.info("Loading cached data from %s", csv_path)
                    df = pd.read_csv(csv_path)
                    df["open_time"] = pd.to_datetime(df["open_time"])
                    return df[["open_time", "close"]]
                return pd.DataFrame(columns=["open_time", "close"])

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
                "Error fetching klines (attempt %s/%s): %s", attempt + 1, retries, e
            )
            if attempt == retries - 1:
                if csv_path.exists():
                    logger.info("Loading cached data from %s", csv_path)
                    df = pd.read_csv(csv_path)
                    df["open_time"] = pd.to_datetime(df["open_time"])
                    return df[["open_time", "close"]]
                return pd.DataFrame(columns=["open_time", "close"])

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
