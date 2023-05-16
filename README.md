# Refrigerator simulation

### Installation
```bash
$ git clone https://github.com/Dawnkai/iss.git
```

```bash
$ pip install -r requirements.txt
```

### Running

1. With `matplotlib`:
```bash
$ python script.py
```

2. With `dash`:
```bash
$ python main.py
```

### Files
* `controllers/fuzzy_controller.py` - Fuzzy controller script
* `controllers/pi_controller.py` - PI controller script
* `controllers/pid_controller.py` - PID controller script
* `matplotlib_tests/script_refrigerator.py` - example script for testing simulation results for refrigerator in matplotlib
* `matplotlib_tests/script_tempomat.py` - example script for testing simulation results for tempomat in matplotlib
* `processes/tempomat.py` - tempomat simulation process
* `processes/refrigerator.py` - refrigerator simulation process
* `constants.py` - contant values shared by all scripts
* `database_script.sql` - SQL script for generating all necessary tables
* `database.py` - script for communicating with SQLite database
* `main.py` - main file, starts the whole application
* `simulation.py` - script for running simulation (takes into consideration chosen process and regulator)
* `utils.py` - utility functions for generating GUI (figures and controls)
