import sys
from pathlib import Path
import pandas as pd

ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from TradingBotTV.ml_optimizer.web_panel import run_dashboard  # noqa: E402
from dash import html  # noqa: E402


def test_run_dashboard(tmp_path):
    csv = tmp_path / "metrics.csv"
    df = pd.DataFrame(
        {"timestamp": ["2024-01-01T00:00:00"], "name": ["m"], "value": [1]}
    )
    df.to_csv(csv, index=False, header=False)
    app = run_dashboard(csv, extra_charts=True, include_credentials=True)
    assert app.layout is not None
    controls = app.layout.children[0]
    ids = [c.id for c in controls.children if hasattr(c, "id")]
    expected = {
        "api-key",
        "api-secret",
        "api-pass",
        "links",
        "status",
        "toggle-btn",
    }
    assert expected <= set(ids)
    assert len(app.layout.children) >= 2


def test_run_dashboard_with_risk(tmp_path):
    csv = tmp_path / "metrics.csv"
    df = pd.DataFrame(
        {
            "timestamp": ["2024-01-01T00:00:00"],
            "name": ["pnl"],
            "value": [1],
        }
    )
    df.to_csv(csv, index=False, header=False)
    app = run_dashboard(csv, risk_charts=True)
    assert len(app.layout.children) >= 2


def test_run_dashboard_with_tradingview(tmp_path):
    csv = tmp_path / "metrics.csv"
    df = pd.DataFrame(
        {"timestamp": ["2024-01-01T00:00:00"], "name": ["m"], "value": [1]}
    )
    df.to_csv(csv, index=False, header=False)
    url = "https://example.com/chart"
    app = run_dashboard(csv, tradingview_url=url)
    found = False
    for comp in app.layout.children[1:]:
        if isinstance(comp, html.Iframe) and comp.src == url:
            found = True
            break
    assert found
