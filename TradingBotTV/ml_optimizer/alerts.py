"""Telegram alert utilities."""

from __future__ import annotations

import os
import requests


def send_telegram_message(
    message: str,
    *,
    token: str | None = None,
    chat_id: str | None = None,
) -> None:
    """Send *message* using Telegram bot API."""
    token = token or os.getenv("TELEGRAM_TOKEN")
    chat_id = chat_id or os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        raise ValueError("token and chat_id must be provided")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {"chat_id": chat_id, "text": message}
    requests.post(url, data=data, timeout=10)
