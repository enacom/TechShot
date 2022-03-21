from des_model import DES_model
from des_simulator import DES_simulator
import numpy as np

# build model
d = np.array([[40.0e3]]) # port-terminal distance (m)
tu = np.array([[4*3600.0]]) # unloading time (s)
tl = np.array([[8*3600.0]]) # loading time (s)
nt = np.array([2],dtype=int) # train count of each model
v = np.array([40/3.6]) # train speed (m/s)
L = np.array([5.0e6]) # train load (kg)
model = DES_model(d, tu, tl, nt, v, L)

# simulate model
simulator = DES_simulator()
T = 24*3600 # time horizon (s)
simulator.simulate(model, T)