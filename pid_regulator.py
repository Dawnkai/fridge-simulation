class PID_Regulator:
    def __init__(self, target_value = 40, kp = 1.0, ki = 0.01, kd = 0.0):
        self.target_value = target_value
        self.error = [self.target_value]
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.I = 0
        
    def get_signal(self, last_value, last_time, time_before_that):
        self.error.append(self.target_value - last_value)
        P = self.error[-1] * self.kp
        I = self.I + self.ki * self.error[-1] * (last_time - time_before_that)
        D = self.kd * (self.error[-1] - self.error[-2]) / (last_time - time_before_that)
        return (P + I + D)

    def get_errors(self):
        return self.error
