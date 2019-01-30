#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
script de controle du robot:
commande proportionnelle par rapport à l'erreur sur l'angle et la distance
"""
# from std_msgs.msg import Int64
# import rospy

# def callback(msg):
#   """
#   renvoie la commande en accélération du robot
#   """
#   value = msg.data
#   print(value)
#   return None

# rospy.init_node("")
# sub = rospy.Subscriber("/topic", Int64, callback)
# pub = rospy.Publisher("/topic", Int64)
# pub.publish(Int64(data=10))





# license removed for brevity
import rospy
from std_msgs.msg import String, Float64, Float64MultiArray
from math import atan2


def orientation_roue_gauche(angle):
    pub = rospy.Publisher('/desherbor_ensta/joint_left_top_wheel/command', Float64, queue_size = 2)
    # rate = rospy.Rate(10)
    if not rospy.is_shutdown():
        rospy.sleep(0.1)
        pub.publish(Float64(data = angle))
        rospy.sleep(0.1)

def orientation_roue_droite(angle):
    pub = rospy.Publisher('/desherbor_ensta/joint_right_top_wheel/command', Float64, queue_size = 2)
    # rate = rospy.Rate(10)
    if not rospy.is_shutdown():
        rospy.sleep(0.1)
        pub.publish(Float64(data = angle))
        rospy.sleep(0.1)

def orientation_roues(angle):
    orientation_roue_gauche(angle)
    orientation_roue_droite(angle)


def change_wheel_speed(value):
    pub1 = rospy.Publisher('/desherbor_ensta/joint_left_bottom_wheel/command', Float64, queue_size = 1)
    pub2 = rospy.Publisher('/desherbor_ensta/joint_right_bottom_wheel/command', Float64, queue_size = 1)
    # rospy.init_node('commande')
    # rate = rospy.Rate(10)
    if not rospy.is_shutdown():
        rospy.sleep(0.1)
        pub1.publish(Float64(data = value))
        pub2.publish(Float64(data = value))


def movement_policy(position,destination):
    """
    publish l'angle et la vitesse pour aller de position vers destination
    """
    x,y = position
    u1,u2 = destination
    eps = 1 # seuil de tolérance en distance

    theta_hat = get_angle(position,destination)
    orientation_roues(theta_hat)
    if (x-u1)**2 + (y-u2)**2 > eps: # si on est trop loin de l'herbe on avance
        change_wheel_speed(1)
    else:
        change_wheel_speed(0)

def tourner_en_rond():
    orientation_roue_gauche(0)
    change_wheel_speed(1)
    orientation_roue_droite(30)


if __name__ == '__main__':
    while(1):
        rospy.init_node('commande')
        tourner_en_rond()
    # rospy.init_node('commande')
    # rospy.Subscriber("/topic", Float64MultiArray, movement_policy)
    #x = (0,0)
    #y = (0,-1)
    #print(atan2(y[1]-x[1],y[0]-x[0]))
    # while(1):
    #     roulement_roue_gauche()
    #     avancer()
    # try:
    # except rospy.ROSInterruptException:
    #     pass
