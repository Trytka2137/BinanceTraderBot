class PaperAccount:
    """Simple paper trading account."""

    def __init__(self, balance: float):
        if balance < 0:
            raise ValueError("balance must be non-negative")
        self.balance = balance
        self.positions = {}

    def execute_order(self, symbol: str, side: str, qty: float, price: float):
        if qty <= 0 or price <= 0:
            raise ValueError("qty and price must be positive")
        if side not in ("BUY", "SELL"):
            raise ValueError("side must be BUY or SELL")
        cost = qty * price
        if side == "BUY":
            if cost > self.balance:
                raise ValueError("insufficient balance")
            self.balance -= cost
            self.positions[symbol] = self.positions.get(symbol, 0.0) + qty
        else:
            if self.positions.get(symbol, 0.0) < qty:
                raise ValueError("insufficient position")
            self.balance += cost
            self.positions[symbol] -= qty
        return {"symbol": symbol, "side": side, "qty": qty, "price": price}

    def get_position(self, symbol: str) -> float:
        return self.positions.get(symbol, 0.0)
