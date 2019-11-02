#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Description : Initial 1D model for 1 different atoms in a primitive cell

###########################
#   1) Import libraries   #
###########################
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from one_dim_model import one_dimensional_model

## initialize system
n = 1
a = 1
m = 1
k0 = 1

spacing_vec = [a,a]
delta_r_vec = [0]
masse_vec = [m]
k_vec = [k0,k0]
num_cells = 21

system = one_dimensional_model(n, spacing_vec, delta_r_vec, masse_vec, k_vec, num_cells)
w,modes = system.compute_all_1ZB()

w_b,f_b = system.split_branches(w,modes)


###
plt.scatter(system.k_vec,w_b[0])

plt.show()
