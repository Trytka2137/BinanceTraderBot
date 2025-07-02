"""Discord alert utilities."""

from __future__ import annotations

import os
import requests


def send_discord_message(
    message: str,
    *,
    webhook_url: str | None = None,
) -> None:
    """Send ``message`` to a Discord channel using a webhook."""
    webhook_url = webhook_url or os.getenv("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        raise ValueError("webhook_url must be provided")
    data = {"content": message}
    requests.post(webhook_url, json=data, timeout=10)
