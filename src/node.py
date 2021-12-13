from src.output import Output

class Node:
    def __init__(self, name):
        """
        Create a new node with the given name

        A new node is unconstrained, i.e., all 6 position variables (x, y, z, rx, ry, rz) are free variables in the
        system. As more constraints are added, more position variables become fixed (i.e., they get moved from
        self.output_dynamic to self.output_ground).
        :param name:
        """
        self.name = name
        self.output_dynamic = [Output.x, Output.y, Output.z, Output.rx, Output.ry, Output.rz]
        self.output_ground = []
