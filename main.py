import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, State
from utils import get_controls, get_result_graphs, get_app_layout

from simulation import Simulation
from pi_regulator import PI_Regulator
from pid_regulator import PID_Regulator

class Display:
    def __init__(self):
        self.simulation = Simulation()
        self.results = []
        self.app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
        self.app.css.config.serve_locally = True
        self.app.scripts.config.serve_locally = True
        self.app.layout = get_app_layout()
        self.app.callback(
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
        ])(self.make_graph)

    def start(self):
        self.app.run_server()

    def make_graph(self, regulator_type, target_value, pi_p, pi_i, pid_p, pid_i, pid_d, _):
        if regulator_type != self.simulation.get_regulator_type():
            if regulator_type == "PI":
                self.simulation.set_regulator(PI_Regulator())
            else:
                self.simulation.set_regulator(PID_Regulator())

        if regulator_type == "PI":
            self.simulation.reset_regulator(target_value, pi_p, pi_i)
        else:
            self.simulation.reset_regulator(target_value, pid_p, pid_i, pid_d)

        self.simulation.reset()
        self.simulation.start()
        if len(self.results) > 8:
            self.results.pop(0)
        self.results.append(self.simulation.get_display_results())
        return get_result_graphs(self.results), get_controls(regulator_type, pi_p, pi_i, pid_p, pid_i, pid_d)

if __name__ == "__main__":
    disp = Display()
    disp.start()
