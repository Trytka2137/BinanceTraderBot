import sys
from data_fetcher import fetch_klines
from backtest import compare_strategies


def run(symbol):
    df = fetch_klines(symbol, interval='1h', limit=500)
    if df.empty:
        print('Brak danych do porownania')
        return
    results = compare_strategies(df)
    for name, pnl in results.items():
        print(f'{name} PnL: {pnl}')
    best = max(results, key=results.get)
    print(f'Najlepsza strategia: {best}')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Uzycie: python compare_strategies.py SYMBOL')
        sys.exit(1)
    run(sys.argv[1])
