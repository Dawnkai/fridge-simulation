"""Main app file, starts Dash display and database connection."""

import dash_bootstrap_components as dbc

from dash import Dash, Input, Output, State

from constants import NUM_SIMULATIONS
from database import get_connection, insert_data, get_latest_simulations, simulation_exists, create_tables
from regulators.pi_regulator import PI_Regulator
from regulators.pid_regulator import PID_Regulator
from regulators.fuzzy_regulator import Fuzzy_Regulator
from simulation import Simulation
from utils import get_controls, get_result_graphs, get_app_layout

class Display:
    '''
    Dash object for displaying simulation results.
    :param db_conn: connection to database
    :param n_simulations: number of simulations to display
    '''
    def __init__(self, db_conn = None, n_simulations = NUM_SIMULATIONS):
        self.simulation = Simulation()
        self.results = []
        self.db_conn = db_conn
        self.n_simulations = n_simulations
        self.app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
        self.app.css.config.serve_locally = True
        self.app.scripts.config.serve_locally = True
        self.app.layout = get_app_layout()
        # Dash does not support dynamic Input field generation, so it's necessary
        # to add all fields and set them to invisible in css styles dynamically
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
        """Start Dash server."""
        self.app.run_server()

    def make_graph(self, regulator_type, target_value, pi_p, pi_i, pid_p, pid_i, pid_d, _):
        """Update graphs based on user input and database state."""
        # Get latest measurements from database if less results than required are stored in memory
        if len(self.results) < (self.n_simulations):
            self.results = get_latest_simulations(self.db_conn, self.n_simulations)

        # Do not run the simulation on regulator change (let the user set parameters first)
        if regulator_type != self.simulation.get_regulator_type():
            if regulator_type == "PI":
                self.simulation.set_regulator(PI_Regulator())
            elif regulator_type == "PID":
                self.simulation.set_regulator(PID_Regulator())
            else:
                self.simulation.set_regulator(Fuzzy_Regulator())
        else:
            if regulator_type == "PI":
                self.simulation.reset_regulator(target_value, pi_p, pi_i)
            elif regulator_type == "PID":
                self.simulation.reset_regulator(target_value, pid_p, pid_i, pid_d)
            else:
                self.simulation.reset_regulator(target_value)

            self.simulation.reset()
            self.simulation.start()
            result = self.simulation.get_display_results()

            # Remove oldest result if max number of simulations has been passed
            if len(self.results) > (self.n_simulations - 1):
                self.results.pop(0)

            # Do not add simulations with parameters that already exist in database
            if not simulation_exists(self.db_conn, pi_p, pi_i, pid_p, pid_i, pid_d, target_value, regulator_type):
                insert_data(self.db_conn, pi_p, pi_i, pid_p, pid_i, pid_d, target_value, regulator_type, result)
                self.results.append(result)

        self.results = get_latest_simulations(self.db_conn, self.n_simulations)

        return get_result_graphs(self.results), get_controls(regulator_type, pi_p, pi_i, pid_p, pid_i, pid_d)

if __name__ == "__main__":
    conn = get_connection("database.db")
    create_tables(conn)
    disp = Display(conn)
    disp.start()
