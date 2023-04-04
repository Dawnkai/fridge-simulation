import math
from pid_regulator import PID_Regulator
from fuzzy_regulator import Fuzzy_Regulator
from tempomat import Tempomat

class Simulation:
    def __init__(self, regulator = Fuzzy_Regulator(), process = Tempomat()) -> None:
        self.sampling = 0.1 #s [Tp]
        self.simulation_time = 100 #s [Tsim]
        self.regulator = regulator
        self.process = process
        self.time_measurements = [0.0]
    
    def start(self) -> None:
        # Main loop
        for idx in range(1, math.floor(self.simulation_time / self.sampling) + 1):
            self.time_measurements.append(idx*self.sampling)
            signal = self.regulator.get_signal(self.process.get_latest_measurement(), self.time_measurements[-1], self.time_measurements[-2])
            self.process.add_signal(signal, self.sampling)
        
    def reset(self) -> None:
        self.time_measurements = [0.0]
        self.regulator.reset()
        self.process.reset()

    def get_regulator_type(self) -> str:
        return str(self.regulator)

    def set_regulator(self, regulator) -> None:
        self.regulator = regulator
    
    def set_process(self, process) -> None:
        self.process = process
    
    def get_display_results(self) -> list:
        return [self.time_measurements] + self.process.get_results() + [self.regulator.get_errors()]
