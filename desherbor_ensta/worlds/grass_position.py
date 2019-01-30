
import math
import rospy
from std_msgs.msg import Float64, Point

"""
estimation de position d'un herb par rapport au repère global aprés le detecté et calibré de la camera
"""

def callback_distance_herb(message):
	distance_herb = message.data
	return distance_herb

def callback_theta(message):
	theta = message.data
	return theta

def callback_robot(message):
	robot_position = message.data
	return robot_position


def Grass_position():
	rospy.init_node('Grass_position', anonymous=True)

	distance_herb = rospy.Subscriber("DISTANCE", Float64, callback_distance_herb)
	theta = rospy.Subscriber("ORIENTATION", Float64, callback_theta)
	robot_position = rospy.Subscriber("/desherbor_ensta/position", Float64, callback_robot)

	pub = rospy.Publisher("Grass_position", Point,queue_size=10)
	
	x_grass = robot_position[0] + distance_herb*math.cos(theta)
	y_grass = robot_position[1] + distance_herb*math.sin(theta)
	
	print("position estimé d'herb:",x_grass,y_grass)

	position_grass = point
	position_grass.data = Point(x_grass,y_grass,0.0)
	pub.publish(position_grass)
	
	

if __name__ == '__main__':
	print("estimator position")
	Grass_position()
	rospy.spin()
	
