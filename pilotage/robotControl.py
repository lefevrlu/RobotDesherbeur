import numpy as np

def f(x,u):
	"""
	input:
		x: [x,y,θ,v] vecteur d'état avec:
			x, y: position
			θ: orientation par rapport au Nord
			v: la vitesse
	output:
	f renvoie dx/dt
	"""
    x = x.flatten()
    u = u.flatten()
    return np.array([[x[3] * np.cos(x[2])],
                     [x[3] * np.sin(x[2])],
                     [u[0]],
                     [u[1]]])