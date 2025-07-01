"""Dash control panel for optimizer metrics and bot status."""

from __future__ import annotations

from pathlib import Path
import pandas as pd
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

from .monitor import MONITOR_FILE


BOT_STATUS = "Stopped"


def run_dashboard(path: str | Path = MONITOR_FILE) -> Dash:
    """Return a Dash app with metrics from ``path`` and simple controls."""
    df = pd.read_csv(path, names=["timestamp", "name", "value"])
    if df.empty:
        raise ValueError("metrics file is empty")
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    pivot = df.pivot(index="timestamp", columns="name", values="value")
    pivot = pivot.reset_index()

    app = Dash(__name__)
    fig = px.line(pivot, x="timestamp", y=pivot.columns[1:])
    app.layout = html.Div([
        html.Div(
            [
                html.Label("API Key"),
                dcc.Input(id="api-key", type="text"),
                html.Label("API Secret"),
                dcc.Input(id="api-secret", type="password"),
                html.Label("Links"),
                dcc.Textarea(id="links"),
                html.Div(id="status", children=f"Status: {BOT_STATUS}"),
                html.Button("Toggle", id="toggle-btn"),
            ]
        ),
        dcc.Graph(figure=fig),
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
