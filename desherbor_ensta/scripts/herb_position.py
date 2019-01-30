#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import cv2
import rospy
import roslib
import numpy as np

from sensor_msgs.msg import CompressedImage
from std_msgs.msg import Float64

pub, pub2 = None, None

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
	# Img = cv2.imread(img)
	Img = img
	# get dimensionsImg
	imageHeight, imageWidth, imageChannels = Img.shape
	# lire image en HSV
	hsv = cv2.cvtColor(Img, cv2.COLOR_BGR2HSV)

	# interval HSV of green
	#(120,100,50)
	greenLow = (10, 10, 10) #(36,0,0)
	greenUp = (70, 255,255) #(86,255,255)

	#construct a mask
	mask = cv2.inRange(hsv, greenLow, greenUp)

	#Contours
	contours= cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]

	#choisir le contoure a le plus grand surface
	if len(contours)!=0 :
		# rospy.loginfo("Herbe détectée")

		contour = max(contours, key = cv2.contourArea)

		cv2.drawContours(Img, [contour], -1, 255, -1)

		# if disp:
		dirPath = os.path.dirname(__file__)
		cv2.imwrite(os.path.join(dirPath,'detectee.png'),Img)
		cv2.imshow('camera',Img)
		cv2.waitKey(1)

		M = cv2.moments(contour)
		# center  = (M["m10"]/M["m00"],M["m01"]/M["m00"])
		# area = cv2.contourArea(contour)

		x, y, w, h = cv2.boundingRect(contour)
	else :
		x,y,w,h =0,0,0,0
	return x, y, w, h

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

def get_angle(xc,npx,a = 90, b = 0):
	"""
	input:
		xc: coordonnée x du centre de l'herbe
		npx: nombre de pixels de l'image selon l'axe x
		a, b: coefficients dans le modèle linéaire
	output:
		θ: angle par rapport au centre de l'image
	"""
	theta = a*(xc-npx/2)/npx + b # angle en coordonnées polaire dans le repère du robot
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
		r: distance s	input:
éparant l'herbe du robot
	"""
	r = h/c
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
	_,npx,_ = img.shape
	#_,npx,_ = (cv2.imread(img)).shape
	x,y,w,h = get_bounding_box(img)
	xc,yc = get_central_point(x,y,w,h)
	theta = get_angle(xc,npx)
	r = get_radius(w,h)
	return r,theta

def callback(message):
	global image, pub,pub2
	print('entrer dans le callback')
	#rospy.loginfo(rospy.get_caller_id() + "I heard %s",message.data)
	#image = np.frombuffer(message.data,dtype=np.uint8).reshape(message.height,message.width,-1)

	np_arr = np.fromstring(message.data,np.uint8)
	image = cv2.imdecode(np_arr,cv2.IMREAD_COLOR)

	x,y,w,h = get_bounding_box(image, True)
	r,theta = get_position(image)
	print(r,theta)

	mydistance = Float64
	mydistance.data = r
	pub.publish(mydistance)

	myorientation = Float64
	myorientation.data = theta
	pub2.publish(myorientation)

def listener():
	global pub,pub2
	print("entrée listener")
	rospy.init_node('listener', anonymous=True)
	rospy.Subscriber('/main_camera/image_raw/compressed',CompressedImage,callback)
	pub = rospy.Publisher("DISTANCE", Float64,queue_size=10)
	print("pub publiée")
	pub2 = rospy.Publisher("ORIENTATION", Float64,queue_size=10)
	print("pub2 publiée")
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
	print("entrée dans le main")
	listener()
	rospy.spin()
