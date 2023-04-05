import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, State, dcc, html
from controls import get_controls, get_result_graphs

from simulation import Simulation
from pi_regulator import PI_Regulator
from pid_regulator import PID_Regulator

simulation = Simulation()

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

app.layout = dbc.Container(
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
                                                {"label": "PID", "value": "PID"}
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
                                dbc.Button("Go", color="primary", id="start-simulation", n_clicks=0, style={'marginTop': 15, 'width': '100%'})
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

@app.callback(
    [
        Output("simulation-result", "children"),
        Output("controls", "children")
    ],
    [
        Input("regulator-type", "value"),
        State("target-value", "value"),
        State("pi-proportional", "value"),
        State("pi-integral", "value"),
        State("pid-proportional", "value"),
        State("pid-integral", "value"),
        State("pid-derivative", "value"),
        Input("start-simulation", "n_clicks")
    ],
)
def make_graph(regulator_type, target_value, pi_p, pi_i, pid_p, pid_i, pid_d, n_clicks):
    if regulator_type != simulation.get_regulator_type():
        if regulator_type == "PI":
            simulation.set_regulator(PI_Regulator())
        else:
            simulation.set_regulator(PID_Regulator())

    if regulator_type == "PI":
        simulation.reset_regulator(target_value, pi_p, pi_i)
    else:
        simulation.reset_regulator(target_value, pid_p, pid_i, pid_d)

    simulation.reset()
    simulation.start()
    time, velocity, _, signal, error = simulation.get_display_results()
    return get_result_graphs(time, velocity, signal, error), get_controls(regulator_type, pi_p, pi_i, pid_p, pid_i, pid_d)

if __name__ == "__main__":
    app.run_server()
