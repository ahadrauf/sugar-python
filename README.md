# SUGAR (Python Port)

This is a Python port of the SUGAR platform for MEMS simulation

## What is SUGAR?
	
SUGAR is a simulation tool for MEMS devices based on nodal analysis techniques from the world of integrated circuit simulation. Beams, electrostatic gaps, circuit elements, etc. are modeled by small, coupled systems of differential equations.

In less than a decade, the MEMS community has leveraged nearly all the integrated-circuit community's fabrication techniques, but little of the wealth of simulation capabilities. A wide range of student and professional circuit designers regularly use circuit simulation tools like SPICE, while MEMS designers often resort to back-of-the-envelope calculations. For three decades, development of IC CAD tools has gone hand-in-hand with the development of IC processes. Tools for simulation will play a similar role in future advances in the design of complicated micro-electromechanical systems.

SUGAR inherits its name and philosophy from SPICE. A MEMS designer can describe a device in a compact netlist format, and very quickly simulate the device's behavior. Using simple simulations in SUGAR, a designer can quickly find problems in a design or try out new ideas. Later in the design process, a designer might run more detailed simulations to check for subtle second-order effects; early in the design, a quick approximate solution is key. SUGAR provides that quick solution.

For more information about the original SUGAR project, see https://www-bsac.eecs.berkeley.edu/cadtools/sugar/.

## Reading This Repository

Although this repository tries to be a direct translation of the original SUGAR repo in many cases, it also makes
several adjustments to how models are loaded. It also makes a clearer distinction between models and assemblies 
(originally just put in a folder called MATLAB). _Models_ are individual components with their own mass, spring, and 
damping matrices - they form the building blocks of all MEMS structures. _Assemblies_ are collections of models that specify
the relative position, orientation, and nodal attachments between the models. Analysis is done on assemblies.

In particular, the folder structure of this repository is:

1) ``analysis/`` - This folder contains all the primary analysis tools, corresponding to the ``analysis/`` folder in 
the original repo.
   
2) ``assembly/`` - This folder contains all MEMS assemblies.
    1) ``assembly/assembly.py`` - This file (and the Assembly class inside) forms the core of all assembly objects. 
    Instantiate an Assembly object with the number of nodes you want, rename the nodes if you so desire for readability,
       and add models using the nodes to establish connections.
   
3) ``model/`` - This folder contains all MEMS models
    1) ``model/model.py`` - This file (and the abstract Model class inside) forms the core of all model objects. 
    All core model objects should inherit this base class, which establishes the basic structure expected by all 
       assemblies (and thus all analysis). It defines several base functions for the mass, spring, and damping
       matrices of each model. The spring matrices are essential for all analysis, while the mass and damping matrices 
       are only necessary for transient analysis.
       
4) ``process/`` - This folder contains all processes
    1) ``process/process.py`` - This file (and the Process and Layer classes inside) form the core for defining
    custom processes. It defines several important mechanical properties for your fabrication stack, and any custom
       parameters can be input just by specifying the name using the **kwargs argument.
       
5) ``src/`` - This folder contains helper classes and functions

## Acknowledgements

Credit to the original SUGAR creators, a wonderful group of PhD students and professors from the early 2000s, including
David Bindel, Jason V. Clark, David Garmire, Professor Kristofer S.J. Pister, and many more. Many thanks to Jason V. 
Clark and Professor Pister for their advice regarding SUGAR functionality.

This particular Python port was begun by Ahad Rauf in 2020, although it was never brought to functionality.