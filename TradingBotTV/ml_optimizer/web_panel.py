"""Dash control panel for optimizer metrics and bot status."""

from __future__ import annotations

from pathlib import Path
import pandas as pd
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

from .monitor import MONITOR_FILE


BOT_STATUS = "Stopped"


def run_dashboard(
    path: str | Path = MONITOR_FILE,
    extra_charts: bool = True,
    include_credentials: bool = True,
    risk_charts: bool = False,
    tradingview_url: str | None = None,
) -> Dash:
    """Return a Dash app with metrics from ``path`` and simple controls.

    If ``tradingview_url`` is provided, an iframe with the given address is
    appended below the charts.
    """
    df = pd.read_csv(path, names=["timestamp", "name", "value"])
    if df.empty:
        raise ValueError("metrics file is empty")
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    pivot = df.pivot(index="timestamp", columns="name", values="value")
    pivot = pivot.reset_index()

    app = Dash(__name__)
    fig = px.line(pivot, x="timestamp", y=pivot.columns[1:])
    charts = [dcc.Graph(figure=fig)]
    if extra_charts and "pnl" in pivot.columns:
        fig2 = px.bar(pivot, x="timestamp", y="pnl", title="PnL")
        charts.append(dcc.Graph(figure=fig2))
    if risk_charts and "pnl" in pivot.columns:
        from .visualizer import plot_risk_indicators

        risk_fig = plot_risk_indicators(path)
        charts.append(dcc.Graph(figure=risk_fig))
    if tradingview_url:
        charts.append(
            html.Iframe(
                src=tradingview_url,
                style={"border": "0", "width": "100%", "height": "600px"},
            )
        )

    controls = []
    if include_credentials:
        controls.extend(
            [
                html.Label("API Key"),
                dcc.Input(id="api-key", type="text"),
                html.Label("API Secret"),
                dcc.Input(id="api-secret", type="password"),
                html.Label("API Passphrase"),
                dcc.Input(id="api-pass", type="password"),
            ]
        )
    controls.extend(
        [
            html.Label("Links"),
            dcc.Textarea(id="links"),
            html.Div(id="status", children=f"Status: {BOT_STATUS}"),
            html.Button("Toggle", id="toggle-btn"),
        ]
    )

    app.layout = html.Div([
        html.Div(controls),
        *charts,
    ])

    @app.callback(
        Output("status", "children"), Input("toggle-btn", "n_clicks")
    )
    def _toggle(n: int | None) -> str:
        global BOT_STATUS
        if n:
            BOT_STATUS = "Running" if BOT_STATUS == "Stopped" else "Stopped"
        return f"Status: {BOT_STATUS}"

    return app
