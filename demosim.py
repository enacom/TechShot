from des_model import DES_model
from des_simulator import DES_simulator
import numpy as np
import matplotlib.pyplot as plt

# build model
d = np.array([[320.0e3, 800.0e3]])  # port-terminal distance (m)
tu = np.array([[4 * 3600.0]])  # unloading time (s)
tl = np.array([[8 * 3600.0], [8 * 3600.0]])  # loading time (s)
v = np.array([40 / 3.6])  # train speed (m/s)
L = np.array([5.0e6])  # train load (kg)
ntmax = 5  # maximum number of trains

# simulate model
T = 2 * 24 * 3600  # time horizon (s)
for i in range(1, ntmax):
    # model
    nt = np.array([i], dtype=int)  # train count of each model
    model = DES_model(d, tu, tl, nt, v, L)

    # simulation
    simulator = DES_simulator()
    simulator.simulate(model, T)

# graphical ouptut