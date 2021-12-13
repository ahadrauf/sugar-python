"""
2D small-deflection linear beam model
Source work: N. Zhou, J. V. Clark, and K. S. J. Pister, “Nodal Analysis for MEMS Design Using SUGARv0.5,” Santa Clara CA April, pp. 6–8, 1998.
Source link: http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.126.5104&rep=rep1&type=pdf

Input parameters:
    l, w  - beam length and width
    h - beam height (often specified in process parameters)
    density, fluid, viscosity, Youngmodulus - material parameters specified as part of the process info

Nodes/variables:
    The two end nodes are conceptually in the middle of the two
    w-by-h end faces, which are l units apart.  Each node has
    the usual spatial displacement variables (x, y, rz)
"""
from process.process import *
from src.node import *
from src.output import *
from src.utils import *
from model import Model
import numpy as np
import matplotlib.pyplot as plt


class Beam2D(Model):
    def __init__(self, l, w, layer: Layer):
        """
        Defines a 2D beam object

        :param l: beam length (typically the large dimension, but you do you)
        :param w: beam width (typically the small dimension, but you do you)
        :param layer: process layer
        """
        super().__init__(n=2,  # node 0 = one end of the beam, node 1 = the other end of the beam
                         output_dynamic=[[Output.x, Output.y, Output.rz],
                                         [Output.x, Output.y, Output.rz]],
                         output_ground=[[Output.z, Output.rx, Output.ry],
                                        [Output.z, Output.rx, Output.ry]])
        self.l = l
        self.w = w
        self.h = layer.h

        self.layer = layer

    def M(self, R: np.ndarray):
        """
        Generates the generalized mass matrix (dimension n*m x n*m)
        :param R: 3D rotation matrix
        :return: Generalized mass matrix
        """
        rho = self.layer.rho
        l = self.l
        A = self.w*self.h

        # Convert rotation matrix to 2D
        R = R.copy()
        R[-1, :] = 0
        R[:, -1] = 0
        R[2, 2] = 1

        M11 = R@np.array([[140, 0, 0],
                          [0, 156, 22*l],
                          [0, 22*l, 4*l*l]])@R.T
        M12 = R@np.array([[70, 0, 0],
                          [0, 54, -13*l],
                          [0, 13*l, -3*l*l]])@R.T
        M22 = R@np.array([[140, 0, 0],
                          [0, 156, -22*l],
                          [0, -22*l, 4*l*l]])@R.T
        a1 = rho*A*l/420
        return a1*np.vstack([np.hstack([M11, M12]), np.hstack([M12.T, M22])])

    def K(self, R: np.ndarray):
        """
        Generates the generalized spring matrix (dimension n*m x n*m)
        :param R: 3D rotation matrix
        :return: Generalized spring matrix
        """
        E = self.layer.E
        l = self.l
        w = self.w
        h = self.h

        A = w*h
        I = w**3*h/12
        c = E*I/l**3

        # Convert rotation matrix to 2D
        R = R.copy()
        R[-1, :] = 0
        R[:, -1] = 0
        R[2, 2] = 1

        K11 = R@np.array([[E*A/l, 0, 0],
                          [0, 12*c, 6*c*l],
                          [0, 6*c*l, 4*c*l*l]])@R.T
        K12 = R@np.array([[-E*A/l, 0, 0],
                          [0, -12*c, 6*c*l],
                          [0, -6*c*l, 2*c*l*l]])@R.T
        K22 = R@np.array([[E*A/l, 0, 0],
                          [0, 12*c, -6*c*l],
                          [0, -6*c*l, 4*c*l*l]])@R.T
        return np.vstack([np.hstack([K11, K12]), np.hstack([K12.T, K22])])

    def D(self, R: np.ndarray):
        """
        Generates the generalized damping matrix (dimension n*m x n*m)
        :param R: 3D rotation matrix
        :return: Generalized damping matrix
        """
        l = self.l
        w = self.w
        mu = self.layer.mu
        fluid_gap = self.layer.fluid_gap

        # Convert rotation matrix to 2D
        R = R.copy()
        R[-1, :] = 0
        R[:, -1] = 0
        R[2, 2] = 1

        D11 = R@np.array([[140, 0, 0],
                          [0, 156, 22*l],
                          [0, 22*l, 4*l*l]])@R.T
        D12 = R@np.array([[70, 0, 0],
                          [0, 54, -13*l],
                          [0, 13*l, -3*l*l]])@R.T
        D22 = R@np.array([[140, 0, 0],
                          [0, 156, -22*l],
                          [0, -22*l, 4*l*l]])@R.T
        a1 = mu*l*w/(420*fluid_gap)
        return a1*np.vstack([np.hstack([D11, D12]), np.hstack([D12.T, D22])])

    def display(self, q: np.ndarray, R: np.ndarray, fig: plt.Figure):
        """
        Displays the model in the given Matplotlib Figure
        :param q: Full state of the model ([x, y, z, rx, ry, rz] for each node). Dimension n*m.
        :param R: 3D rotation matrix
        :param fig: Matplotlib figure to plot on
        :return: None
        """
        q1 = np.zeros(12)
        q1[[0, 1, 5, 6, 7, 11]] = q

