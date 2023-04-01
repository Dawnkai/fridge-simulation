import dash_bootstrap_components as dbc
from dash import dcc, html

def get_controls(columns):
    return dbc.Card(
        [
            html.Div(
                [
                    dbc.Label("X variable"),
                    dcc.Dropdown(
                        id="x-variable",
                        options=[
                            {"label": col, "value": col} for col in columns
                        ],
                        value="sepal length (cm)",
                    ),
                ]
            ),
            html.Div(
                [
                    dbc.Label("Y variable"),
                    dcc.Dropdown(
                        id="y-variable",
                        options=[
                            {"label": col, "value": col} for col in columns
                        ],
                        value="sepal width (cm)",
                    ),
                ]
            ),
            html.Div(
                [
                    dbc.Label("Cluster count"),
                    dbc.Input(id="cluster-count", type="number", value=3),
                ]
            ),
        ],
        body=True,
    )
