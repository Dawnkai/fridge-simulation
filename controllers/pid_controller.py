"""PID controller component."""

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
        self.errors.append(abs(self.target_value - last_value))
        delta_time = last_time - time_before_that
        integral_error = self.errors[-1] * delta_time
        derivative_error = (self.errors[-1] - self.errors[-2]) / delta_time
        return self.proportional_coefficient * self.errors[-1] + self.integral_coefficient * integral_error + self.derivative_coefficient * derivative_error

    def get_errors(self) -> list:
        """Get all measurement errors detected by controller."""
        return self.errors

    def reset(self, target_value : float = 10, init_value : float = 25, proportional_coefficient : float = 1.0,
              integral_coefficient : float  = 0.01, derivative_coefficient : float  = 0.0) -> None:
        """Change parameters of the controller and reset measurements."""

        self.target_value = target_value
        self.errors = [abs(init_value - target_value)]
        self.proportional_coefficient = proportional_coefficient
        self.integral_coefficient = integral_coefficient
        self.derivative_coefficient = derivative_coefficient
        self.sums = 0
