"""PI regulator component."""

class PI_Regulator:
    '''
    PI regulator object.
    :param target_value: target regulated process value.
    :param proportional_gain: proportional gain of regulator.
    :param integral_gain: integral gain of regulator.
    '''
    def __init__(self, target_value : float = 40, proportional_gain : float = 0.010,
                 integral_gain : float = 0.1) -> None:
        self.reset(target_value, proportional_gain, integral_gain)

    def __str__(self) -> str:
        return "PI"

    def get_signal(self, last_value : float, last_time : int, time_before_that : int) -> float:
        '''
        Get response from the regulator.
        :param last_value: last value of controlled object.
        :param last_time: unused, last time of the measurement
        :param time_before_that: unused, time before the last_time
        '''
        self.error.append(self.target_value - last_value)
        return self.proportional_gain * (self.error[-1]
                                         + ((self.proportional_gain / self.integral_gain) * sum(self.error)))

    def get_errors(self) -> list:
        """Get all measurement errors detected by regulator."""
        return self.error

    def reset(self, target_value : float = 40, proportional_gain : float = 0.010, integral_gain : float = 0.1) -> None:
        """Change parameters of the regulator and reset measurements."""
        self.target_value = target_value
        self.error = [self.target_value]
        self.proportional_gain = proportional_gain # T_p (1)
        self.integral_gain = integral_gain # T_i (1)
