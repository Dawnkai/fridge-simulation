"""Car tempomat process."""

from constants import MASS, MIN_RESPONSE, MAX_RESPONSE, MIN_SIGNAL, MAX_SIGNAL, RESISTANCE

class Tempomat:
    """Car tempomat process object."""
    def __init__(self) -> None:
        self.mass = MASS
        self.resistance = RESISTANCE

        # Limits
        self.min_pull_force = MIN_RESPONSE
        self.max_pull_force = MAX_RESPONSE
        self.min_signal = MIN_SIGNAL
        self.max_signal = MAX_SIGNAL
        self.reset()

    def __str__(self) -> str:
        return "Tempomat"

    def get_signal_response(self, signal : float) -> float:
        '''
        Get response to provided signal.
        :param signal: signal to respond to.
        '''
        # a = (Fmax - Fmin) / (umax - umin)
        coefficient = (self.max_pull_force - self.min_pull_force) / (self.max_signal - self.min_signal)
        return (coefficient * (signal - self.min_signal)) + self.min_pull_force

    def add_signal(self, signal : float, sampling : float) -> None:
        '''
        Calculate system response and environment variables.
        :param signal: signal from the controller.
        :param sampling: sampling rate of the simulation.
        '''
        self.signals.append(min(self.max_signal, max(self.min_signal, signal)))
        self.pull_force = self.get_signal_response(self.signals[-1])
        # v(n+1) = Tp * (Fc(n) - beta*v(n)^2)*m + v(n)
        self.velocity_measurements.append(sampling * (self.pull_force -
                                                      (self.resistance*self.velocity_measurements[-1]**2)) /
                                                      self.mass + self.velocity_measurements[-1]
                                        )
        # x = v[-2] * p + x[-1]
        self.position_measurements.append(sampling * self.velocity_measurements[-2] + self.position_measurements[-1])

    def get_latest_measurement(self) -> float:
        """Get latest velocity measurement."""
        return self.velocity_measurements[-1] 

    def get_results(self) -> list:
        """Get process display results."""
        return [self.velocity_measurements, self.position_measurements, self.signals]

    def reset(self, init_value : float = 0.0) -> None:
        """Reset process."""
        # Measurements
        self.velocity_measurements = [init_value]
        self.position_measurements = [0.0]
        self.pull_force = 0 #N [Fc]
        self.signals = [0.0] #V [U]
