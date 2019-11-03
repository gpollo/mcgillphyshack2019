#!/usr/bin/env python
# -*- coding: utf-8 -*-

###########################
#   1) Import libraries   #
###########################
import numpy as np
import cmath


class OneDimensionalModel(object):

    def __init__(self,n,spacing_vec,delta_r_vec,mass_vec,k_vec,num_cells): #spacing_vec et k_vec |k0--o--k1--o--k2--o--..--kn|
        self.n = n
        self.spacing_vec = spacing_vec
        self.r = sum(spacing_vec[0:-1])
        self.delta_r_vec = delta_r_vec
        self.mass_vec = mass_vec
        self.k_vec = k_vec
        self.num_cells = num_cells
        self.num_atoms = n * num_cells

        self.position_vec = np.array([ l*self.r+delta_r_vec[i]  for l in range(num_cells) for i in range(n) ])


        ##############################
        # Compute the Rigidity matrix
        K = np.zeros((n,3*n))

        # i) Interaction with neighbors
        for index_primitive_cell in range(n):
            K[index_primitive_cell,n+index_primitive_cell-1] = -k_vec[index_primitive_cell]
            K[index_primitive_cell,n+index_primitive_cell+1] = -k_vec[index_primitive_cell+1]

        # ii) Self-interaction (acoustic sum rule)
        for index_primitive_cell in range(n):
            K[index_primitive_cell, n+index_primitive_cell] = -sum(K[index_primitive_cell,:])

        #Save K
        self.K_matrix = K

        #############################################
        # Compute vectors in the first Brillouin zone
        index = np.linspace(-int(num_cells/2), int(num_cells/2), num_cells)
        self.k_vec = np.array([2*np.pi*i/(num_cells*self.r) for i in index])


    def _compute_eigenfrequencies(self,k):
        eigenfreqs = np.zeros(self.n)
        eigenmodes = [[] for i in range(self.n)]

        #Compute dynamical matrix
        D = np.zeros((self.n,self.n), dtype=np.complex128)
        for i in range(self.n):
            for j in range(self.n):
                #loop on the 2 neighbooring cells and the cell itself
                for index,l in enumerate((-1,0,1)):
                    D[i,j] = D[i,j] + self.K_matrix[i,index*self.n+j]*np.exp(complex(0,1)*k*l*self.r)

                D[i,j] = 1/np.sqrt(self.mass_vec[i]*self.mass_vec[j]) * D[i,j]


        #Compute eigenvalues and eigenmodes
        w, v = np.linalg.eig(D)

        w = np.sort(w)

        for i in range(self.n):
            eigenfreqs[i] = np.sqrt(w[i].real)
            eigenmodes[i] = v[i]

        return eigenfreqs, eigenmodes


    def compute_all_1ZB(self):
        w = [np.array([]) for i in range(self.num_cells)]
        modes = [np.array([]) for i in range(self.num_cells)]

        for i,k in enumerate(self.k_vec):
            w[i],modes[i] = self._compute_eigenfrequencies(k)

        return w,modes


    def split_branches(self,w,modes):
        w_branches = [np.array([]) for i in range(self.n)]
        f_branches = [np.array([]) for i in range(self.n)]
        for i in range(self.n):
            w_branches[i] = np.array([ f[i] for f in w ])
            f_branches[i] = np.array([ f[i] for f in modes ])
        return w_branches, np.array(f_branches)


    def compute_amplitude_and_phase(self,modes):
        phase_func = np.vectorize(cmath.phase)

        phase = phase_func(modes)
        ampl = np.abs(modes)

        return phase, ampl


    def compute_displacement(self,modes,w_branches,w,k,t):
        if self.n !=1:
            phase,ampl = self.compute_amplitude_and_phase(modes)
            print(phase)
            print(ampl)
            print(w)
            print(k)

            for i in range(self.n):
                if w in w_branches[i]:
                    branch_index = i
                    k_index = np.where(w_branches[i] == w)[0][0]
                else:
                    pass

            print(phase[branch_index])
            print(ampl[branch_index])
            phases_diff = phase[branch_index][0][0][k_index]
            ampl_rel = ampl[branch_index][0][0][k_index]

            #
            phase = np.array([j*i for j in np.ones(self.num_cells) for i in phases_diff])
            amplitude = np.array([j*i for j in np.ones(self.num_cells) for i in ampl_rel])

            #
            displacement = amplitude * np.sin( k*self.position_vec - w*t*np.ones(self.num_atoms) + phase )

        else:
            displacement = 0.1* np.sin( k*self.position_vec - w*t*np.ones(self.num_atoms) )

        return displacement

from model.abstract import AbstractModel
import pygame
import pygame.gfxdraw
class OneDimensionalModelWrapper(AbstractModel):
    def __init__(self):
        super(OneDimensionalModelWrapper, self).__init__()

        n = 1
        a = 1
        m = 1
        k0 = 1

        spacing_vec = [a,a]
        delta_r_vec = [0]
        masse_vec = [m]
        k_vec = [k0,k0]
        self.__num_cells = 21

        self.__system = OneDimensionalModel(
            n,
            spacing_vec,
            delta_r_vec,
            masse_vec,
            k_vec,
            self.__num_cells
        )
        w,self.__modes = self.__system.compute_all_1ZB()

        self.__w_b, self.__f_b = self.__system.split_branches(w, self.__modes)

    def get_name(self):
        return "One Dimensional"

    def get_series(self):
        return [(self.__system.k_vec, self.__w_b[0])]

    def draw(self, surface, time):
        (w, h) = surface.get_size()

        spacing = w / (self.__num_cells + 1)
        start = spacing / 2
        middle = h / 2

        vecs = []
        points = set(self._points)
        for (x, y) in points:
            vecs.append(self.__system.compute_displacement(
                self.__modes,
                self.__w_b,
                y, x, time
            ))

        for i in range(self.__num_cells):
            displacement = sum(vec[i] for vec in vecs)

            x = int(start + spacing * i + 2 * displacement * spacing)
            y = int(middle)
            r = int(spacing/4)
            c = int(0)
            color = (127, 142, 201)

            pygame.gfxdraw.aacircle(surface, x, y, r, color)
            pygame.gfxdraw.filled_circle(surface, x, y, r, color)
