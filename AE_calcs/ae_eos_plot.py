#!/usr/bin/env python

import sys
import numpy as np

try:
    data = np.loadtxt(sys.argv[1])
except:
    print("Usage: ae_eos_plot.py FILE")
    sys.exit(1)

Ha_to_eV = 27.21138386
data[:,2] *= Ha_to_eV

d = dict(alist_ang=data[:,0], volumes_ang=data[:,1], etotals_ev=data[:,2])

import matplotlib.pyplot as plt

plt.plot(d["volumes_ang"], d["etotals_ev"])
plt.xlabel("V (Ang^3)")
plt.ylabel("E (eV)")
plt.title(sys.argv[1])
plt.show()
