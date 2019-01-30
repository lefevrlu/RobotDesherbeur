# -*- coding: utf-8 -*-
import Image as IMAGE
import cv2
import rospy
import roslib
import numpy as np
import PIL

from sensor_msgs.msg import CompressedImage
from std_msgs.msg import Float64
from cv_bridge import CvBridge, CvBridgeError

pub = None

def callback(message):
	global image, pub
	print('entrer dans le callback')
	#rospy.loginfo(rospy.get_caller_id() + "I heard %s",message.data)
	#image = np.frombuffer(message.data,dtype=np.uint8).reshape(message.height,message.width,-1)

	np_arr = np.fromstring(message.data,np.uint8)
	image = cv2.imdecode(np_arr,cv2.IMREAD_COLOR)


	x,y,w,h = get_bounding_box(image, True)
	print(x, y, w, h)
	myFloat = Float64()
	myFloat.data = 12
	#pub.publish(myFloat)

def listener():
	global pub
	rospy.init_node('listener', anonymous=True)
	print('initialisation de la node')
	rospy.Subscriber('/main_camera/image_raw/compressed',CompressedImage,callback)
	print('sortie du subscriver')
	#pub = rospy.Publisher("my_topic", Float64)


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
	# get dimensions
	imageHeight, imageWidth, imageChannels = Img.shape
	print(imageWidth)
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
	print('entrer dans le main')
	listener()
	print('sortie du listener')
	rospy.spin()

	# read image from file
	#Img = cv2.imread("cylindre3.jpg")
