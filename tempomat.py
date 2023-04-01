class Tempomat:
    def __init__(self):
        self.mass = 1200
        self.resistance = 0.75
        
         # Limits
        self.min_pull_force = -1500.0 #N [Fcmin]
        self.max_pull_force = 1500.0 #N [Fcmax]
        self.min_signal = -10 #V [Umin]
        self.max_signal = 10 #V [Umax]
        
        # Measurements
        self.velocity_measurements = [0.0]
        self.position_measurements = [0.0]
        self.pull_force = 0 #N [Fc]
        self.signals = [0.0] #V [U]
    
    def get_signal_response(self, signal):
        # a = (Fmax - Fmin) / (umax - umin)
        coefficient = (self.max_pull_force - self.min_pull_force) / (self.max_signal - self.min_signal)
        return (coefficient * (signal - self.min_signal)) + self.min_pull_force
    
    def add_signal(self, signal, sampling):
        self.signals.append(min(self.max_signal, max(self.min_signal, signal)))
        self.pull_force = self.get_signal_response(self.signals[-1])
        # v(n+1) = Tp * (Fc(n) - beta*v(n)^2)*m + v(n)
        self.velocity_measurements.append(sampling * (self.pull_force - (self.resistance*self.velocity_measurements[-1]**2)) / self.mass + self.velocity_measurements[-1])
        # x = v[-2] * p + x[-1]
        self.position_measurements.append(sampling * self.velocity_measurements[-2] + self.position_measurements[-1])
    
    def get_latest_measurement(self):
        return self.velocity_measurements[-1]
    
    def get_results(self):
        return [self.velocity_measurements, self.position_measurements, self.signals]
