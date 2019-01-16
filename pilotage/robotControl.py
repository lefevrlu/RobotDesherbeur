import numpy as np

def f(x,u):
    x = x.flatten()
    u = u.flatten()
    return np.array([[x[3] * np.cos(x[2])],
                     [x[3] * np.sin(x[2])],
                     [u[0]],
                     [u[1]]])
