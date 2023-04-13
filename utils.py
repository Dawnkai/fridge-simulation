"""Project utilities (UI controls, app layout and result graph), separated for readability."""

import dash_bootstrap_components as dbc
import plotly.graph_objs as go

from dash import dcc, html

def get_controls(regulator_type : str, pi_p : float = 1.0, pi_i : float = 1.0, pid_p : float = 1.0,
                 pid_i : float = 1.0, pid_d : float = 1.0) -> dbc.Card:
    """Regulator controls visible in the GUI."""
    return [
        html.Div(
            [
                dbc.Label("Proportional gain: "),
                dcc.Input(
                    id="pi-proportional",
                    min=0,
                    step=0.001,
                    value=pi_p,
                    type="number",
                    style={"marginLeft": 10}
                ),
            ],
            style={'display': 'none' if regulator_type != 'PI' else 'block'}
        ),
        html.Div(
            [
                dbc.Label("Integral gain: "),
                dcc.Input(
                    id="pi-integral",
                    min=0,
                    step=0.001,
                    value=pi_i,
                    type="number",
                    style={"marginLeft": 10}
                )
            ],
            style={'display': 'none' if regulator_type != 'PI' else 'block'}
        ),
        html.Div(
            [
                dbc.Label("Proportional coefficient: "),
                dcc.Input(
                    id="pid-proportional",
                    min=0,
                    step=0.001,
                    value=pid_p,
                    type="number",
                    style={"marginLeft": 10}
                )
            ],
            style={'display': 'none' if regulator_type != 'PID' else 'block'}
        ),
        html.Div(
            [
                dbc.Label("Integral coefficient: "),
                dcc.Input(
                    id="pid-integral",
                    min=0,
                    step=0.001,
                    value=pid_i,
                    type="number",
                    style={"marginLeft": 10}
                )
            ],
            style={'display': 'none' if regulator_type != 'PID' else 'block'}
        ),
        html.Div(
            [
                dbc.Label("Derivative coefficient: "),
                dcc.Input(
                    id="pid-derivative",
                    min=0,
                    step=0.001,
                    value=pid_d,
                    type="number",
                    style={"marginLeft": 10}
                )
            ],
            style={'display': 'none' if regulator_type != 'PID' else 'block'}
        )
    ]

def get_result_graphs(results : list) -> dcc.Tabs:
    """Graphs with simulation results."""
    signal_figure = go.Figure()
    response_figure = go.Figure()
    error_figure = go.Figure()

    for idx, result in enumerate(results):
        signal_figure.add_trace(go.Scatter(x=result[0], y=result[2], name=f"Signals ({idx})"))
        response_figure.add_trace(go.Scatter(x=result[0], y=result[3], name=f"Responses ({idx})"))
        error_figure.add_trace(go.Scatter(x=result[0], y=result[4], name=f"Errors ({idx})"))

    signal_figure.update_layout(xaxis_title="Time [s]", yaxis_title="Response [km/h]")
    response_figure.update_layout(xaxis_title="Time [s]", yaxis_title="Signal [V]")
    error_figure.update_layout(xaxis_title="Time [s]", yaxis_title="Error [V]")

    return dcc.Tabs([
        dcc.Tab(label="Signal response", children=[dcc.Graph(figure=response_figure)]),
        dcc.Tab(label="Signal", children=[dcc.Graph(figure=signal_figure)]),
        dcc.Tab(label="Error", children=[dcc.Graph(figure=error_figure)])
    ])

def get_app_layout() -> dbc.Container:
    """Application layout."""
    return dbc.Container(
        [
            dbc.Card([
                html.H1("Levitating Ball Simulation", style={"textAlign": "center", "color": "white"}),
                html.Hr(),
                dbc.Row(
                    [
                        # Window with parameters
                        dbc.Col(
                            dbc.Card(
                                [
                                    html.Div(
                                        [
                                            dbc.Label("Regulator type", style={"fontWeight": "bold"}),
                                            dcc.Dropdown(
                                                id="regulator-type",
                                                options=[
                                                    {"label": "PI", "value": "PI"},
                                                    {"label": "PID", "value": "PID"},
                                                    {"label": "Fuzzy", "value": "Fuzzy"}
                                                ],
                                                value="PI",
                                            )
                                        ]
                                    ),
                                    html.Div(
                                        [
                                            dbc.Label("Target value", style={'marginTop': 10, "fontWeight": "bold"}),
                                            html.Br(),
                                            dcc.Input(
                                                type="number",
                                                id="target-value",
                                                step=1,
                                                value=40
                                            )
                                        ]
                                    ),
                                    html.Hr(),
                                    html.Div(
                                        dbc.Card(
                                            get_controls("PI"),
                                            body=True,
                                            id="controls"
                                        )
                                    ),
                                    dbc.Button("Go", color="primary", id="start-simulation", n_clicks=0,
                                               style={'marginTop': 15, 'width': '100%'})
                                ],
                                body=True,
                            )
                        , md=4),
                        # Plots and results
                        dbc.Col(html.Div(
                            dbc.Tabs(),
                            id="simulation-result"
                        ),md=8)
                    ],
                    align="center",
                )],
                body=True,
                style={"height": "100%", "marginTop": 15, "marginBottom": 15, "backgroundColor": "#295e8f"}
            )
        ],
        fluid=True
    )
