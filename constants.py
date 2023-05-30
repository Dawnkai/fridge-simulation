"""Constants shared between all scripts."""


#For cruise control
# Maximum controller response
MAX_RESPONSE = 1500.0#N
# Minimum controller response
MIN_RESPONSE = -1500.0#N
# Minimum allowed signal to the controlled process
MIN_SIGNAL = -10#V
# Maximum allowed signal to the controlled process
MAX_SIGNAL = 10#V

#For refrigerator
# Maximum temperature change
MAX_TEMPERATURE_CHANGE = 50.0#C
# Minimum temperature change
MIN_TEMPERATURE_CHANGE = -50.0#C
# Minimum worked performed by refrigerator
MIN_WORK = 0#W
# Maximum worked performed by refrigerator
MAX_WORK = 2000#W


# Mass of the controlled object
MASS = 1200#kg
# Resistance of the environment
RESISTANCE = 0.75
# Simulation sampling rate
SAMPLING = 0.1#s
# Simulation time
SIMULATION_TIME = 100#s
# Filepath to database with results
DB_FILEPATH = "database.db"
# Number of simulations displayed on the result graph
NUM_SIMULATIONS = 8


# Mass of water cooled in refrigerator 
WATER_MASS = 0.15 #m [kg]
# Specific heat of water
WATER_SPECIFIC_HEAT = 3.33 * 105 #c [J/kg]
# Temperature of hot reservoir
RESERVOIR_HOT = 293 #T_h [K] 
# Temperature of cold reservoir
RESERVOIR_COLD = 273 #T_l [K] 


