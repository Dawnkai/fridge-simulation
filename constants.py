"""Constants shared between all scripts."""

# Maximum controller response
MAX_RESPONSE = 1500.0#N
# Minimum controller response
MIN_RESPONSE = -1500.0#N
# Minimum allowed signal to the controlled process
MIN_SIGNAL = -10#V
# Maximum allowed signal to the controlled process
MAX_SIGNAL = 10#V
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

# Minimum refrigerator work input
MIN_WORK = 0 #[W]
# Maximum refrigerator work input
MAX_WORK = 500 #[W]
# Mass of water cooled in refrigerator 
WATER_MASS = 0.5 #m [kg]
# Specific heat of water
WATER_SPECIFIC_HEAT = 4182 #m [J/kg /C]
# Energy efficiency rating
EER = 18 
