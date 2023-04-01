# Levitation Ball Simulation

### Installation
```bash
$ pip install plotly pandas dash dash-bootstrap-components 
```

```bash
$ git clone https://github.com/Dawnkai/iss.git
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

* `controls.py` - main controls for setting simulation variables (regulator type, regulator parameters, etc)
* `main.py` - dash application
* `pi_regulator.py` - PI regulator
* `pid_regulator.py` - PID regulator
* `script.py` - quick matplotlib visualisation
* `simulation.py` - running simulation with specified regulator and process type
* `tempomat.py` - tempomat process
