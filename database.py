"""Database connection driver."""

import sqlite3

from datetime import datetime

def get_connection(dbpath : str):
    '''
    Get SQLite connection object.
    :param dbpath: file location of the database.
    '''
    conn = None
    try:
        conn = sqlite3.connect(dbpath, check_same_thread=False)
    except sqlite3.Error as error:
        print(f"Sqlite error in get_connection: {error}")
    return conn

def execute_query(conn, query : str, commit : bool) -> bool:
    '''
    Run SQL query.
    :param conn: database connection object.
    :param query: SQL query to execute.
    :param commit: whether to run commit after execution or not.
    '''
    try:
        cur = conn.cursor()
        cur.execute(query)
        cur.close()
        if commit:
            conn.commit()
    except sqlite3.Error as error:
        print(f"Sqlite error when executing query ({query}): {error}")
        return False
    return True

def select_query(conn, query : str) -> list:
    '''
    Run SELECT query and return result as list of tuples.
    :param conn: database connection object.
    :param query: SQL SELECT query to execute.
    '''
    rows = []
    try:
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        cur.close()
    except sqlite3.Error as error:
        print(f"Sqlite error when executing query ({query}): {error}")
    return rows

def get_new_simulation_id(conn) -> int:
    '''
    Get new simulation id higher than all available in the database.
    :param conn: database connection object.
    '''
    try:
        rows = select_query(conn, "SELECT MAX(simulation_id) FROM Simulations")
        if len(rows) > 0 and rows[0][0] is not None:
            return rows[0][0] + 1
        return 0
    except sqlite3.Error as error:
        print(f"Sqlite error in get_new_simulation_id: {error}")
    return -1

def insert_simulation(conn, sim_id : int, param_1 : float, param_2 : float, param_3 : float,
                      target_value : float, regulator_type : str) -> bool:
    '''
    Insert simulation data into database.
    Because SQLite does not support variable amount of columns, number of columns is max of required parameters
    by any regulator (so 3 because PID requires P, I and D).
    :param conn: database connection object.
    :param param_1: first parameter
    :param param_2: second parameter
    :param param_3: third parameter
    :target_value: target value of the simulation.
    :regulator_type: regulator used in simulation.
    '''
    insert_query = (
        f"INSERT INTO Simulations (simulation_id, date, time, param_1, param_2, "
        f"param_3, target_value, regulator_type) VALUES ({sim_id}, "
    )
    now = datetime.now()
    insert_query += f"{now.strftime('%Y%m%d')}, {now.strftime('%H%M%S')},"
    insert_query += f"{param_1}, {param_2}, {param_3}, {target_value}, '{regulator_type}')"
    return execute_query(conn, insert_query, True)

def insert_measurements(conn, sim_id : int, measurements : list) -> bool:
    '''
    Insert simulation measurements into database.
    :param conn: database connection object.
    :param measurements: list of simulation display results.
    '''
    insert_query = "INSERT INTO Measurements (simulation_id, time, signal, signal_response, error) VALUES "
    for idx, time_measurement in enumerate(measurements[0]):
        insert_query += f"""({sim_id}, {time_measurement}, {measurements[2][idx]},
                         {measurements[3][idx]}, {measurements[4][idx]}), """
    insert_query = insert_query[:-2]
    return execute_query(conn, insert_query, True)

def check_simulation_exists(conn, pi_p : float, pi_i : float, pid_p : float, pid_i : float,
                            pid_d : float, target_value : float, regulator_type : str) -> bool:
    '''
    Check if simulation using provided parameters already exists in the database.
    :param conn: database connection object.
    :param pi_p: proportional PI regulator parameter.
    :param pi_i: integral PI regulator parameter.
    :param pid_p: proportional PID regulator parameter.
    :param pid_i: integral PID regulator parameter.
    :param pid_d: derivative PID regulator parameter.
    :param target_value: target value of the simulation.
    :param regulator_type: regulator used in simulation.
    '''
    test_query = ""
    if regulator_type == "PI":
        test_query += (
            f"SELECT * FROM Simulations WHERE param_1 = {float(pi_p)} AND param_2 "
            f" = {float(pi_i)} AND param_3 IS NULL AND "
        )
    elif regulator_type == "PID":
        test_query += (
            f"SELECT * FROM Simulations WHERE param_1 = {float(pid_p)} AND param_2 "
            f" = {float(pid_i)} AND param_3 = {float(pid_d)} AND "
        )
    else:
        test_query += "SELECT * FROM Simulations WHERE "
    test_query += f"target_value = {float(target_value)} AND regulator_type = '{regulator_type}'"

    simulation_check = select_query(conn, test_query)
    if simulation_check != []:
        return True
    return False

def insert_data(conn, pi_p : float, pi_i : float, pid_p : float, pid_i : float, pid_d : float,
                target_value : float, regulator_type : str, measurements : list) -> bool:
    '''
    Insert simulation and display results data into database.
    :param conn: database connection object.
    :param pi_p: proportional PI regulator parameter.
    :param pi_i: integral PI regulator parameter.
    :param pid_p: proportional PID regulator parameter.
    :param pid_i: integral PID regulator parameter.
    :param pid_d: derivative PID regulator parameter.
    :param target_value: target value of the simulation.
    :param regulator_type: regulator used in simulation.
    :param measurements: display results of simulation.
    '''
    new_sim_id = get_new_simulation_id(conn)
    success = True
    if regulator_type == "PI":
        success = insert_simulation(conn, new_sim_id, pi_p, pi_i, "NULL", target_value, "PI")
    elif regulator_type == "PID":
        success = insert_simulation(conn, new_sim_id, pid_p, pid_i, pid_d, target_value, "PID")
    else:
        success = insert_simulation(conn, new_sim_id, "NULL", "NULL", "NULL", target_value, "Fuzzy")
    return success and insert_measurements(conn, new_sim_id, measurements)

def get_latest_simulations(conn, n_simulations : int):
    '''
    Get n latest simulation results from the database.
    :param conn: database connection object.
    :param n_simulations: number of simulations to fetch.
    '''
    simulations = select_query(conn,
                               f"SELECT simulation_id FROM Simulations ORDER BY date, time DESC LIMIT {n_simulations}")
    sim_ids = [ val[0] for val in simulations ]
    if sim_ids == [None]:
        return None

    results = []
    for sim_id in sim_ids:
        measurements = select_query(conn,
                                    (
                                        f"SELECT time, signal, signal_response, error FROM Measurements "
                                        f"WHERE simulation_id = {sim_id} ORDER BY time"
                                    ))
        parsed_measurements = [[], [], [], [], []]
        for measure in measurements:
            parsed_measurements[0].append(measure[0])
            parsed_measurements[2].append(measure[1])
            parsed_measurements[3].append(measure[2])
            parsed_measurements[4].append(measure[3])
        results.append(parsed_measurements)
    return results
