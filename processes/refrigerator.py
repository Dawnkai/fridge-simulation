"""Cooling water in refrigerator process."""
from constants import MIN_WORK, MAX_WORK, WATER_MASS, WATER_SPECIFIC_HEAT, RESERVOIR_HOT, RESERVOIR_COLD

class Refrigerator:
    """Cooling water in refrigerator process object."""
    def __init__(self) -> None:

        self.water_mass = WATER_MASS #m [kg]
        self.water_specific_heat = WATER_SPECIFIC_HEAT #c [J/kg]
        self.temp_high = RESERVOIR_HOT #T_h [K]
        self.temp_low = RESERVOIR_COLD #T_l [K]
        
        self.reset()

    def __str__(self) -> str:
        return "Refrigerator"
    
   

    def add_signal(self, signal : float, sampling : float) -> None:

        '''
        Calculate system response and environment variables.
        :param signal: signal from the controller.
        :param sampling: sampling rate of the simulation.
        '''
        
        
        self.work_measurements.append( sampling * min(50, max(-50,  signal)))

        
        #coefficient = -T_l / m * c * (T_h - T_l)
        coefficient = -self.temp_low / (
             self.temp_high-self.temp_low)

        #[T[-1] - sampling * (work * coefficient/(mass*specific heat of water put in refrigerator)) ]
        self.temperature_measurements.append( 
             ( self.temperature_measurements[-1]  - sampling *
               ( self.work_measurements[-1] *  coefficient/(self.water_mass* self.water_specific_heat)))
        )    

        #mass * specific heat * change in temperature
        self.heat_measurements.append(self.water_mass * self.water_specific_heat *
                                       (self.temperature_measurements[-1]-self.temperature_measurements[-2]))
        
        
         

        
    def get_latest_measurement(self) -> float:
        """Get latest temperature measurement."""
        return self.temperature_measurements[-1] 

    def get_results(self) -> list:
        """Get process display results."""
        return [self.temperature_measurements, self.work_measurements, self.heat_measurements]

    def reset(self, init_value : float = 25.0) -> None:
        """Reset process."""
        # Measurements
        self.work_measurements = [0.0]
        self.temperature_measurements = [ init_value]
        self.heat_measurements=[0.0]
        
        
