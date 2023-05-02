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

def create_tables(conn):
    '''
    Create required sqlite3 tables.
    :param conn: database connection object.
    '''
    try:
        cur = conn.cursor()
        with open("database_script.sql") as script:
            cur.executescript(script.read())
        conn.commit()
        cur.close()
    except sqlite3.Error as error:
        print(f"Erron in create_tables: {error}")

def get_new_simulation_id(conn) -> int:
    '''
    Get new simulation id higher than all available in the database.
    :param conn: database connection object.
    '''
    try:
        cur = conn.cursor()
        cur.execute("SELECT MAX(simulation_id) + 1 FROM Simulations")
        rows = cur.fetchall()
        if len(rows) > 0 and rows[0][0] is not None:
            return rows[0][0] + 1
        return 0
    except sqlite3.Error as error:
        print(f"Sqlite error in get_new_simulation_id: {error}")
    finally:
        cur.close()
    return -1

def insert_simulation(conn, sim_id : int, param_1, param_2, param_3,
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
    now = datetime.now()
    try:
        cur = conn.cursor()
        cur.execute(
            f"INSERT INTO Simulations"
            f"(simulation_id, simulation_date, simulation_time, param_1, "
            f"param_2,param_3, target_value, regulator_type)"
            f"VALUES ("
            f"{sim_id}, {now.strftime('%Y%m%d')}, {now.strftime('%H%M%S')},"
            f"{param_1 if param_1 is not None else 'NULL'},"
            f"{param_2 if param_2 is not None else 'NULL'},"
            f"{param_3 if param_3 is not None else 'NULL'},"
            f"{target_value}, '{regulator_type}'"
            f")"
        )
        conn.commit()
    except sqlite3.Error as error:
        print(f"Error in insert_simulation: {error}")
        return False
    finally:
        cur.close()
    return True

def insert_measurements(conn, sim_id : int, measurements : list) -> bool:
    '''
    Insert simulation measurements into database.
    :param conn: database connection object.
    :param measurements: list of simulation display results.
    '''
    insert_query = ("INSERT INTO Measurements "
                    "(simulation_id, measurement_time, measurement_value, measurement_signal,"
                    "measurement_response, error) VALUES ")
    for idx, time_measurement in enumerate(measurements[0]):
        insert_query += f"""({sim_id}, {time_measurement}, {measurements[1][idx]}, {measurements[2][idx]},
                         {measurements[3][idx]}, {measurements[4][idx]}), """
    insert_query = insert_query[:-2]
    try:
        cur = conn.cursor()
        cur.execute(insert_query)
        conn.commit()
    except sqlite3.Error as error:
        print(f"Error in insert_measurements: {error}")
        return False
    finally:
        cur.close()
    return True

def simulation_exists(conn, pi_p : float, pi_i : float, pid_p : float, pid_i : float,
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

    try:
        cur = conn.cursor()
        cur.execute(test_query)
        if cur.fetchall() != []:
            return True
    except sqlite3.Error as error:
        print(f"Error in simulation_exists: {error}")
        return False
    finally:
        cur.close()

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
        success = insert_simulation(conn, new_sim_id, pi_p, pi_i, None, target_value, "PI")
    elif regulator_type == "PID":
        success = insert_simulation(conn, new_sim_id, pid_p, pid_i, pid_d, target_value, "PID")
    else:
        success = insert_simulation(conn, new_sim_id, None, None, None, target_value, "Fuzzy")
    return success and insert_measurements(conn, new_sim_id, measurements)

def get_latest_simulations(conn, n_simulations : int):
    '''
    Get n latest simulation results from the database.
    :param conn: database connection object.
    :param n_simulations: number of simulations to fetch.
    '''
    try:
        cur = conn.cursor()
        cur.execute(
            f"SELECT simulation_id FROM Simulations "
            f"ORDER BY simulation_date, simulation_time DESC LIMIT {n_simulations}"
        )
        sim_ids = [ val[0] for val in cur.fetchall() ]

        if sim_ids == [None]:
            return None

        results = []
        for sim_id in sim_ids:
            cur.execute(
                f"SELECT measurement_time, measurement_value, measurement_signal, measurement_response,"
                f"error FROM Measurements "
                f"WHERE simulation_id = {sim_id} ORDER BY measurement_time"
            )
            parsed_measurements = [[], [], [], [], []]
            for measure in cur.fetchall():
                parsed_measurements[0].append(measure[0])
                parsed_measurements[1].append(measure[1])
                parsed_measurements[2].append(measure[2])
                parsed_measurements[3].append(measure[3])
                parsed_measurements[4].append(measure[4])
            results.append(parsed_measurements)
        return results
    except sqlite3.Error as error:
        print(f"Error in get_latest_simulations: {error}")
        return []
    finally:
        cur.close()
