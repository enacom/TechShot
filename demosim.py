from des_model import DES_model
from des_simulator import DES_simulator
import numpy as np
import matplotlib.pyplot as plt

# build model
d = np.array([[320.0e3]])  # port-terminal distance (m)
tu = np.array([[4 * 3600.0]])  # unloading time (s)
tl = np.array([[8 * 3600.0]])  # loading time (s)
v = np.array([40 / 3.6])  # train speed (m/s)
L = np.array([5.0e6])  # train load (kg)
ntmax = 8  # maximum number of trains

tc = tu[0][0] + tl[0][0] + 2 * d[0][0] / v[0]
ntm = tc / tl[0][0]

# simulate model
T = 50 * 24 * 3600  # time horizon (s)
Pn = [0]  # numerical productivity (kg/s)
Pa = [0]  # analytical productivity (kg/s)
tq = [0]  # queue time (s)
n = [0]  # number of trains
for i in range(1, ntmax):
    # model
    nt = np.array([i], dtype=int)  # train count of each model
    model = DES_model(d, tu, tl, nt, v, L)

    # simulation
    simulator = DES_simulator()
    simulator.simulate(model, T)
    Pt, P, t = model.productivity()  # [kg/s], [kg], [s]
    tq.append(model.queue_time())

    # log
    n.append(i)
    Pn.append(Pt[-1])
    Pa.append(min(nt[0], ntm) * L[0] / tc)

    # line command output
    print('\n Numerical productivity {:.0f}'.format(Pt[-1] * 3.6))
    print('Analytical productivity {:.0f}'.format(Pa[-1] * 3.6))

    # graphical output
    if False:
        hf, ha = plt.subplots()
        plt.plot(t / 3600, Pt * 3.6)
        plt.xlabel('time (hours)')
        plt.ylabel('productivity (ton/hour)')
        plt.title('{} trains'.format(i))

# graphical ouptut
hf, ha = plt.subplots()
plt.plot(np.array(n), np.array(Pn) * 3.6, label='numerical')
plt.plot(np.array(n), np.array(Pa) * 3.6, label='analytical')
plt.xlabel('number of trains')
plt.ylabel('productivity (ton/hour)')
plt.title('{} trains'.format(i))
plt.legend()

hf, ha = plt.subplots()
plt.plot(np.array(n), np.array(tq) / 3600)
plt.xlabel('number of trains')
plt.ylabel('queue time (hours)')
plt.title('{} trains'.format(i))

plt.show()