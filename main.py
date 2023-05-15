"""Main app file, starts Dash display and database connection."""
import dash_bootstrap_components as dbc

from dash import Dash, Input, Output, State

from constants import NUM_SIMULATIONS
from database import Database
from simulation import Simulation
from utils import get_controls, get_result_graphs, get_app_layout, form_valid

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
            State("param-1", "value"),
            State("param-2", "value"),
            State("param-3", "value"),
            Input("simulation-button", "n_clicks")
        ])(self.make_graph)

    def make_graph(self, regulator_type, target_value, param_1, param_2, param_3, _):
        """Update graphs based on user input and database state."""
        if form_valid(regulator_type, param_1, param_2, param_3):
            # Do not run the simulation on regulator change (let the user set parameters first)
            if regulator_type != self.simulation.get_regulator_type():
                self.simulation.set_regulator(regulator_type)
            elif not self.running:
                self.running = True
                self.simulation.reset_regulator(target_value, param_1, param_2, param_3)
                self.simulation.reset()
                self.simulation.start()
                result = self.simulation.get_display_results()
                self.db.insert_or_update_data(param_1, param_2, param_3, target_value, regulator_type, result)
        
        self.running = False
        results = self.db.get_latest_simulations(NUM_SIMULATIONS, target_value)
        return get_result_graphs(results), get_controls(regulator_type, param_1, param_2, param_3)
    
    def run_server(self):
        self.app.run_server()

if __name__ == "__main__":
    app = Display()
    app.run_server()
