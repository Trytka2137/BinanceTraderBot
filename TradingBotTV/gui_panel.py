"""Simple desktop control panel for the trading bot."""

from __future__ import annotations

import json
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import requests

from .ml_optimizer.visualizer import plot_metrics
from .ml_optimizer.monitor import MONITOR_FILE
from .ml_optimizer.logger import LOG_FILE as OPT_LOG_FILE

BOT_LOG_FILE = Path(__file__).resolve().parent / "logs" / "bot.log"
CONFIG_FILE = Path(__file__).resolve().parent / "config" / "settings.json"


def create_app(
    metrics_path: Path = MONITOR_FILE,
    opt_log: Path = OPT_LOG_FILE,
    bot_log: Path = BOT_LOG_FILE,
) -> tk.Tk:
    """Return a :class:`tkinter.Tk` control panel."""
    root = tk.Tk()
    root.title("Trytonator2137")

    try:
        cfg = json.loads(CONFIG_FILE.read_text())
    except Exception:
        cfg = {"binance": {}, "trading": {}}

    api_key_var = tk.StringVar(
        value=cfg.get("binance", {}).get("apiKey", "")
    )
    api_secret_var = tk.StringVar(
        value=cfg.get("binance", {}).get("apiSecret", "")
    )
    symbol_var = tk.StringVar(
        value=cfg.get("trading", {}).get("symbol", "")
    )
    amount_var = tk.StringVar(
        value=str(cfg.get("trading", {}).get("amount", ""))
    )
    trading_var = tk.BooleanVar(value=True)
    training_var = tk.BooleanVar(value=False)

    frame = tk.Frame(root)
    frame.pack(pady=5)

    def toggle_trading() -> None:
        """Toggle live trading via the local dashboard."""
        try:
            requests.post("http://localhost:5001/toggle", timeout=2)
        except Exception:
            pass
        btn_text = "Stop Bot" if trading_var.get() else "Start Bot"
        toggle_btn.config(text=btn_text)

    def toggle_training() -> None:
        """Enable or disable training mode."""
        pass

    tk.Checkbutton(
        frame, text="Trading", variable=trading_var, command=toggle_trading
    ).pack(side=tk.LEFT, padx=5)
    tk.Checkbutton(
        frame, text="Training", variable=training_var, command=toggle_training
    ).pack(side=tk.LEFT, padx=5)

    def toggle_bot() -> None:
        trading_var.set(not trading_var.get())
        toggle_trading()

    toggle_btn = tk.Button(frame, text="Stop Bot", command=toggle_bot)
    toggle_btn.pack(side=tk.LEFT, padx=5)

    cfg_frame = tk.LabelFrame(root, text="Configuration")
    cfg_frame.pack(padx=5, pady=5, fill=tk.X)

    tk.Label(cfg_frame, text="API Key").grid(row=0, column=0, sticky="e")
    tk.Entry(
        cfg_frame,
        textvariable=api_key_var,
        width=40,
    ).grid(row=0, column=1, padx=5)
    tk.Label(cfg_frame, text="API Secret").grid(row=1, column=0, sticky="e")
    tk.Entry(
        cfg_frame,
        textvariable=api_secret_var,
        width=40,
        show="*",
    ).grid(row=1, column=1, padx=5)
    tk.Label(cfg_frame, text="Symbol").grid(row=2, column=0, sticky="e")
    tk.Entry(
        cfg_frame,
        textvariable=symbol_var,
        width=20,
    ).grid(row=2, column=1, sticky="w", padx=5)
    tk.Label(cfg_frame, text="Amount").grid(row=3, column=0, sticky="e")
    tk.Entry(
        cfg_frame,
        textvariable=amount_var,
        width=10,
    ).grid(row=3, column=1, sticky="w", padx=5)

    def save_config() -> None:
        data = {"binance": {}, "trading": {}}
        if CONFIG_FILE.exists():
            try:
                data = json.loads(CONFIG_FILE.read_text())
            except Exception:
                pass
        data.setdefault("binance", {})["apiKey"] = api_key_var.get().strip()
        data["binance"]["apiSecret"] = api_secret_var.get().strip()
        data.setdefault("trading", {})["symbol"] = symbol_var.get().strip()
        try:
            data["trading"]["amount"] = float(amount_var.get())
        except ValueError:
            pass
        CONFIG_FILE.write_text(json.dumps(data, indent=2))

    tk.Button(
        cfg_frame,
        text="Save",
        command=save_config,
    ).grid(row=4, column=0, columnspan=2, pady=5)
    log_text = ScrolledText(root, height=10, width=80)
    log_text.pack(padx=5, pady=5, fill=tk.BOTH, expand=False)

    cmd_text = ScrolledText(root, height=10, width=80)
    cmd_text.pack(padx=5, pady=5, fill=tk.BOTH, expand=False)

    def tail(path: Path, lines: int = 200) -> str:
        if not path.exists():
            return ""
        data = path.read_text().splitlines()[-lines:]
        return "\n".join(data)

    def refresh_logs() -> None:
        texts: list[str] = []
        for path in (opt_log, bot_log):
            snippet = tail(path)
            if snippet:
                texts.append(snippet)
        log_text.delete("1.0", tk.END)
        log_text.insert(tk.END, "\n".join(texts))
        root.after(5000, refresh_logs)

    def refresh_cmds() -> None:
        cmd_text.delete("1.0", tk.END)
        cmd_text.insert(tk.END, tail(bot_log, 50))
        root.after(3000, refresh_cmds)

    refresh_logs()
    refresh_cmds()

    try:
        fig = plot_metrics(metrics_path, recent=300)
    except Exception:
        fig = plt.figure()
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def refresh_plot() -> None:
        try:
            fig = plot_metrics(metrics_path, recent=300)
        except Exception:
            fig = plt.figure()
        canvas.figure = fig
        canvas.draw()
        root.after(10000, refresh_plot)

    refresh_plot()

    return root


if __name__ == "__main__":
    app = create_app()
    app.mainloop()
