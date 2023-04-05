import dash_bootstrap_components as dbc
from dash import dcc, html
import plotly.graph_objs as go
import plotly.express as px

def get_controls(regulator_type : str, pi_p : float = 1.0, pi_i : float = 1.0, pid_p : float = 1.0, pid_i : float = 1.0, pid_d : float = 1.0) -> dbc.Card:
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
            style={'display': 'none' if regulator_type == 'PID' else 'block'}
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
            style={'display': 'none' if regulator_type == 'PID' else 'block'}
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
            style={'display': 'none' if regulator_type == 'PI' else 'block'}
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
            style={'display': 'none' if regulator_type == 'PI' else 'block'}
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
            style={'display': 'none' if regulator_type == 'PI' else 'block'}
        )
    ]


def get_result_graphs(time_result : list, response_result : list, signal_result : list, error_result : list) -> dcc.Tabs:
    signal_figure = go.Figure(data=px.line(x=time_result, y=signal_result))
    signal_figure.update_layout(xaxis_title="Time [s]", yaxis_title="Response [km/h]")
    response_figure = go.Figure(data=px.line(x=time_result, y=response_result))
    response_figure.update_layout(xaxis_title="Time [s]", yaxis_title="Signal [V]")
    error_figure = go.Figure(data=px.line(x=time_result, y=error_result))
    error_figure.update_layout(xaxis_title="Time [s]", yaxis_title="Error [V]")
    return dcc.Tabs([
        dcc.Tab(label="Signal response", children=[dcc.Graph(figure=response_figure)]),
        dcc.Tab(label="Signal", children=[dcc.Graph(figure=signal_figure)]),
        dcc.Tab(label="Error", children=[dcc.Graph(figure=error_figure)])
    ])
