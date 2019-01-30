
import math
import rospy
from std_msgs.msg import Float64, Point

"""
estimation de position d'un herb par rapport au repère global aprés le detecté et calibré de la camera
"""

class Grass_position():

	def __init__(self):
		self.distance_herb = 0.0
		self.theta_herb = 0.0
		self.position_robot = (0.0,0.0,0.0,0.0)
		self.pub = rospy.Publisher("Grass_position", Point,queue_size=10)
		rospy.Subscriber("DISTANCE", Float64, self.callback_distance_herb)
		rospy.Subscriber("ORIENTATION", Float64, self.callback_theta)
		rospy.Subscriber("/desherbor_ensta/position", Float64, self.callback_robot)

	def callback_distance_herb(self, message):
		self.distance_herb = message

	def callback_theta(self, message):
		self.theta_herb = message

	def callback_robot(self, message):
		self.robot_position = message

	def get_position():
		x_grass = self.robot_position[0] + self.distance_herb*math.cos(self.theta)
		y_grass = self.robot_position[1] + self.distance_herb*math.sin(self.theta)
		print("position estimé d'herb:",x_grass,y_grass)

		position_grass = Point
		position_grass.data = Point(x_grass,y_grass,0.0)
		self.pub.publish(position_grass)


if __name__ == '__main__':
	rospy.init_node('Grass_position')
	print("estimator grass position")
	Grass = Grass_position()
	r = rospy.Rate(10)
	while not rospy.is_shutdown():
	 	Grass.get_position()
		r.sleep()
	rospy.spin()
