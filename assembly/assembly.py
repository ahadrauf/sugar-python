from src.node import Node
from model.model import Model
from src.utils import *


class Assembly:
    def __init__(self, n, node_names=()):
        if node_names:
            assert (n == len(node_names))
            assert (len(set(node_names)) == len(node_names))  # assert all node names are unique
        else:
            node_names = (i for i in range(n))
        self.nodes = {node_names[i]: Node(node_names[i]) for i in range(n)}
        self.elements = []  # contains tuples (model, node_names, R)

    def add_model(self, model: Model, node_names, rx=0., ry=0., rz=0.):
        """
        Adds a model to the assembly

        :param model: The model to add (should inherit the Model abstract base class)
        :param nodes: A list of the node names
        :param rx: Rotation about the body x axis (see src.utils.rotation() documentation). Zero for planar designs.
        :param ry: Rotation about the line of nodes axis (see src.utils.rotation() documentation). Zero for planar designs.
        :param rz: Rotation about the inertial z axis (see src.utils.rotation() documentation).
        :return:
        """
        assert (model.n == len(node_names))  # ensures you're specifying enough nodes for the model
        nodes = (self.nodes[name] for name in node_names)
        R = rotation(rx, ry, rz)
        self.elements.append((model, nodes, R))

        # TODO: The below DoF update procedure is likely broken (or at least untested) - FIX!
        for i, node in enumerate(nodes):
            for output in model.output_ground[i]:
                if output not in node.output_ground:
                    node.output_dynamic.remove(output)
                    node.output_ground.append(output)

    def rename_node(self, old_name, new_name):
        """
        Rename the node <old_name> into the node <new_name>

        >>> assem = Assembly(2)
        >>> assem.rename_node(0, "gnd")
        >>> assem.rename_node(1, "tip")

        :param old_name: The old name
        :param new_name: The new name
        :return: None
        """
        assert (old_name in self.nodes.keys())  # old name must be a current node
        assert (new_name not in self.nodes.keys())  # new name can't overlap with an existing node
        node = self.nodes.pop(old_name)
        node.name = new_name
        self.nodes[new_name] = node

    def dof(self):
        """
        Returns the number of free variables in the assembly
        :return: The assembly dof
        """
        return sum([len(node.output_dynamic) for node in self.nodes])

    def assemble_system_mass(self, is_sparse=True):
        pass

    def assemble_system_spring(self, is_sparse=True):
        pass

    def assemble_system_damping(self, is_sparse=True):
        pass

    def assemble_F(self, q, t):
        """
        Assemble the forcing function F

        :param q: The state vector [x; xdot] (xdot can be omitted, in which case it is presumed zero)
        :param t: time
        :return: F: force value
        """
        pass

    def assemble_dFdx(self, q, t, is_sparse=False):
        """
        Assemble the Jacobian dF/dx of the forcing function F

        :param q: The state vector [x; xdot] (xdot can be omitted, in which case it is presumed zero)
        :param t: time
        :param is_sparse: (Optional) Flags whether to use sparse solvers or not. Default is false (don't use sparse solvers).
        :return: dF/dx: Jacobian matrix with respect to x
        """
        pass

    def assemble_dFdxdot(self):
        pass
