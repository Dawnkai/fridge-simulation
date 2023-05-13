"""Main app file, starts Dash display and database connection."""
import dash_bootstrap_components as dbc

from dash import Dash, Input, Output, State

from constants import NUM_SIMULATIONS
from database import Database
from regulators.pi_regulator import PI_Regulator
from regulators.pid_regulator import PID_Regulator
from regulators.fuzzy_regulator import Fuzzy_Regulator
from simulation import Simulation
from utils import get_controls, get_result_graphs, get_app_layout

class Display:
    def __init__(self):
        self.db = Database("database.db")
        self.simulation = Simulation()
        self.app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
        self.app.css.config.serve_locally = True
        self.app.scripts.config.serve_locally = True
        self.app.layout = get_app_layout()
        self.running = False
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
            Input("simulation-button", "n_clicks")
        ])(self.make_graph)

    def make_graph(self, regulator_type, target_value, pi_p, pi_i, pid_p, pid_i, pid_d, _):
        """Update graphs based on user input and database state."""

        # Do not run the simulation on regulator change (let the user set parameters first)
        if regulator_type != self.simulation.get_regulator_type():
            if regulator_type == "PI":
                self.simulation.set_regulator(PI_Regulator())
            elif regulator_type == "PID":
                self.simulation.set_regulator(PID_Regulator())
            else:
                self.simulation.set_regulator(Fuzzy_Regulator())
        elif not self.running:
            self.running = True
            if regulator_type == "PI":
                self.simulation.reset_regulator(target_value, pi_p, pi_i)
            elif regulator_type == "PID":
                self.simulation.reset_regulator(target_value, pid_p, pid_i, pid_d)
            else:
                self.simulation.reset_regulator(target_value)

            self.simulation.reset()
            self.simulation.start()
            result = self.simulation.get_display_results()

            # Do not add simulations with parameters that already exist in database
            if not self.db.simulation_exists(pi_p, pi_i, pid_p, pid_i, pid_d, target_value, regulator_type):
                self.db.insert_data(pi_p, pi_i, pid_p, pid_i, pid_d, target_value, regulator_type, result)
            self.running = False

        results = self.db.get_latest_simulations(NUM_SIMULATIONS, target_value)
        return get_result_graphs(results), get_controls(regulator_type, pi_p, pi_i, pid_p, pid_i, pid_d)
    
    def run_server(self):
        self.app.run_server()

if __name__ == "__main__":
    app = Display()
    app.run_server()
