"""Simulation component."""

import math

from constants import SAMPLING, SIMULATION_TIME
from controllers.pi_controller import PI_Controller
from controllers.pid_controller import PID_Controller
from controllers.fuzzy_controller import Fuzzy_Controller
from processes.tempomat import Tempomat
from processes.refrigerator import Refrigerator

class Simulation:
    '''
    Simulation object.
    :param controller: controller object to use in the simulation.
    :param process: process object that simulation simulates.
    '''
    def __init__(self, controller = PI_Controller(), process = Refrigerator()) -> None:
        self.sampling = SAMPLING
        self.simulation_time = SIMULATION_TIME
        self.controller = controller
        self.process = process
        self.time_measurements = [0.0]

    def start(self) -> None:
        """Start the simulation."""
        # Main loop
        for idx in range(1, math.floor(self.simulation_time / self.sampling) + 1):
            self.time_measurements.append(idx*self.sampling)
            signal = self.controller.get_signal(self.process.get_latest_measurement(),
                                               self.time_measurements[-1],
                                               self.time_measurements[-2])
            self.process.add_signal(signal, self.sampling)

    def reset(self, init_value) -> None:
        """Reset simulation and its parameters."""
        self.time_measurements = [0.0]
        self.process.reset(init_value)

    def reset_controller(self, target_value, init_value, param_1, param_2, param_3):
        """Reset selected controller object."""
        if str(self.controller) == "PI":
            self.controller.reset(target_value, init_value, param_1, param_2)
        elif str(self.controller) == "PID":
            self.controller.reset(target_value, init_value, param_1, param_2, param_3)
        else:
            self.controller.reset(target_value, init_value)

    def get_controller_type(self) -> str:
        """Get name of selected controller."""
        return str(self.controller)

    def set_controller(self, controller_type) -> None:
        """Change selected controller to provided controller type."""
        if controller_type == "PI":
            self.controller = PI_Controller()
        elif controller_type == "PID":
            self.controller = PID_Controller()
        else:
            self.controller = Fuzzy_Controller()

    def set_process(self, process) -> None:
        """Change simulated process to provided process."""
        self.process = process

    def get_display_results(self) -> list:
        """Return simulation results to display."""
        return [self.time_measurements] + self.process.get_results() + [self.controller.get_errors()]
