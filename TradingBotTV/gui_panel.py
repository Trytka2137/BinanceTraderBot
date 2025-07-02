"""Simple desktop control panel for the trading bot."""

from __future__ import annotations

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


def create_app(
    metrics_path: Path = MONITOR_FILE,
    opt_log: Path = OPT_LOG_FILE,
    bot_log: Path = BOT_LOG_FILE,
) -> tk.Tk:
    """Return a :class:`tkinter.Tk` control panel."""
    root = tk.Tk()
    root.title("BinanceTraderBot")

    trading_var = tk.BooleanVar(value=True)
    training_var = tk.BooleanVar(value=False)

    frame = tk.Frame(root)
    frame.pack(pady=5)

    def toggle_trading() -> None:
        try:
            requests.post("http://localhost:5001/toggle", timeout=2)
        except Exception:
            pass
        trading_var.set(not trading_var.get())

    def toggle_training() -> None:
        training_var.set(not training_var.get())

    tk.Checkbutton(
        frame, text="Trading", variable=trading_var, command=toggle_trading
    ).pack(side=tk.LEFT, padx=5)
    tk.Checkbutton(
        frame, text="Training", variable=training_var, command=toggle_training
    ).pack(side=tk.LEFT, padx=5)

    log_text = ScrolledText(root, height=10, width=80)
    log_text.pack(padx=5, pady=5, fill=tk.BOTH, expand=False)

    def refresh_logs() -> None:
        texts: list[str] = []
        for path in (opt_log, bot_log):
            if path.exists():
                texts.append(path.read_text())
        log_text.delete("1.0", tk.END)
        log_text.insert(tk.END, "\n".join(texts))
        root.after(5000, refresh_logs)

    refresh_logs()

    try:
        fig = plot_metrics(metrics_path)
    except Exception:
        fig = plt.figure()
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    return root


if __name__ == "__main__":
    app = create_app()
    app.mainloop()
