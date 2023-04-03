import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import plotly.express as px
from dash import Dash, Input, Output, dcc, html
from controls import get_controls

from simulation import Simulation
from pi_regulator import PI_Regulator
from pid_regulator import PID_Regulator

simulation = Simulation()

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

app.layout = dbc.Container(
    [
        html.H1("Levitating Ball Simulation"),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
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
                                    )
                                ]
                            ),
                            html.Div(
                                [
                                    dbc.Label("Target value"),
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
                            )
                        ],
                        body=True,
                    )
                , md=4),
                dbc.Col(dcc.Graph(id="simulation-result"), md=8),
            ],
            align="center",
        ),
    ],
    fluid=True
)

@app.callback(
    [
        Output("simulation-result", "figure"),
        Output("controls", "children")
    ],
    [
        Input("regulator-type", "value"),
        Input("target-value", "value"),
        Input("pi-proportional", "value"),
        Input("pi-integral", "value"),
        Input("pid-proportional", "value"),
        Input("pid-integral", "value"),
        Input("pid-derivative", "value")
    ],
)
def make_graph(regulator_type, target_value, pi_p, pi_i, pid_p, pid_i, pid_d):
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
    time, velocity, _, _, _ = simulation.get_display_results()
    return go.Figure(data=px.line(x=time, y=velocity)), get_controls(regulator_type, pi_p, pi_i, pid_p, pid_i, pid_d)

if __name__ == "__main__":
    app.run_server()
