"""PI controller component."""
from constants import SAMPLING

class PI_Controller:
    '''
    PI controller object.
    :param target_value: target regulated process value.
    :param proportional_gain: proportional gain of controller.
    :param integral_gain: integral gain of controller.
    '''
    def __init__(self, target_value : float = 10, init_value : float = 25, proportional_gain : float = 0.010,
                 integral_gain : float = 0.1) -> None:
        self.reset(target_value, init_value, proportional_gain, integral_gain)

    def __str__(self) -> str:
        return "PI"

    def get_signal(self, last_value : float, last_time : int, time_before_that : int) -> float:
        '''
        Get response from the controller.
        :param last_value: last value of controlled object.
        :param last_time: unused, last time of the measurement
        :param time_before_that: unused, time before the last_time
        '''
        self.errors.append(self.target_value - last_value)
        return self.proportional_gain * (self.errors[-1]
                                         + ((SAMPLING / self.integral_gain) * sum(self.errors)))

    def get_errors(self) -> list:
        """Get all measurement errors detected by controller."""
        return self.errors

    def reset(self, target_value : float = 10, init_value : float = 25, proportional_gain : float = 0.010, integral_gain : float = 0.1) -> None:
        """Change parameters of the controller and reset measurements."""
        self.target_value = target_value
        self.errors = [target_value - init_value]
        self.proportional_gain = proportional_gain # T_p (1)
        self.integral_gain = integral_gain # T_i (1)
