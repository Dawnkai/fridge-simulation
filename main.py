import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, State

from utils import get_controls, get_result_graphs, get_app_layout
from database import get_connection, execute_query, insert_data, get_latest_measurements, check_simulation_exists
from simulation import Simulation
from pi_regulator import PI_Regulator
from pid_regulator import PID_Regulator

class Display:
    def __init__(self, db_conn = None, n_measurements = 8):
        self.simulation = Simulation()
        self.results = []
        self.db_conn = db_conn
        self.n_measurements = n_measurements
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
        if len(self.results) < (self.n_measurements):
            self.results = get_latest_measurements(self.db_conn, self.n_measurements)

        if regulator_type != self.simulation.get_regulator_type():
            if regulator_type == "PI":
                self.simulation.set_regulator(PI_Regulator())
            else:
                self.simulation.set_regulator(PID_Regulator())
        else:
            if regulator_type == "PI":
                self.simulation.reset_regulator(target_value, pi_p, pi_i)
            else:
                self.simulation.reset_regulator(target_value, pid_p, pid_i, pid_d)

            self.simulation.reset()
            self.simulation.start()

            result = self.simulation.get_display_results()

            if len(self.results) > (self.n_measurements - 1):
                self.results.pop(0)
            
            if not check_simulation_exists(self.db_conn, pi_p, pi_i, pid_p, pid_i, pid_d, target_value, regulator_type):
                insert_data(self.db_conn, pi_p, pi_i, pid_p, pid_i, pid_d, target_value, regulator_type, result)
                self.results.append(result)

        self.results = get_latest_measurements(self.db_conn, self.n_measurements)

        return get_result_graphs(self.results), get_controls(regulator_type, pi_p, pi_i, pid_p, pid_i, pid_d)

if __name__ == "__main__":
    conn = get_connection("database.db")
    execute_query(conn, "CREATE TABLE IF NOT EXISTS Simulations(simulation_id INTEGER PRIMARY KEY AUTOINCREMENT, date INTEGER NOT NULL, time INTEGER NOT NULL, param_1 REAL NULL, param_2 REAL NULL, param_3 REAL NULL, target_value REAL NOT NULL, regulator_type TEXT NOT NULL)", True)
    execute_query(conn, "CREATE TABLE IF NOT EXISTS Measurements(measurement_id INTEGER PRIMARY KEY AUTOINCREMENT, simulation_id INTEGER NOT NULL REFERENCES Simulations(simulation_id), time REAL NOT NULL, signal REAL NOT NULL, signal_response REAL NOT NULL, error REAL NOT NULL)", True)
    disp = Display(conn)
    disp.start()
