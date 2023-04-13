class PID_Regulator:
    def __init__(self, target_value : float = 20, kp : float = 1.0, ki : float  = 0.01, kd : float  = 0.0) -> None:
        self.reset(target_value, kp, ki, kd)
    
    def __str__(self) -> str:
        return "PID"
        
    def get_signal(self, last_value : float, last_time : int, time_before_that : int) -> float:
        self.error.append(self.target_value - last_value)
        P = self.error[-1] * self.kp
        I = self.I + self.ki * self.error[-1] * (last_time - time_before_that)
        D = self.kd * (self.error[-1] - self.error[-2]) / (last_time - time_before_that)
        return (P + I + D)

    def get_errors(self) -> list:
        return self.error
    
    def reset(self, target_value : float = 20, kp : float = 1.0, ki : float  = 0.01, kd : float  = 0.0) -> None:
        self.target_value = target_value
        self.error = [self.target_value]
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.I = 0
