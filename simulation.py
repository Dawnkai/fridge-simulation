"""Simulation component."""

import math

from pid_regulator import PID_Regulator
from tempomat import Tempomat

class Simulation:
    '''
    Simulation object.
    :param regulator: regulator object to use in the simulation.
    :param process: process object that simulation simulates.
    '''
    def __init__(self, regulator = PID_Regulator(), process = Tempomat()) -> None:
        self.sampling = 0.1 #s [Tp]
        self.simulation_time = 100 #s [Tsim]
        self.regulator = regulator
        self.process = process
        self.time_measurements = [0.0]

    def start(self) -> None:
        """Start the simulation."""
        # Main loop
        for idx in range(1, math.floor(self.simulation_time / self.sampling) + 1):
            self.time_measurements.append(idx*self.sampling)
            signal = self.regulator.get_signal(self.process.get_latest_measurement(), self.time_measurements[-1],
                                               self.time_measurements[-2])
            self.process.add_signal(signal, self.sampling)

    def reset(self) -> None:
        """Reset simulation and its parameters."""
        self.time_measurements = [0.0]
        self.process.reset()

    def reset_regulator(self, *args):
        """Reset selected regulator object."""
        self.regulator.reset(*args)

    def get_regulator_type(self) -> str:
        """Get name of selected regulator."""
        return str(self.regulator)

    def set_regulator(self, regulator) -> None:
        """Change selected regulator to provided object."""
        self.regulator = regulator

    def set_process(self, process) -> None:
        """Change simulated process to provided process."""
        self.process = process

    def get_display_results(self) -> list:
        """Return simulation results to display."""
        # [time, signal, (unused), signal_response, errors]
        return [self.time_measurements] + self.process.get_results() + [self.regulator.get_errors()]
