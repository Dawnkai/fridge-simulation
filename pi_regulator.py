class PI_Regulator:
    def __init__(self, target_value : float = 40, proportional_gain : float = 0.010, integral_gain : float = 0.1) -> None:
        self.reset(target_value, proportional_gain, integral_gain)
    
    def __str__(self) -> str:
        return "PI"
    
    def get_signal(self, last_value : float, last_time : int, time_before_that : int) -> float:
        self.error.append(self.target_value - last_value)
        return self.proportional_gain * (self.error[-1] + ((self.proportional_gain / self.integral_gain) * sum(self.error)))

    def get_errors(self) -> list:
        return self.error
    
    def reset(self, target_value : float = 40, proportional_gain : float = 0.010, integral_gain : float = 0.1) -> None:
        self.target_value = target_value
        self.error = [self.target_value]
        self.proportional_gain = proportional_gain # T_p (1)
        self.integral_gain = integral_gain # T_i (1)
