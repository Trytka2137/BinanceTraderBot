import os
import requests
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')


def fetch_klines(symbol, interval='1h', limit=1000):
    url = (
        'https://api.binance.com/api/v3/klines'
        f'?symbol={symbol}&interval={interval}&limit={limit}'
    )
    csv_path = os.path.join(DATA_DIR, f'{symbol}_{interval}.csv')
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        print(f"Error fetching klines: {e}")
        if os.path.exists(csv_path):
            print(f'Loading cached data from {csv_path}')
            df = pd.read_csv(csv_path)
            df['open_time'] = pd.to_datetime(df['open_time'])
            return df[['open_time', 'close']]
        return pd.DataFrame(columns=['open_time', 'close'])

    df = pd.DataFrame(data, columns=[
        'open_time', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_asset_volume', 'number_of_trades',
        'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
    ])

    df['close'] = df['close'].astype(float)
    df['open_time'] = pd.to_datetime(df['open_time'], unit='ms')
    os.makedirs(DATA_DIR, exist_ok=True)
    df.to_csv(csv_path, index=False)
    return df[['open_time', 'close']]
