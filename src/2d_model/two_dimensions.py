#!/usr/bin/env python
# -*- coding: utf-8 -*-

###########################
#   1) Import libraries   #
###########################
import numpy as np
import cmath


class one_dimensional_model(object):

    def __init__(self,vec_base,mass,k,num_cells_x,num_cells_y):
        self.vec_base = vec_base
        self.a1 = np.sqrt(vec_base[0][0]**2 + vec_base[0][1]**2)
        self.a2 = np.sqrt(vec_base[1][0]**2 + vec_base[1][1]**2)
        self.a_mean = (self.a1+self.a2)/2
        self.mass = mass
        self.k = k
        self.num_cells_x = num_cells_x
        self.num_cells_y = num_cells_y
        self.rx = self.a1*num_cells_x
        self.ry = self.a2*num_cells_y

        self.num_atoms = num_cells_x * num_cells_y

        self.position_vec = np.array([i*vec_base[0]+j*vec_base[1] for i in range(num_cells_x) for j in range(num_cells_y)])

        ##################################
        # Define the interacting neighbors
        r1 = vec_base[0]
        r2 = -vec_base[0]
        r3 = vec_base[1]
        r4 = -vec_base[1]
        r5 =  vec_base[0] + vec_base[1]
        r6 =  vec_base[0] - vec_base[1]
        r7 = -vec_base[0] + vec_base[1]
        r8 = -vec_base[0] - vec_base[1]

        self.R_vec = [np.array([0,0]),r1,r2,r3,r4,r5,r6,r7,r8]

        ##############################
        # Compute the Rigidity matrix
        K = np.zeros((2*1,2*9))

        # i) Interaction with neighbors
        for i in range(2):
            for index_primitive_cell,r in enumerate(self.R_vec):
                if index_primitive_cell == 0:
                    pass
                else:
                    for j in range(2):
                        if r[i]==0:
                            pass
                        else:
                            K[i,index_primitive_cell*2+j] = -self.k * abs(r[j])/(r[0]**2+r[1]**2)**2
                            if j==0:
                                K[i,0] = K[i,0] + self.k * abs(r[j])/(r[0]**2+r[1]**2)**2
                            elif j==1:
                                K[i,1] = K[i,1] + self.k * abs(r[j])/(r[0]**2+r[1]**2)**2

        #Save K
        self.K_matrix = K
        print(K)

        #############################################
        # Compute vectors in the first Brillouin zone
        index_x = np.linspace(-int(num_cells_x/2), int(num_cells_x/2), num_cells_x)
        index_y = np.linspace(-int(num_cells_y/2), int(num_cells_y/2), num_cells_y)

        self.k_vec = np.array([(2*np.pi*i/(num_cells_x*self.a1),(2*np.pi*j/(num_cells_x*self.a2))) for i in index_x for j in index_y])
        print(self.k_vec)


    def _compute_eigenfrequencies(self,k):
        eigenfreqs = np.zeros(2)
        eigenmodes = [[] for i in range(2)]

        #Compute dynamical matrix
        D = np.zeros((2,2), dtype=np.complex128)

        #Loop on x and y
        for i in range(2):
            for j in range(2):
                #loop on the 2 neighbooring cells and the cell itself
                for index,r in enumerate(self.R_vec):
                    #print(np.exp(complex(0,1)*np.dot(k,r)))
                    #print(self.K_matrix[i,index*2+j])
                    #print()
                    D[i,j] = D[i,j] + self.K_matrix[i,index*2+j]*np.exp(complex(0,1)*np.dot(k,r))

        D = 1/(self.mass) * D
        #print(D)

        #Compute eigenvalues and eigenmodes
        w, v = np.linalg.eig(D)
        w = np.sort(w)

        for i in range(2):
            eigenfreqs[i] = np.sqrt(w[i].real)
            eigenmodes[i] = v[i]

        return eigenfreqs,eigenmodes


    def compute_all_1ZB(self):
        w = [np.array([]) for i in range(self.num_cells_x * self.num_cells_y)]
        modes = [np.array([]) for i in range(self.num_cells_x * self.num_cells_y)]

        for i,k in enumerate(self.k_vec):
            w[i],modes[i] = self._compute_eigenfrequencies(k)

        return w,modes


    def compute_for_given_k(self,k_v):
        w = [np.array([]) for i in range(len(k_v))]
        modes = [np.array([]) for i in range(len(k_v))]

        for i,k in enumerate(k_v):
            w[i],modes[i] = self._compute_eigenfrequencies(k)

        return w,modes


    def split_branches(self,w,modes):
        w_branches = [np.array([]) for i in range(2)]
        f_branches = [np.array([]) for i in range(2)]
        for i in range(2):
            w_branches[i] = np.array([ f[i] for f in w ])
            f_branches[i] = np.array([ f[i] for f in modes ])
        return w_branches, np.array(f_branches)


    def compute_amplitude_and_phase(self,modes):
        phase_func = np.vectorize(cmath.phase)

        phase = phase_func(modes)
        ampl = abs(modes)

        return phase, ampl


    def compute_displacement(self,f_branches,w_branches,w,k,t):

        phase,ampl = self.compute_amplitude_and_phase(f_branches)

        for i in range(2):
            if w in w_branches[i]:
                branch_index = i
                k_index = np.where(w_branches[i] == w)[0][0]
            else:
                pass

        phases_diff = phase[branch_index][k_index]
        ampl = ampl[branch_index][k_index]

        #
        phase = np.ones(self.num_cells_x*self.num_cells_y) * phases_diff
        amplitude_x = ampl[0] * np.ones(self.num_cells_x*self.num_cells_y)
        amplitude_y = ampl[1] * np.ones(self.num_cells_x*self.num_cells_y)

        np.array([j*i for j in np.ones(self.num_cells) for i in ampl])

        #
        displacement_x = ampl[0] * np.sin( np.dot(k,self.position_vec) - w*t*np.ones(self.num_cells_x*self.num_cells_y)  )
        displacement_y = ampl[1] * np.sin( np.dot(k,self.position_vec) - w*t*np.ones(self.num_cells_x*self.num_cells_y) + phase )

        return (displacement_x, displacement_y)
