# PDEngine - Process Dynamics Engine

Process Dynamics Engine (PDEngine) is an online, iterative simulator for process control models described by transfer functions or state space representations. PDE is implemented in Python and uses the [Python Control Systems Library](https://github.com/python-control/python-control). Users can interact with the simulation by using an API to send control actions (e.g. increasing a reflux rate or shutting off a valve) and query process variables like temperature and pressure. PDE is intended to be an educational tool in chemical engineering process control courses.

## Usage

Models are defined by inheriting from the `Model` parent class. An example using the Wood-Berry distillation model (3 inputs - 2 MVs, 1 FF & 2 outputs) is provided in `/src/WoodBerryModel.py`.

A PDEngine Model must include:
- Name (e.g. Wood-Berry Distillation)
- Input names (e.g. $R$ - Reflux flow rate, $S$ - Steam flow rate, $F$ - Feed flow rate)
- Ouput names (e.g. $X_D$ - top composition, $X_B$ - bottom composition)
- Steady-state values for inputs and outputs
- Validity limits for inputs and outputs
- Typical moves for inputs

A driver program is then created to set up the simulation and initialize the model. Users must define:

- The simulation step size, $dt$
- Simulation speed, in terms of a time delay, $T_D$ between steps

```python
wm = WoodBerryModel()
dt=0.02 # in minutes, for the Wood-Berry model
woodberry = wm.create_system(dt=dt) # make the actual generator with step size = 0.02
```

At each iteration of the simulation, users can send values to the simulation by using `send()` with a dictionary with the Input names as keys:

```python
# the main engine loop
for i in range(N):        
    y = woodberry.send({'R': 0.01, 'S': 0.01, 'F': 0.05}) # send this value to the model
    time.sleep(0.001) # this is the time delay T_D for the simulation speed
```

An example driver program is provided in the `Example.ipynb` notebook that uses the Wood-Berry distillation example.
