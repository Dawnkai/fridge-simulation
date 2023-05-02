CREATE TABLE IF NOT EXISTS Simulations(
    simulation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    simulation_date INTEGER NOT NULL,
    simulation_time INTEGER NOT NULL,
    param_1 REAL NULL,
    param_2 REAL NULL,
    param_3 REAL NULL,
    target_value REAL NOT NULL,
    regulator_type TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Measurements(
    measurement_id INTEGER PRIMARY KEY AUTOINCREMENT,
    simulation_id INTEGER NOT NULL REFERENCES Simulations(simulation_id),
    measurement_time REAL NOT NULL,
    measurement_value REAL NOT NULL,
    measurement_signal REAL NOT NULL,
    measurement_response REAL NOT NULL,
    error REAL NOT NULL
);
