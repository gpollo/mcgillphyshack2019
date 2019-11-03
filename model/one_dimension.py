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

            for i in range(self.n):
                if w in w_branches[i]:
                    branch_index = i
                    k_index = np.where(w_branches[i] == w)[0][0]
                else:
                    pass

            phases_diff = phase[branch_index][k_index]
            ampl_rel = ampl[branch_index][k_index]

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

class AbstractOneDimensionalModelWrapper(AbstractModel):
    def __init__(self):
        super(AbstractOneDimensionalModelWrapper, self).__init__()

        self.a = 1
        self.m = 1
        self.k0 = 1

        atom_count     = self.get_atom_count()
        spacing_vector = self.get_spacing_vector()
        delta_r_vector = self.get_delta_r_vector()
        masse_vector   = self.get_mass_vector()
        k_vector       = self.get_k_vector()
        cell_count     = self.get_cell_count()

        self.__system = OneDimensionalModel(
            atom_count,
            spacing_vector,
            delta_r_vector,
            masse_vector,
            k_vector,
            cell_count
        )

        self.w, self.modes = self.__system.compute_all_1ZB()
        self.w_b, self.f_b = self.__system.split_branches(self.w, self.modes)

    def get_name(self):
        raise NotImplementedError

    def get_config_widgets(self):
        return []

    def get_atom_count(self):
        raise NotImplementedError

    def get_spacing_vector(self):
        raise NotImplementedError

    def get_delta_r_vector(self):
        raise NotImplementedError

    def get_mass_vector(self):
        raise NotImplementedError

    def get_k_vector(self):
        raise NotImplementedError

    def get_cell_count(self):
        raise NotImplementedError

    def get_series(self):
        raise NotImplementedError

    def get_x_limits(self):
        return (-np.pi / self.get_r(), np.pi / self.get_r())

    def get_x_ticks(self):
        return [
            -np.pi / self.get_r(),
            0,
            np.pi / self.get_r(),
        ]

    def get_x_ticklabels(self):
        return [
            r"$-\displaystyle\frac{\pi}{r}$",
            r"$0$",
            r"$\displaystyle\frac{\pi}{r}$"
        ]

    def get_vertical_lines(self):
        return []

    def get_system(self):
        return self.__system

    def get_r(self):
        return self.get_system().r

    def draw(self, surface, time):
        (w, h) = surface.get_size()

        spacing = w / (self.get_cell_count() + 1)
        start = spacing / 2
        middle = h / 2

        vectors = []
        points = set(self._points)
        for (x, y) in points:
            vectors.append(self.__system.compute_displacement(
                self.f_b,
                self.w_b,
                y, x, time
            ))

        largest_atom = max(self.get_mass_vector())
        for i in range(self.get_cell_count()):
            atom = i % len(self.get_mass_vector())
            displacement = sum(vector[i] for vector in vectors)

            x = int(start + spacing * i + 2 * displacement * spacing * self.get_amplitude_factor())
            y = int(middle)
            r = int((spacing/4) * min(1, (self.get_mass_vector()[atom] / largest_atom) * 1.8))
            c = int(0)

            color = self.get_colors()[atom]
            pygame.gfxdraw.aacircle(surface, x, y, r, color)
            pygame.gfxdraw.filled_circle(surface, x, y, r, color)

from PyQt5.QtWidgets import QLabel, QSlider
class OneDimensionalModelWrapper(AbstractOneDimensionalModelWrapper):
    def __init__(self):
        super(OneDimensionalModelWrapper, self).__init__(self)

        self.__atom_count        = 1
        self.__atom_count_label  = QLabel("Atom Count")
        self.__atom_count_slider = QSlider()
        self.__atom_count_slider.setMinimum(1)
        self.__atom_count_slider.setMaximum(5)
        self.__cell_count        = 20
        self.__cell_count_label  = QLabel("Cell Count")
        self.__cell_count_slider = QSlider()
        self.__cell_count_slider.setMinimum(1)
        self.__cell_count_slider.setMaximum(30)

        #self.__atom_count_slider.valueChanged.connect(

    def atom_count_changed(self, value):
        self.__atom_count = value

    def cell_count_changed(self, value):
        self.__cell_count = value

    def get_name(self):
        return "One Dimensional (Custom)"

    def get_config_widgets(self):
        return [
            self.__atom_count_label,
            self.__atom_count_slider,
            self.__cell_count_label,
            self.__cell_count_slider,
        ]

    def get_atom_count(self):
        return self.__atom_count

    def get_spacing_vector(self):
        return [self.a] * (self.__atom_count + 1)

    def get_delta_r_vector(self):
        atom_count = self.get_atom_count()
        if self.get_atom_count() % 2 == 0:
            step = (2*self.a)/(atom_count+1)
        else:
            step = (2*self.a)/(atom_count-1) if atom_count != 1 else 0
        return [0] # TODO

    def get_mass_vector(self):
        return [self.m] * (self.__atom_count)

    def get_k_vector(self):
        return [self.k0] * (self.__atom_count + 1)

    def get_cell_count(self):
        return self.__cell_count

    def get_series(self):
        return [
            (self.get_system().k_vec, self.w_b[i])
            for i in range(self.__atom_count)
        ]

class OneDimensionalModelWrapper1(AbstractOneDimensionalModelWrapper):
    def get_name(self):
        return "One Dimensional 1"

    def get_atom_count(self):
        return 1

    def get_spacing_vector(self):
        return [self.a, self.a]

    def get_delta_r_vector(self):
        return [0]

    def get_mass_vector(self):
        return [self.m]

    def get_k_vector(self):
        return [self.k0, self.k0]

    def get_cell_count(self):
        return 21

    def get_series(self):
        return [
            (self.get_system().k_vec, self.w_b[0])
        ]

class OneDimensionalModelWrapper2(AbstractOneDimensionalModelWrapper):
    def get_name(self):
        return "One Dimensional 2"

    def get_atom_count(self):
        return 2

    def get_spacing_vector(self):
        return [self.a, self.a, self.a]

    def get_delta_r_vector(self):
        return [-self.a/2, self.a/2]

    def get_mass_vector(self):
        return [self.m, 2 * self.m]

    def get_k_vector(self):
        return [self.k0, self.k0, self.k0]

    def get_cell_count(self):
        return 21

    def get_series(self):
        return [
            (self.get_system().k_vec, self.w_b[0]),
            (self.get_system().k_vec, self.w_b[1])
        ]

class OneDimensionalModelWrapper3(AbstractOneDimensionalModelWrapper):
    def get_name(self):
        return "One Dimensional 3"

    def get_atom_count(self):
        return 3

    def get_spacing_vector(self):
        return [self.a, self.a, self.a, self.a]

    def get_delta_r_vector(self):
        return [-self.a, 0, self.a]

    def get_mass_vector(self):
        return [self.m, 2 * self.m, 3 * self.m]

    def get_k_vector(self):
        return [self.k0, self.k0, self.k0, self.k0]

    def get_cell_count(self):
        return 21

    def get_series(self):
        return [
            (self.get_system().k_vec, self.w_b[0]),
            (self.get_system().k_vec, self.w_b[1]),
            (self.get_system().k_vec, self.w_b[2])
        ]
