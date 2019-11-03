#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import cmath
import matplotlib.pyplot as plt
from two_dimensions import one_dimensional_model


# Matplotlib parameters
plt.rcParams.update({'font.size': 18})
plt.rc('text', usetex=True)
plt.rc('font', family='serif')
plt.rc('font', weight='bold')
plt.rcParams['text.latex.preamble'] = [r'\usepackage{amssymb} \usepackage{sfmath} \boldmath']


a = 1
vec_base = [np.array([a,0]), np.array([0,a])]
mass = 1
k = 1
num_cells_x = 51
num_cells_y = 51

system = one_dimensional_model(vec_base,mass,k,num_cells_x,num_cells_y)

# Define k vector
# X to Gamma
index_x = np.linspace(-int(num_cells_x/2), int(num_cells_x/2), int(num_cells_x))
k_0 = np.array([(2*np.pi*i/(num_cells_x*a),0) for i in index_x ])

w0,modes0 = system.compute_for_given_k(k_0)
w_b0,f_b0 = system.split_branches(w0,modes0)

# X to M
index_y = np.linspace(1, int(num_cells_x/2), int(num_cells_x/2))
k_1 = np.array([(np.pi/(a),2*np.pi*i/(num_cells_x*a)) for i in index_y ])

w1,modes1 = system.compute_for_given_k(k_1)
w_b1,f_b1 = system.split_branches(w1,modes1)

# M to Gamma
index = np.linspace(int(num_cells_x/2), 0, int(num_cells_x/2))
k_2 = np.array([(2*np.pi*i/(num_cells_x*a),2*np.pi*i/(num_cells_x*a)) for i in index ])

w2,modes2 = system.compute_for_given_k(k_2)
w_b2,f_b2 = system.split_branches(w2,modes2)


f, ax = plt.subplots()

ax.scatter(np.arange(len(np.concatenate((w_b0[0],w_b1[0],w_b2[0])))),np.concatenate((w_b0[0],w_b1[0],w_b2[0])))
ax.scatter(np.arange(len(np.concatenate((w_b0[0],w_b1[0],w_b2[0])))),np.concatenate((w_b0[1],w_b1[1],w_b2[1])))

ax.set_xlabel(r"$k$",fontsize=26)
ax.set_ylabel(r"$\omega$",fontsize=26)

ax.axvline(x=0)
ax.axvline(x=int(num_cells_x/2))
ax.axvline(x=int(num_cells_x))
ax.axvline(x=int(num_cells_x/2)+int(num_cells_x))
ax.axvline(x=2*int(num_cells_x))

ax.set_xticks([0, int(num_cells_x/2), int(num_cells_x), int(num_cells_x/2)+int(num_cells_x), 2*int(num_cells_x) ])
ax.set_xticklabels([r'$-X$',r'$\Gamma$',r'$X$', r'$M$', r'$\Gamma$'])

plt.tight_layout()
plt.show()
