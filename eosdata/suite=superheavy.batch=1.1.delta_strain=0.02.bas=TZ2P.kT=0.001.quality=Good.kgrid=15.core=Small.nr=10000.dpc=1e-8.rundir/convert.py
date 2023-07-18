#!/usr/bin/env python

import numpy as np

"""
From
#    V [A^3/n_atoms]               E [eV]         OK
to:
#    a [Ang]  V [Ang] E [Ang]
#
with n_atoms == 1
"""

import sys
import abipy.core.abinit_units as abu
path = sys.argv[1]
data = np.loadtxt(path, usecols=[0,1])

new_data = np.empty((len(data[:,0]), 3))
# l = 2^(1/6) * V^(1/3)
new_data[:,0] = (data[:,0]**(1/3.)) * (2**(1/6.))
# Volume
new_data[:,1] = data[:,0]
# Ene in Ha
new_data[:,2] = data[:,1] / abu.Ha_to_eV

#print(new_data)

print("# l [Ang]  V [Ang^3] E [Hartree]")
for line in new_data:
    print(line[0], line[1], line[2])


