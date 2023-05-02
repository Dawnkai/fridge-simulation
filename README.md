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

* `matplotlib_tests/script_refrigerator.py` - example script for showing example simulation results for refrigerator in matplotlib
* `matplotlib_tests/script_tempomat.py` - example script for showing example simulation results for tempomat in matplotlib
* `processes/tempomat.py` - tempomat simulation process
* `processes/refrigerator.py` - refrigerator simulation process
* `regulators/fuzzy_regulator.py` - Fuzzy regulator
* `regulators/pi_regulator.py` - PI regulator
* `regulators/pid_regulator.py` - PID regulator
* `constants.py` - contant values shared by all scripts
* `database.py` - script for communicating with SQLite database
* `database_script.sql` - SQL script for generating all necessary tables
* `main.py` - main file, starts the whole application
* `simulation.py` - script with simulation description (takes into consideration chosen process and regulator)
* `utils.py` - utility functions for generating GUI (figures and controls)
