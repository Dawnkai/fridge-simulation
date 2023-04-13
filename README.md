# Levitating Ball Simulation

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

* `utils.py` - GUI controls, app layout and result graph generation
* `main.py` - dash application
* `pi_regulator.py` - PI regulator
* `pid_regulator.py` - PID regulator
* `fuzzy_regulator.py` - Fuzzy regulator
* `script.py` - quick matplotlib visualisation
* `simulation.py` - running simulation with specified regulator and process type
* `tempomat.py` - tempomat process
* `database.py` - database driver for DB connection
