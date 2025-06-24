import json

import numpy as np

from .data_fetcher import fetch_klines
from .backtest import backtest_strategy

STATE_PATH = 'rl_state.json'

def load_state():
    try:
        with open(STATE_PATH, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_state(state):
    with open(STATE_PATH, 'w') as f:
        json.dump(state, f)

def train(symbol, episodes=10):
    state = load_state()
    q = state.get('q', {})
    for _ in range(episodes):
        buy = np.random.randint(20, 40)
        sell = np.random.randint(60, 80)
        df = fetch_klines(symbol, interval='1h', limit=500)
        pnl = backtest_strategy(df, rsi_buy_threshold=buy, rsi_sell_threshold=sell)
        key = f'{buy}-{sell}'
        q[key] = max(q.get(key, -np.inf), pnl)
    best_key = max(q, key=q.get)
    best_buy, best_sell = map(int, best_key.split('-'))
    save_state({'q': q, 'best_buy': best_buy, 'best_sell': best_sell})
    print(f'Best params: {best_buy} {best_sell}')
    return best_buy, best_sell

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print('Usage: python rl_optimizer.py SYMBOL')
        sys.exit(1)
    train(sys.argv[1])
