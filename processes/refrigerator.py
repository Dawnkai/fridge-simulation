"""Cooling water in refrigerator process."""

class Refrigerator:
    """Cooling water in refrigerator process object."""
    def __init__(self) -> None:
        
        # Limits
        self.min_work = 0 #[W]
        self.max_work = 500 #[W]

        self.water_mass = 0.5 #m [kg]
        self.water_specific_heat = 4182 #m [J/kg /C]
        self.eer = 18 # energy efficiency rating

        self.reset()

    def __str__(self) -> str:
        return "Refrigerator"

   

    def add_signal(self, signal : float, sampling : float) -> None:
        '''
        Calculate system response and environment variables.
        :param signal: signal from the controller.
        :param sampling: sampling rate of the simulation.
        '''
        self.work_measurements.append(min(self.max_work, max(self.min_work, -1*signal)))

        #(1055.05 * EER * W)/(3600)
        #1055.05 comes from calculating heat transfer from btu to Joules
        #3600 comes from dividing time in hours and seconds from original formula 
        self.heat_transfer_measurements.append((1055.05 * self.eer * self.work_measurements[-1])/3600)

        #Q= m * c * temperature change, so T = T[-1] + Q/mc
        self.temperature_measurements.append( 
            self.temperature_measurements[-1] -  sampling * (self.heat_transfer_measurements[-1] 
            / (self.water_mass*self.water_specific_heat) )
        ) 

    def get_latest_measurement(self) -> float:
        """Get latest temperature measurement."""
        return self.temperature_measurements[-1] 

    def get_results(self) -> list:
        """Get process display results."""
        return [self.temperature_measurements, self.work_measurements, self.heat_transfer_measurements]

    def reset(self, init_value : float = 25.0) -> None:
        """Reset process."""
        # Measurements
        self.work_measurements = [0.0]
        self.temperature_measurements = [init_value]
        self.heat_transfer_measurements=[0.0]
        
        
