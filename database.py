"""Database connection driver."""

import sqlite3

from datetime import datetime

class Database:
    '''
    Database class for communication with sqlite3 database.
    :param dbpath: file location of the database
    '''
    def __init__(self, dbpath):
        self.dbpath = dbpath
        self.create_tables()

    def get_connection(self):
        '''
        Get SQLite connection object.
        '''
        conn = None
        try:
            conn = sqlite3.connect(self.dbpath, check_same_thread=False)
        except sqlite3.Error as error:
            print(f"Sqlite error in get_connection: {error}")
        return conn

    def create_tables(self):
        '''
        Create required sqlite3 tables.
        '''
        conn = self.get_connection()
        try:
            cur = conn.cursor()
            with open("database_script.sql") as script:
                cur.executescript(script.read())
            conn.commit()
            cur.close()
        except sqlite3.Error as error:
            print(f"Erron in create_tables: {error}")
        finally:
            conn.close()

    def insert_simulation(self, conn, param_1 : float, param_2 : float, param_3 : float,
                        target_value : float, controller_type : str) -> list:
        '''
        Insert simulation data into database.
        Because SQLite does not support variable amount of columns, number of columns is max of required parameters
        by any controller (so 3 because PID requires P, I and D).
        :param conn: database connection object
        :param param_1: first parameter (only for PI and PID)
        :param param_2: second parameter (only for PI and PID)
        :param param_3: third parameter (only for PID)
        :target_value: target value of the simulation
        :controller_type: controller used in simulation
        '''
        now = datetime.now()
        sim_id = -1
        try:
            cur = conn.cursor()
            cur.execute(
                f"INSERT INTO Simulations"
                f"(simulation_date, simulation_time, param_1, "
                f"param_2,param_3, target_value, controller_type)"
                f"VALUES ("
                f"{now.strftime('%Y%m%d')}, {now.strftime('%H%M%S')},"
                f"{param_1 if param_1 is not None and controller_type != 'Fuzzy' else 'NULL'},"
                f"{param_2 if param_2 is not None and controller_type != 'Fuzzy' else 'NULL'},"
                f"{param_3 if param_3 is not None and controller_type == 'PID' else 'NULL'},"
                f"{target_value}, '{controller_type}'"
                f")"
            )
            conn.commit()
            sim_id = cur.lastrowid
        except sqlite3.Error as error:
            print(f"Error in insert_simulation: {error}")
            return [False, -1]
        finally:
            cur.close()
        return [True, sim_id]

    def insert_measurements(self, conn, sim_id : int, measurements : list) -> bool:
        '''
        Insert simulation measurements into database.
        :param conn: database connection object
        :param sim_id: id of the simulation the measurements belong to
        :param measurements: list of simulation display results
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

    def simulation_exists(self, param_1 : float, param_2 : float, param_3 : float, target_value : float, controller_type : str) -> bool:
        '''
        Check if simulation using provided parameters already exists in the database.
        :param param_1: first parameter (only for PI and PID)
        :param param_2: second parameter (only for PI and PID)
        :param param_3: third parameter (only for PID)
        :param target_value: target value of the simulation
        :param controller_type: controller used in simulation
        '''
        conn = self.get_connection()
        test_query = ""
        if controller_type == "PI":
            test_query += (
                f"SELECT * FROM Simulations WHERE param_1 = {float(param_1)} AND param_2 "
                f" = {float(param_2)} AND param_3 IS NULL AND "
            )
        elif controller_type == "PID":
            test_query += (
                f"SELECT * FROM Simulations WHERE param_1 = {float(param_1)} AND param_2 "
                f" = {float(param_2)} AND param_3 = {float(param_3)} AND "
            )
        else:
            test_query += "SELECT * FROM Simulations WHERE "
        test_query += f"target_value = {float(target_value)} AND controller_type = '{controller_type}'"

        try:
            cur = conn.cursor()
            cur.execute(test_query)
            if cur.fetchall() != []:
                return True
            return False
        except sqlite3.Error as error:
            print(f"Error in simulation_exists: {error}")
            return False
        finally:
            cur.close()
            conn.close()

    def insert_data(self, param_1 : float, param_2 : float, param_3 : float,
                    target_value : float, controller_type : str, measurements : list) -> bool:
        '''
        Insert simulation and display results data into database.
        :param param_1: first parameter (only for PI and PID)
        :param param_2: second parameter (only for PI and PID)
        :param param_3: third parameter (only for PID)
        :param target_value: target value of the simulation
        :param controller_type: controller used in simulation
        :param measurements: display results of simulation
        '''
        conn = self.get_connection()
        success = True
        try:
            success, sim_id = self.insert_simulation(conn, param_1, param_2, param_3, target_value, controller_type)
            if sim_id == -1:
                return False
            return success and self.insert_measurements(conn, sim_id, measurements)
        finally:
            conn.close()

    def update_data(self, param_1 : float, param_2 : float, param_3 : float,
                    target_value : float, controller_type : str) -> bool:
        '''
        Update timestamp of simulation with provided parameters.
        :param param_1: first parameter (only for PI and PID)
        :param param_2: second parameter (only for PI and PID)
        :param param_3: third parameter (only for PID)
        :target_value: target value of the simulation
        :controller_type: controller name used in simulation
        '''
        conn = self.get_connection()
        now = datetime.now()
        try:
            cur = conn.cursor()
            cur.execute(
                f"SELECT simulation_id FROM Simulations WHERE controller_type = '{controller_type}' AND "
                f"param_1 {f'= {param_1}' if param_1 is not None and controller_type != 'Fuzzy' else 'IS NULL'} AND "
                f"param_2 {f'= {param_2}' if param_2 is not None and controller_type != 'Fuzzy' else 'IS NULL'} AND "
                f"param_3 {f'= {param_3}' if param_3 is not None and controller_type == 'PID' else 'IS NULL'} AND "
                f"target_value = {target_value}"
            )
            sim_id = cur.fetchall()[0][0]
            cur.execute(
                f"UPDATE Simulations SET simulation_date = {now.strftime('%Y%m%d')},"
                f"simulation_time = {now.strftime('%H%M%S')} WHERE simulation_id = {sim_id}"
            )
            conn.commit()
            return True
        except sqlite3.Error as error:
            print(f"Error in update_data : {error}")
            return False
        finally:
            conn.close()
        
    def insert_or_update_data(self, param_1 : float, param_2 : float, param_3 : float,
                              target_value : float, controller_type : str, measurements : list) -> bool:
        '''
        Insert new simulation data if no simulation exists for provided parameters or update
        timestamp of existing one.
        :param param_1: first parameter (only for PI and PID)
        :param param_2: second parameter (only for PI and PID)
        :param param_3: third parameter (only for PID)
        :param target_value: target value of the simulation
        :param controller_type: name of the controller used in simulation
        :param measurements: list of results to insert into DB
        '''
        if not self.simulation_exists(param_1, param_2, param_3, target_value, controller_type):
            self.insert_data(param_1, param_2, param_3, target_value, controller_type, measurements)
        else:
            self.update_data(param_1, param_2, param_3, target_value, controller_type)

    def get_latest_simulations(self, n_simulations : int, target_value : float):
        '''
        Get n latest simulation results from the database.
        :param n_simulations: number of simulations to fetch
        :param target_value: filter results to only show simulations for this target value
        '''
        conn = self.get_connection()
        try:
            cur = conn.cursor()
            cur.execute(
                f"SELECT simulation_id, controller_type, param_1, param_2, param_3 FROM Simulations WHERE target_value = {target_value} "
                f"ORDER BY simulation_date DESC, simulation_time DESC LIMIT {n_simulations}"
            )
            sims = [ [val[0], val[1], [val[2], val[3], val[4]]] for val in cur.fetchall() ]

            if sims == [None]:
                return None

            results = []
            for sim in sims:
                cur.execute(
                    f"SELECT measurement_time, measurement_value, measurement_signal, measurement_response,"
                    f"error FROM Measurements "
                    f"WHERE simulation_id = {sim[0]} ORDER BY measurement_time"
                )
                parsed_measurements = [[], [], [], [], []]
                for measure in cur.fetchall():
                    parsed_measurements[0].append(measure[0])
                    parsed_measurements[1].append(measure[1])
                    parsed_measurements[2].append(measure[2])
                    parsed_measurements[3].append(measure[3])
                    parsed_measurements[4].append(measure[4])
                parsed_measurements.append(sim[1])
                parsed_measurements.append(sim[2])
                results.append(parsed_measurements)
            return results
        except sqlite3.Error as error:
            print(f"Error in get_latest_simulations: {error}")
            return []
        finally:
            cur.close()
            conn.close()
