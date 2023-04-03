import dash_bootstrap_components as dbc
from dash import dcc, html

def get_controls(regulator_type : str, pi_p : float = 1.0, pi_i : float = 1.0, pid_p : float = 1.0, pid_i : float = 1.0, pid_d : float = 1.0) -> dbc.Card:
    return [
        html.Div(
            [
                dbc.Label("Proportional gain"),
                dcc.Input(
                    id="pi-proportional",
                    min=0,
                    step=0.001,
                    value=pi_p,
                    type="number"
                ),
            ],
            style={'display': 'none' if regulator_type == 'PID' else 'block'}
        ),
        html.Div(
            [
                dbc.Label("Integral gain"),
                dcc.Input(
                    id="pi-integral",
                    min=0,
                    step=0.001,
                    value=pi_i,
                    type="number"
                )
            ],
            style={'display': 'none' if regulator_type == 'PID' else 'block'}
        ),
        html.Div(
            [
                dbc.Label("Proportional coefficient"),
                dcc.Input(
                    id="pid-proportional",
                    min=0,
                    step=0.001,
                    value=pid_p,
                    type="number"
                )
            ],
            style={'display': 'none' if regulator_type == 'PI' else 'block'}
        ),
        html.Div(
            [
                dbc.Label("Integral coefficient"),
                dcc.Input(
                    id="pid-integral",
                    min=0,
                    step=0.001,
                    value=pid_i,
                    type="number"
                )
            ],
            style={'display': 'none' if regulator_type == 'PI' else 'block'}
        ),
        html.Div(
            [
                dbc.Label("Derivative coefficient"),
                dcc.Input(
                    id="pid-derivative",
                    min=0,
                    step=0.001,
                    value=pid_d,
                    type="number"
                )
            ],
            style={'display': 'none' if regulator_type == 'PI' else 'block'}
        )
    ]
