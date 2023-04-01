class PI_Regulator:
    def __init__(self, target_value = 40, proportional_gain = 0.010, integral_gain = 0.1):
        self.target_value = target_value #m/h [Vs]
        self.error = [self.target_value]
        self.proportional_gain = proportional_gain # T_p (1)
        self.integral_gain = integral_gain # T_i (1)
    
    def get_signal(self, last_value, last_time, time_before_that):
        self.error.append(self.target_value - last_value)
        return self.proportional_gain * (self.error[-1] + ((self.proportional_gain / self.integral_gain) * sum(self.error)))

    def get_errors(self):
        return self.error
