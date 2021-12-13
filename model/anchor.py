"""
This model takes one node and anchors (grounds) all its position variables

Input parameters:
    l, w  - anchor length and width (purely for display purposes)
    h - beam height (often specified in process parameters) (purely for display purposes)

Nodes/variables:
    This model takes one node and anchors (grounds) all its position variables (x, y, z, rx, ry, rz)
"""
from process.process import *
from src.node import *
from src.output import *
from src.utils import *
from model import Model
import numpy as np
import matplotlib.pyplot as plt


class Anchor(Model):
    def __init__(self, l, w, layer: Layer):
        """
        Defines a 2D beam object

        :param l: beam length (typically the large dimension, but you do you)
        :param w: beam width (typically the small dimension, but you do you)
        :param layer: process layer
        """
        super().__init__(n=1,
                         output_dynamic=[[]],
                         output_ground=[[Output.x, Output.y, Output.z,
                                         Output.rx, Output.ry, Output.rz]])
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
        pass

    def K(self, R: np.ndarray):
        """
        Generates the generalized spring matrix (dimension n*m x n*m)
        :param R: 3D rotation matrix
        :return: Generalized spring matrix
        """
        pass

    def D(self, R: np.ndarray):
        """
        Generates the generalized damping matrix (dimension n*m x n*m)
        :param R: 3D rotation matrix
        :return: Generalized damping matrix
        """
        pass

    def display(self, q: np.ndarray, R: np.ndarray, fig: plt.Figure):
        """
        Displays the model in the given Matplotlib Figure
        :param q: Full state of the model ([x, y, z, rx, ry, rz] for each node). Dimension n*m.
        :param R: 3D rotation matrix
        :param fig: Matplotlib figure to plot on
        :return: None
        """
        q1 = np.zeros(12)
        # q1[[0, 1, 5, 6, 7, 11]] = q

