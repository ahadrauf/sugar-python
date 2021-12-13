import numpy as np


def rotation(rx=0., ry=0., rz=0.):
    """
    Generates the 3D rotation matrix using 3-2-1 Euler angles, i.e., R = Rx(rx)*Ry(ry)*Rz(rz)

    :param rx: Rotation about the body x axis (phi in Euler notation)
    :param ry: Rotation about the line of nodes (new y axis) (theta in Euler notation)
    :param rz: Rotation about the inertial z axis (psi in Euler notation)
    :return: 3D rotation matrix
    """
    return Rx(rx)@Ry(ry)@Rz(rz)


def Rx(phi):
    return np.array([[1, 0, 0],
                     [0, np.cos(phi), np.sin(phi)],
                     [0, -np.sin(phi), np.cos(phi)]])


def Ry(theta):
    return np.array([[np.cos(theta), 0, -np.sin(theta)],
                     [0, 1, 0],
                     [np.sin(theta), 0, np.cos(theta)]])


def Rz(psi):
    return np.array([[np.cos(psi), np.sin(psi), 0],
                     [-np.sin(psi), np.cos(psi), 0],
                     [0, 0, 1]])


def angular_velocity(drx=0., dry=0., drz=0.):
    """
    Computes the angular velocity about the body axes (i.e., the final axes after rotation) using 3-2-1 Euler angles
    Multiply the output matrix by [dphi; dtheta; dpsi] (rate of rotation of Euler angles) to get the vector
        [omega_x; omega_y; omega_z] (rate of rotation about body axes)

    :param drx: Angular velocity about about the body x axis (dphi in Euler notation)
    :param dry: Angular velocity about the line of nodes (new y axis) (dtheta in Euler notation)
    :param drz: Angular velocity about the inertial z axis (dpsi in Euler notation)
    :return: Angular velocity conversion matrix
    """
    return np.array([[1, 0, -np.sin(dry)],
                     [0, np.cos(drx), np.cos(dry)*np.sin(drx)],
                     [0, -np.sin(drx), np.cos(dry)*np.cos(drx)]])
