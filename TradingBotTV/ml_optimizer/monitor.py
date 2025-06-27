"""Simple metrics recording for monitoring purposes."""

from __future__ import annotations

import csv
import datetime as _dt
from pathlib import Path

from .logger import get_logger

logger = get_logger(__name__)

MONITOR_FILE = Path(__file__).resolve().parent / "state" / "metrics.csv"


def record_metric(
    name: str,
    value: float,
    *,
    timestamp: _dt.datetime | None = None,
) -> None:
    """Append ``name`` and ``value`` with timestamp to :data:`MONITOR_FILE`."""
    if timestamp is None:
        timestamp = _dt.datetime.utcnow()
    MONITOR_FILE.parent.mkdir(exist_ok=True)
    try:
        with MONITOR_FILE.open("a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([timestamp.isoformat(), name, value])
    except Exception as exc:  # pragma: no cover - filesystem errors
        logger.error("Error recording metric %s: %s", name, exc)
