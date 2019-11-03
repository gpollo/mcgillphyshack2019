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


        #K = np.array([[ 0.,    0.,   -1.,    -1/np.sqrt(2),   -1.,    -1/np.sqrt(2),    -1/np.sqrt(2),     0.,    -1/np.sqrt(2),    0.,   -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25],
        #              [ 0.,    0.,    0.,    -1/np.sqrt(2),    0.,    -1/np.sqrt(2),    -1/np.sqrt(2),    -1.,    -1/np.sqrt(2),   -1.,   -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25]])

        #K = np.array([[ 0.,    0.,   -1.,    -1,   -1.,    -1,    -1,     0.,    -1,    0.,   -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25],
        #              [ 0.,    0.,    0.,    -1,    0.,    -1,    -1,    -1.,    -1,   -1.,   -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25]])
        # ii) Self-interaction (acoustic sum rule)
        #for i in range(2):
        #    K[i, i] = -sum(K[i,:])

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
        ampl = np.abs(modes)

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
        phase1 = np.ones(self.num_cells_x*self.num_cells_y) * phases_diff[0]
        phase2 = np.ones(self.num_cells_x*self.num_cells_y) * phases_diff[1]

        #
        displacement_x = ampl[0] * np.sin( np.dot(k, self.position_vec.transpose()) - w*t*np.ones(self.num_cells_x*self.num_cells_y) + phase1 )
        displacement_y = ampl[1] * np.sin( np.dot(k, self.position_vec.transpose()) - w*t*np.ones(self.num_cells_x*self.num_cells_y) + phase2 )

        return (displacement_x, displacement_y)

from model.abstract import AbstractModel
import pygame
import pygame.gfxdraw

class TwoDimensionalModelWrapper(AbstractModel):
    def __init__(self):
        super(TwoDimensionalModelWrapper, self).__init__()

        self.a = 1
        self.vec_base = [np.array([self.a, 0]), np.array([0, self.a])]
        self.mass = 1
        self.k = 1
        self.num_cells_x = 21
        self.num_cells_y = 21

        self.system = one_dimensional_model(
            self.vec_base,
            self.mass,
            self.k,
            self.num_cells_x,
            self.num_cells_y
        )

        # Define k vector
        # X to Gamma
        self.index_x = np.linspace(
            -int(self.num_cells_x/2),
             int(self.num_cells_x/2),
             int(self.num_cells_x/1)
        )

        self.k_0 = np.array([(2*np.pi*i/(self.num_cells_x*self.a),0) for i in self.index_x])

        self.w0, self.modes0 = self.system.compute_for_given_k(self.k_0)
        self.w_b0, self.f_b0 = self.system.split_branches(self.w0, self.modes0)

        # X to M
        self.index_y = np.linspace(1, int(self.num_cells_x/2), int(self.num_cells_x/2))
        self.k_1 = np.array([(np.pi/(self.a),2*np.pi*i/(self.num_cells_x*self.a)) for i in self.index_y ])

        self.w1, self.modes1 = self.system.compute_for_given_k(self.k_1)
        self.w_b1, self.f_b1 = self.system.split_branches(self.w1, self.modes1)

        # M to Gamma
        self.index = np.linspace(int(self.num_cells_x/2), 0, int(self.num_cells_x/2))
        self.k_2 = np.array([(2*np.pi*i/(self.num_cells_x*self.a),2*np.pi*i/(self.num_cells_x*self.a)) for i in self.index])

        self.w2, self.modes2 = self.system.compute_for_given_k(self.k_2)
        self.w_b2, self.f_b2 = self.system.split_branches(self.w2, self.modes2)

        self.w_b = [
            np.concatenate((self.w_b0[0], self.w_b1[0], self.w_b2[0])),
            np.concatenate((self.w_b0[1], self.w_b1[1], self.w_b2[1])),
        ]

        self.f_b = [
            np.concatenate((self.f_b0[0], self.f_b1[0], self.f_b2[0])),
            np.concatenate((self.f_b0[1], self.f_b1[1], self.f_b2[1])),
        ]

        self.k = [
            np.concatenate((self.k_0[:,0], self.k_1[:,0], self.k_2[:,0])),
            np.concatenate((self.k_0[:,1], self.k_1[:,1], self.k_2[:,1])),
        ]

        print("test", self.k)

        self.__series = [
            (
                np.arange(len(np.concatenate((self.w_b0[0], self.w_b1[0], self.w_b2[0])))),
                np.concatenate((self.w_b0[0], self.w_b1[0],self.w_b2[0]))
            ), (
                np.arange(len(np.concatenate((self.w_b0[0], self.w_b1[0], self.w_b2[0])))),
                np.concatenate((self.w_b0[1], self.w_b1[1], self.w_b2[1]))
            )
        ]

    def get_name(self):
        return "2 dimensional"

    def get_config_widgets(self):
        return []

    def get_series(self):
        return self.__series

    def get_r(self):
        return 1

    def draw(self, surface, time):
        (w, h) = surface.get_size()

        spacing_x = w / (self.num_cells_x + 1)
        spacing_y = h / (self.num_cells_y + 1)

        start_x = spacing_x / 2
        start_y = spacing_y / 2

        displacement_vectors_x = []
        displacement_vectors_y = []
        indices = set(self._indices)
        points = set(self._points)
        for (i, (_, w)) in zip(indices, points):
            print(i, len(self.k[0]))
            (displacement_x, displacement_y) = self.system.compute_displacement(
                self.f_b, self.w_b, w,
                [self.k[0][i], self.k[1][i]], time
            )

            displacement_vectors_x.append(displacement_x)
            displacement_vectors_y.append(displacement_y)

        for j in range(self.num_cells_y):
            for i in range(self.num_cells_x):
                displacement_x = sum(vec[i+j*self.num_cells_x] for vec in displacement_vectors_x)
                displacement_y = sum(vec[i+j*self.num_cells_x] for vec in displacement_vectors_y)

                x = int(start_x + spacing_x * i + 2 * displacement_x * spacing_x * self.get_amplitude_factor())
                y = int(start_x + spacing_y * j + 2 * displacement_y * spacing_y * self.get_amplitude_factor())
                r = int((spacing_x + spacing_y) / 6)
                color = self.get_colors()[0]

                print(x, y)

                pygame.gfxdraw.aacircle(surface, x, y, r, color)
                pygame.gfxdraw.filled_circle(surface, x, y, r, color)
