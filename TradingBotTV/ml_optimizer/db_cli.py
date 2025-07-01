from __future__ import annotations

import argparse

from .database import DB_FILE, init_db, store_trade, store_metric


def main() -> None:
    parser = argparse.ArgumentParser(description="Database helper")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_init = sub.add_parser("init")
    p_init.add_argument("--path", default=str(DB_FILE))

    p_trade = sub.add_parser("trade")
    p_trade.add_argument("timestamp")
    p_trade.add_argument("symbol")
    p_trade.add_argument("side")
    p_trade.add_argument("quantity", type=float)
    p_trade.add_argument("price", type=float)
    p_trade.add_argument("--path", default=str(DB_FILE))

    p_metric = sub.add_parser("metric")
    p_metric.add_argument("timestamp")
    p_metric.add_argument("name")
    p_metric.add_argument("value", type=float)
    p_metric.add_argument("--path", default=str(DB_FILE))

    args = parser.parse_args()

    if args.cmd == "init":
        init_db(args.path)
    elif args.cmd == "trade":
        store_trade(
            args.timestamp,
            args.symbol,
            args.side,
            args.quantity,
            args.price,
            args.path,
        )
    elif args.cmd == "metric":
        store_metric(args.timestamp, args.name, args.value, args.path)


if __name__ == "__main__":  # pragma: no cover - CLI entry
    main()
