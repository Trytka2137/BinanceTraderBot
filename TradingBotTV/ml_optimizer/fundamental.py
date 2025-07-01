import json
from pathlib import Path
import os
import requests


def fetch_coinmarketcap_data(symbol: str, api_key: str | None = None) -> dict:
    """Return latest market data for ``symbol`` from CoinMarketCap."""
    api_key = api_key or os.getenv("COINMARKETCAP_API_KEY")
    headers = {"X-CMC_PRO_API_KEY": api_key} if api_key else {}
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    params = {"symbol": symbol}
    response = requests.get(url, headers=headers, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def fetch_coingecko_market_data(coin_id: str) -> dict:
    """Return market data for ``coin_id`` from CoinGecko."""
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()


def fetch_messari_asset_metrics(asset: str) -> dict:
    """Return asset metrics for ``asset`` from Messari."""
    url = f"https://data.messari.io/api/v1/assets/{asset}/metrics"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()


def fetch_github_activity(repo: str) -> dict:
    """Return basic GitHub repository statistics."""
    url = f"https://api.github.com/repos/{repo}"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()
    return {
        "stars": data.get("stargazers_count", 0),
        "forks": data.get("forks_count", 0),
        "open_issues": data.get("open_issues_count", 0),
    }


def cache_fundamental_data(symbol: str, path: str | Path) -> dict:
    """Fetch basic fundamental data and cache it to ``path``."""
    data = {
        "cmc": fetch_coinmarketcap_data(symbol),
        "cg": fetch_coingecko_market_data(symbol.lower()),
    }
    Path(path).write_text(json.dumps(data))
    return data
