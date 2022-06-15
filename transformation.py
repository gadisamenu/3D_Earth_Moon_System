import numpy as np

def translationMatrix(x, y, z):
    return np.array([
        [0.3,0,0,x],
        [0,0.3,0,y],
        [0,0,0.3,z],
        [0,0,0,1]
    ],dtype=np.float32)



def rotationMatrix(angle,axis):
    theta = angle * np.pi / 180.0
    mag = np.sqrt(axis[0]**2 + axis[1]**2 + axis[2]**2)

    ux, uy, uz = (axis[0]/mag, axis[1]/mag, axis[2]/mag)

    cs = np.cos(theta)
    sn = np.sin(theta)
    mat = np.array([
        [cs + ux** 2 * (1 - cs),             ux * uy * (1-cs) - uz * sn,           ux * uz * (1-cs) + uy * sn, 0],
        [uy * ux * (1 - cs) + uz * sn,     cs + uy**2 * (1 - cs),            uy * uz * (1 - cs) - ux * sn, 0],
        [ux * uz * (1 - cs) - uy * sn,    uz * uy * (1 - cs) + ux * sn,      cs + uz**2 * (1 - cs), 0],
        [0, 0, 0, 1]
    ], dtype=np.float)
    return mat