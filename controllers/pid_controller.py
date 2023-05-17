"""PID controller component."""
from constants import SAMPLING

class PID_Controller:
    '''
    PID controller object.
    :param target_value: target regulated process value.
    :param proportional_coefficient: proportional coefficient of controller.
    :param integral_coefficient: integral coefficient of controller.
    :param derivative_coefficient: derivative coefficient of controller
    '''
    def __init__(self, target_value : float = 10, init_value : float = 25, proportional_coefficient : float = 1.0,
                 integral_coefficient : float  = 1.0, derivative_coefficient : float  = 1.0) -> None:
        self.reset(target_value, init_value, proportional_coefficient, integral_coefficient, derivative_coefficient)

    def __str__(self) -> str:
        return "PID"

    def get_signal(self, last_value : float, last_time : int, time_before_that : int) -> float:
        '''
        Get response from PID controller.
        :param last_value: last value of controlled object.
        :param last_time: latest measurement time.
        :param time_before_that: measurement time right before list_time.
        '''
        self.errors.append(self.target_value - last_value)
        integral_part = (SAMPLING / self.integral_coefficient) * sum(self.errors)
        derivative_part = (self.derivative_coefficient / SAMPLING) * (self.errors[-1] - self.errors[-2])
        return self.proportional_coefficient * (self.errors[-1] + integral_part + derivative_part)

    def get_errors(self) -> list:
        """Get all measurement errors detected by controller."""
        return self.errors

    def reset(self, target_value : float = 10, init_value : float = 25, proportional_coefficient : float = 1.0,
              integral_coefficient : float  = 0.01, derivative_coefficient : float  = 0.0) -> None:
        """Change parameters of the controller and reset measurements."""

        self.target_value = target_value
        self.errors = [target_value - init_value]
        self.proportional_coefficient = proportional_coefficient
        self.integral_coefficient = integral_coefficient
        self.derivative_coefficient = derivative_coefficient
        self.sums = 0
