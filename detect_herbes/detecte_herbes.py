# -*- coding: utf-8 -*-
import cv2

def get_bounding_box(img,disp = False):
	"""
	input:
		img: adresse de l'image
		disp: booléen, enregistre une image de l'object détecté si vrai
	output:
		* les coordonées sont dans le repère image usuel *
		x: coordonnée x du coin supérieur gauche de la bounding box (en pixels depuis la bordure gauche de l'image)
		y: coordonnée y du coin supérieur gauche de la bounding box (en pixels depuis la bordure supérieure de l'image)
		w: largeur de la bounding box (en pixels)
		h: hauteur de la bounding box (en pixels)
	"""
	Img = cv2.imread(img)
	# get dimensions
	imageHeight, imageWidth, imageChannels = Img.shape

	# lire image en HSV
	hsv = cv2.cvtColor(Img, cv2.COLOR_BGR2HSV)

	# interval HSV of green
	#(120,100,50)
	greenLow = (40, 40,40) #(36,0,0) 
	greenUp = (70, 255,255) #(86,255,255) 

	#construct a mask
	mask = cv2.inRange(hsv, greenLow, greenUp)

	#Contours
	contours= cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]

	#choisir le contoure a le plus grand surface
	contour = max(contours, key = cv2.contourArea)

	cv2.drawContours(Img, [contour], -1, 255, -1)

	if disp:
		cv2.imwrite('detectee.png',Img)

	M = cv2.moments(contour)
	center  = (M["m10"]/M["m00"],M["m01"]/M["m00"])
	area = cv2.contourArea(contour)

	x, y, w, h = cv2.boundingRect(contour)
	return x, y, w, h

if __name__ == "__main__":

	# read image from file
	Img = cv2.imread("cylindre3.jpg")
	x,y,w,h = get_bounding_box(Img, True)
	print(x, y, w, h)
