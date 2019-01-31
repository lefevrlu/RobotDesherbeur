#!/usr/bin/env python

import math
import rospy
from std_msgs.msg import Float64
from geometry_msgs.msg import Point, Pose2D


"""
estimation de position d'un herb par rapport au repere global apres le detecte et calibre de la camera
"""


class Grass_position():

	def __init__(self):
		self.distance_herb = 0.0
		self.theta_herb = 0.0
		self.position_robot = Pose2D()
		self.pub = rospy.Publisher("Grass_position", Point,queue_size=10)
		rospy.Subscriber("DISTANCE", Float64, self.callback_distance_herb)
		rospy.Subscriber("ORIENTATION", Float64, self.callback_theta)
		rospy.Subscriber("/position", Pose2D, self.callback_robot)

	def callback_distance_herb(self, message):
		self.distance_herb = message.data

	def callback_theta(self, message):
		self.theta_herb = message.data

	def callback_robot(self, message):
		self.position_robot = message

	def get_position(self):
		print(type(self.position_robot.theta),type(self.theta_herb),type(self.position_robot.x))
		x_grass = self.position_robot.x + self.distance_herb*math.cos(self.position_robot.theta + self.theta_herb)
		y_grass = self.position_robot.y + self.distance_herb*math.sin(self.position_robot.theta + self.theta_herb)
		print("position estime d'herb:",x_grass,y_grass)

		position_grass = Point
		position_grass.data = Point(x_grass,y_grass,0.0)
		self.pub.publish(position_grass)


if __name__== '__main__':
	rospy.init_node("grass_position")
	print("estimator grass position")
	Grass = Grass_position()
	r = rospy.Rate(10)
	while not rospy.is_shutdown():
	 	Grass.get_position()
		r.sleep()
	rospy.spin()
