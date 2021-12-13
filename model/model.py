from abc import ABC, abstractmethod
import numpy as np
import matplotlib.pyplot as plt


class Model(ABC):
    def __init__(self, n, output_dynamic, output_ground):
        """
        Abstract base class for all SUGAR models

        :param nodes: The relevant nodes which define the output state (length n)
        :param output_dynamic: Important state variables for each node. Defined as a 2D array, with rows corresponding
                               to each node (dimension n x m, if all nodes have m state variables)
        :param output_ground: State variables that are grounded (i.e. kept at zero)
        """
        self.output_dynamic = output_dynamic
        self.output_ground = output_ground
        self.n = len(self.nodes)

        # for most models, each node has the same dynamic output types
        # feel free to redefine this variable if each of your nodes has its
        # own output types
        self.m = len(self.output_dynamic[0])

    @abstractmethod
    def M(self, R: np.ndarray):
        """
        Generates the generalized mass matrix (dimension n*m x n*m)
        :param R: 3D rotation matrix
        :return: Generalized mass matrix
        """
        pass

    @abstractmethod
    def K(self, R: np.ndarray):
        """
        Generates the generalized spring matrix (dimension n*m x n*m)
        :param R: 3D rotation matrix
        :return: Generalized spring matrix
        """
        pass

    @abstractmethod
    def D(self, R: np.ndarray):
        """
        Generates the generalized damping matrix (dimension n*m x n*m)
        :param R: 3D rotation matrix
        :return: Generalized damping matrix
        """
        pass

    @abstractmethod
    def display(self, q: np.ndarray, R: np.ndarray, fig: plt.Figure):
        """
        Displays the model in the given Matplotlib Figure
        :param q: Full state of the model ([x, y, z, rx, ry, rz] for each node). Dimension n*m.
        :param R: 3D rotation matrix
        :param fig: Matplotlib figure to plot on
        :return: None
        """
        pass
