"""Project utilities (UI controls, app layout and result graph), separated for readability."""

import dash_bootstrap_components as dbc
import plotly.graph_objs as go

from dash import dcc, html

def get_controls(regulator_type : str, param_1 : float = 1.0, param_2 : float = 1.0, param_3 : float = 1.0) -> dbc.Card:
    """Regulator controls visible in the GUI."""
    return [
        html.Div(
            [
                dbc.Label("Proportional gain: " if regulator_type == 'PI' else 'Proportional coefficient'),
                dcc.Input(
                    id="param-1",
                    min=0,
                    step=0.01,
                    value=param_1,
                    type="number",
                    style={"marginLeft": 10}
                )
            ],
            style={'display': 'none' if regulator_type == 'Fuzzy' else 'block'}
        ),
        html.Div(
            [
                dbc.Label("Integral gain: " if regulator_type == 'PI' else 'Integral coefficient'),
                dcc.Input(
                    id="param-2",
                    min=0,
                    step=0.01,
                    value=param_2,
                    type="number",
                    style={"marginLeft": 10}
                )
            ],
            style={'display': 'none' if regulator_type == 'Fuzzy' else 'block'}
        ),
        html.Div(
            [
                dbc.Label("Derivative coefficient: "),
                dcc.Input(
                    id="param-3",
                    min=0,
                    step=0.01,
                    value=param_3,
                    type="number",
                    style={"marginLeft": 10}
                )
            ],
            style={'display': 'none' if regulator_type != 'PID' else 'block'}
        )
    ]

def get_line_color(regulator_type : str) -> dict:
    '''
    Get color of the line for results based on regulator type.
    :param regulator_type: type of the regulator (PI, PID or Fuzzy)
    '''
    if regulator_type == "Fuzzy":
        return dict(color="#ff0000")
    if regulator_type == 'PID':
        return dict(color="#00ff00")
    if regulator_type == 'PI':
        return dict(color="#0000ff")
    return dict(color="#000000")

def get_line_name(idx : int, result : list) -> str:
    '''
    Get name of the line on plot legend based on index and simulation params.
    :param idx: index of the simulation
    :param result: list containing results of simulation
    '''
    if result[5] == "Fuzzy":
        return f"Fuzzy ({idx})"
    if result[5] == "PID":
        return f"Kp: {result[6][0]}, Ki: {result[6][1]}, Kd: {result[6][2]}"
    if result[5] == "PI":
        return f"Tp: {result[6][0]}, Ti: {result[6][1]}"
    return f"Simulation {idx}"

def get_result_graphs(results : list) -> dcc.Tabs:
    """Graphs with simulation results."""
    value_figure = go.Figure()
    signal_figure = go.Figure()
    response_figure = go.Figure()
    error_figure = go.Figure()

    for idx, result in enumerate(results):
        line_color = get_line_color(result[5]) if idx > 0 else dict(color="#fa07f2")
        value_figure.add_trace(go.Scatter(x=result[0], y=result[1], name=get_line_name(idx, result),
                                          line=line_color))
        signal_figure.add_trace(go.Scatter(x=result[0], y=result[2], name=get_line_name(idx, result),
                                           line=line_color))
        response_figure.add_trace(go.Scatter(x=result[0], y=result[3], name=get_line_name(idx, result),
                                             line=line_color))
        error_figure.add_trace(go.Scatter(x=result[0], y=result[4], name=get_line_name(idx, result),
                                          line=line_color))

    value_figure.update_layout(xaxis_title="Time [s]", yaxis_title="Value [km]")
    signal_figure.update_layout(xaxis_title="Time [s]", yaxis_title="Response [km/h]")
    response_figure.update_layout(xaxis_title="Time [s]", yaxis_title="Signal [V]")
    error_figure.update_layout(xaxis_title="Time [s]", yaxis_title="Error [V]")

    return dcc.Tabs([
        dcc.Tab(label="Value", children=[dcc.Graph(figure=value_figure)]),
        dcc.Tab(label="Signal response", children=[dcc.Graph(figure=response_figure)]),
        dcc.Tab(label="Signal", children=[dcc.Graph(figure=signal_figure)]),
        dcc.Tab(label="Error", children=[dcc.Graph(figure=error_figure)])
    ])

def form_valid(regulator_type : str, param_1 : float, param_2 : float, param_3 : float) -> list:
    if regulator_type == 'Fuzzy':
        return [True, True, True]

    is_valid_1 = True if param_1 is not None else False
    is_valid_2 = True if param_2 is not None else False
    if regulator_type == 'PI':
        return [is_valid_1, is_valid_2, True]
    
    is_valid_3 = True if param_3 is not None else False
    return [is_valid_1, is_valid_2, is_valid_3]

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
                                    dbc.Button("Go", color="primary", id="simulation-button", n_clicks=0,
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
            ),
            html.Div(id='simulation-control', style={'display': 'none'})
        ],
        fluid=True
    )
