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
                dbc.Col(get_controls(), md=4),
                dbc.Col(dcc.Graph(id="simulation-result"), md=8),
            ],
            align="center",
        ),
    ],
    fluid=True
)

@app.callback(
    Output("simulation-result", "figure"),
    [
        Input("regulator-type", "value")
    ],
)
def make_graph(regulator_type):
    if regulator_type != simulation.get_regulator_type():
        if regulator_type == "PI":
            simulation.set_regulator(PI_Regulator())
        else:
            simulation.set_regulator(PID_Regulator())

    simulation.reset()
    simulation.start()
    time, velocity, _, _, _ = simulation.get_display_results()
    return go.Figure(data=px.line(x=time, y=velocity))

if __name__ == "__main__":
    app.run_server()
