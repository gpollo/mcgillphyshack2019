#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Description : Initial 1D model for 2 different atoms in a primitive cell

###########################
#   1) Import libraries   #
###########################
import numpy as np
import matplotlib.pyplot as plt
import cmath
from matplotlib import animation


# Matplotlib parameters
plt.rcParams.update({'font.size': 18})
plt.rc('text', usetex=True)
plt.rc('font', family='serif')
plt.rc('font', weight='bold')
plt.rcParams['text.latex.preamble'] = [r'\usepackage{amssymb} \usepackage{sfmath} \boldmath']

###################################
#   2) Define lattice constants   #
###################################

# i) Lattice vector
a = 1 #Spacing between atoms
r = 2*a #lattice vector

# ii) Number of atom in a primitive cell
n = 2

# iii) Position of atoms in the primitive cell
delta_r1 = -a/2
delta_r2 = a/2

delta_r_vec = np.array([delta_r1, delta_r2])

# iv) Masses of the atoms in the primitive cell
m = 1
M = 2

mass_vec = np.array([m,M])

# v) Spring constants
k12 = 1
k11 = 1
k22 = 1

k_vec = np.array([[k11, k12],[k12, k22]])

# vi) number of unit cells
num_atoms = 65

# vii) define position vector
position_vec = np.array([ k*r+delta_r_vec[i]  for k in range(num_atoms) for i in range(n) ])

######################################
#   3) define simulation constants   #
######################################

# Number of neighboring cells considered
cutoff_cells = 1
cells_considered = np.arange(-cutoff_cells, cutoff_cells+1)

# Cutoff distance where the interaction is no longer considered
cutoff_dist = 1.5*a


#####################################
#   4) Create the rigidity matrix   #
#####################################

# i) Initialize the matrix
K = np.zeros(( n , ((2*cutoff_cells+1)*n) ))

# ii) Define the constants for neighbors
for i in range(n): #atoms in primitive cell
    for j in range(2*cutoff_cells+1): #considered cell
        for k in range(n):  #atoms in the considered cell
            dist1 = delta_r_vec[i]
            dist2 = cells_considered[j]*r + delta_r_vec[k]
            dist = abs( (delta_r_vec[i]) - (cells_considered[j]*r + delta_r_vec[k]) )

            if cells_considered[j]==0 and i==k:
                pass

            elif dist > cutoff_dist:
                pass

            else:
                K[i,j*n+k] = -k_vec[i,k]

# iii) Self interaction (acoustic sum rule)
for i in range(n):
    K[i,cutoff_cells*n+i] = -sum(K[i,:])

print(K)

#########################################################
#   5) Compute the vectors in the First Brillouin Zone  #
#########################################################

index = np.linspace(-int(num_atoms/2), int(num_atoms/2), num_atoms)

k_vec = np.array([2*np.pi*i/(num_atoms*r) for i in index])


#######################################################################################
#   6) Compute the dynamical matrix and eigenfrequecies for every point in the 1ZB    #
#######################################################################################

w_vec = np.zeros(n*num_atoms)
w_vec1 = np.zeros(num_atoms)
w_vec2 = np.zeros(num_atoms)

k_real_vec = [ [0]  for i in range(n*num_atoms) ]

ampl  = np.zeros(n*num_atoms)
phase = np.zeros(n*num_atoms)

for index,k in enumerate(k_vec):
    #i) Dynamical matrix
    D = np.zeros(( n,n ), dtype=np.complex128)
    for i in range(n):
        for j in range(n):

            for l in range(2*cutoff_cells+1):
                D[i,j] = D[i,j] + K[i, l*n+j]*np.exp(complex(0,1)*k*cells_considered[l]*r)

            D[i,j] = 1/np.sqrt(mass_vec[i]*mass_vec[j]) * D[i,j]

    print(D)
    #ii) Eigenfrequecies
    w, v = np.linalg.eig(D)


    for i in range(n):
        w_vec[index*n+i] = np.sqrt(w[i].real)
        k_real_vec[index*n+i] = v[i]

    w_vec1[index] = np.sqrt(w[0].real)
    w_vec2[index] = np.sqrt(w[1].real)
    print(v)
    #Compute Phase and amplitude factor
    for i in range(n):
        ampl[index*n+i]  = np.sqrt(v[i][0].conjugate()*v[i][0]).real/np.sqrt(v[i][1].conjugate()*v[i][1]).real
        phase[index*n+i] = cmath.phase(v[i][0])-cmath.phase(v[i][1])
    print()

# Create the vector determining the oscillations (a[0]*cos(kr-wt+a[1])
#mod_phase = [[np.sqrt(i[j].conjugate()*i[j]).real, cmath.phase(i[j])] for i in k_real_vec for j in range(n)]
#print(mod_phase)
print(ampl)
print(phase)



#########################
#   7) Display result   #
#########################

# i) Display dispersion relation
f, ax = plt.subplots()

ax.scatter(k_vec,w_vec1)
ax.scatter(k_vec,w_vec2)

ax.set_xlabel(r"$k$",fontsize=26)
ax.set_ylabel(r"$\omega$",fontsize=26)

ax.set_xticks([-np.pi/(2*a),0,np.pi/(2*a)])
ax.set_xticklabels([r'$-\pi/r$',r'$0$',r'$\pi/r$'])

ax.set_xlim(-np.pi/r, np.pi/r)
ax.set_ylim(0)


for axis in ['top','bottom','left','right']:
  ax.spines[axis].set_linewidth(1.5)
ax.tick_params(width=1.5)

plt.tight_layout()
plt.show()


# ii) Display animation of atoms for a given mode

mode_display = (6,1) #functionning: (a,b) a for the k_n and b for the branch -> a*n+b

k_n = k_vec[mode_display[0]]

w = w_vec[mode_display[0]*n+mode_display[1]]
#mode_phase1 = mode_phase(mode_display)
#mode_phase2 =


f, ax = plt.subplots()

for i,pos in enumerate(position_vec):
    if i%2==0:
        ax.scatter(pos,0,color='b')
    else:
        ax.scatter(pos,0,color='r')

t = 0
def animate(i):
    t = 0.5*i
    ax.clear()

    phase = np.pi

    #Compute new positions
    displacement = np.zeros(n*num_atoms)
    for i in range(num_atoms):
        for j in range(n):
            if j==0:
                displacement[i*n+j] = 0.2*1/m * np.cos(k_n*position_vec[i*n+j] - w*t)
            elif j==1:
                displacement[i*n+j] = 0.2*1/M * np.cos(k_n*position_vec[i*n+j] - w*t + phase)

    #Draw new plot
    for index,i in enumerate(position_vec):
        if index%2==0:
            ax.scatter(i+displacement[index],0,color='b')
        else:
            ax.scatter(i+displacement[index],0,color='r')

    print(i)

interval = 0.0001
i#plt.tight_layout(rect=[0, 0.03, 1, 0.95])
anim = animation.FuncAnimation(f,animate,blit=False)
#anim.save('2D_oneslit.mp4', fps=15, extra_args=['-vcodec', 'libx264'])

plt.show()
