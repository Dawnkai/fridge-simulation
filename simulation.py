"""Simulation component."""

import math

from constants import SAMPLING, SIMULATION_TIME
from regulators.pi_regulator import PI_Regulator
from regulators.pid_regulator import PID_Regulator
from regulators.fuzzy_regulator import Fuzzy_Regulator
from processes.tempomat import Tempomat
from processes.refrigerator import Refrigerator

class Simulation:
    '''
    Simulation object.
    :param regulator: regulator object to use in the simulation.
    :param process: process object that simulation simulates.
    '''
    def __init__(self, regulator = Fuzzy_Regulator(), process = Refrigerator()) -> None:
        self.sampling = SAMPLING
        self.simulation_time = SIMULATION_TIME
        self.regulator = regulator
        self.process = process
        self.time_measurements = [0.0]

    def start(self) -> None:
        """Start the simulation."""
        # Main loop
        for idx in range(1, math.floor(self.simulation_time / self.sampling) + 1):
            self.time_measurements.append(idx*self.sampling)
            signal = self.regulator.get_signal(self.process.get_latest_measurement(),
                                               self.time_measurements[-1],
                                               self.time_measurements[-2])
            self.process.add_signal(signal, self.sampling)

    def reset(self) -> None:
        """Reset simulation and its parameters."""
        self.time_measurements = [0.0]
        self.process.reset()

    def reset_regulator(self, target_value, param_1, param_2, param_3):
        """Reset selected regulator object."""
        if str(self.regulator) == "PI":
            self.regulator.reset(target_value, param_1, param_2)
        elif str(self.regulator) == "PID":
            self.regulator.reset(target_value, param_1, param_2, param_3)
        else:
            self.regulator.reset(target_value)

    def get_regulator_type(self) -> str:
        """Get name of selected regulator."""
        return str(self.regulator)

    def set_regulator(self, regulator_type) -> None:
        """Change selected regulator to provided regulator type."""
        if regulator_type == "PI":
            self.regulator = PI_Regulator()
        elif regulator_type == "PID":
            self.regulator = PID_Regulator()
        else:
            self.regulator = Fuzzy_Regulator()

    def set_process(self, process) -> None:
        """Change simulated process to provided process."""
        self.process = process

    def get_display_results(self) -> list:
        """Return simulation results to display."""
        # [time, signal, (unused), signal_response, errors]
        return [self.time_measurements] + self.process.get_results() + [self.regulator.get_errors()]
