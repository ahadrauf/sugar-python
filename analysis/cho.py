from assembly.assembly import Assembly
import numpy as np
import scipy.linalg as sp
import scipy.sparse.linalg as sps


def cho_dc(assem: Assembly, q0=None, t=0, is_sparse=True):
    """
    Do a simple Newton-Raphson iteration to find an equilibrium point Kq = F(q).
    The iteration will stop after forty steps, or after the step sizes decrease to a size less than 1e-9.

    :param assem: The assembly to analyze
    :param q0: (Optional) Starting guess of equilibrium position. If q0 is not provided, the search will start at q0=0.
    :param t: (Optional) Time (defaults to zero for DC solvers).
    :param is_sparse: (Optional) Flags whether to use sparse solvers or not. Default is true (use sparse solvers).
    :return: q: The estimated equilibrium state
             converged: True if the convergence test passed
    """
    if q0 is None:
        q0 = np.zeros((assem.dof(), 1))
    q = q0
    itr = 0

    K = assem.assemble_system_spring(is_sparse)
    G = K@q - assem.assemble_F(q, t)
    dG = K - assem.assemble_dFdx(q, t, is_sparse)
    if is_sparse:
        delta_q = sps.spsolve(dG, G)
    else:
        delta_q = sp.solve(dG, G)
    itr += 1

    while sp.norm(delta_q) >= 1e-6 and itr < 100:
        q = q - delta_q
        G = K@q - assem.assemble_F(q, t)
        dG = K - assem.assemble_dFdx(q, t, is_sparse)
        if is_sparse:
            delta_q = sps.spsolve(dG, G)
        else:
            delta_q = sp.solve(dG, G)
        itr += 1
    q = q - delta_q

    converged = sp.norm(delta_q) < 1e-6
    if itr == 100:
        print('Warning: DC solution finder did not converge after 100 iterations')
    return q, converged
