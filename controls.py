import dash_bootstrap_components as dbc
from dash import dcc, html

def get_controls() -> dbc.Card:
    return dbc.Card(
        [
            html.Div(
                [
                    dbc.Label("Regulator type"),
                    dcc.Dropdown(
                        id="regulator-type",
                        options=[
                            {"label": "PI", "value": "PI"},
                            {"label": "PID", "value": "PID"}
                        ],
                        value="PI",
                    ),
                ]
            )
        ],
        body=True,
    )
