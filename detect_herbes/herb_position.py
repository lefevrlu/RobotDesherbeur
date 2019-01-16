# -*- coding: utf-8 -*-

from detecte_herbes import get_bounding_box
import cv2

def get_central_point(x,y,w,h):
	"""
	input:
		x, y, w, h: comme donnés par get_bounding_box
	output:
		xc, yc: les coordonnées du point central
	"""
	xc = x + w//2
	yc = y + h//2
	return xc, yc

def get_angle(xc,npx,a = 1, b = 0):
	"""
	input:
		xc: coordonnée x du centre de l'herbe
		npx: nombre de pixels de l'image selon l'axe x
		a, b: coefficients dans le modèle linéaire
	output:
		θ: angle par rapport au centre de l'image
	"""
	theta = a*(xc-npx/2) + b # angle en coordonnées polaire dans le repère du robot
	return theta

def get_radius(w,h,c=1):
	"""
	calcule la distance de l'herbe au robot
	fonction linéaire de la surface de la bounding box
	r = S/c
	input:
		w,h: largeur et hauteur de la bounding box
		c: une constante
	output:
		r: distance séparant l'herbe du robot
	"""
	r = w*h/c
	return r

def get_position(img):
	"""
	prend une image en entrée et renvoie l'angle et le rayon de l'herbe par rapport au robot
	repère centré sur le robot, en coordonnées polaires
	input:
		img: adresse de l'image
	output:
		r, θ: rayon et angle
	"""
	_,npx,_ = (cv2.imread(img)).shape
	x,y,w,h = get_bounding_box(img)
	xc,yc = get_central_point(x,y,w,h)
	theta = get_angle(xc,npx)
	r = get_radius(w,h)
	return r,theta

# p1 = (330,70)
# p2 = (611,866)

# x1, y1 = p1
# x2, y2 = p2

# npx = 960 # nombre de pixels sur l'axe x
# npy = 600 # nombre de pixels sur l'axe y

# h = abs(y2 - y1) # hauteur du cylindre
# r*h+br # rayon en coordonnées polaire dans le repère du robot

# ### Calcul de l'angle ###
# aa = 1 # coeff proportionel pour l'angle
# ba = 0 # biais linéraire pour l'angle
# theta = aa*(x1+(x2-x1)/2-npx/2) + ba # angle en coordonnées polaire dans le repère du robot
# print(r,theta)

if __name__ == "__main__":
	img = "cylindre3.jpg"
	# 
	x,y,w,h = get_bounding_box(img, False)
	print(x, y, w, h)
	r,theta = get_position(img)
	print(r,theta)
