import rospy
import numpy as np
from std_msgs.msg import String, Float64, Quaternion
import math








def callback(data, pub):
    coo = data.data
    x, y, z, th = coo[0], coo[1], coo[2], coo[3]

    



if __name__= '__main__':

    try:
        pub_rtw = rospy.Publisher('/desherbor_ensta/joint_right_top_wheel/command', Float64, queue_size = 2)
        pub_ltw = rospy.Publisher('/desherbor_ensta/joint_left_top_wheel/command', Float64, queue_size = 2)
        pub_rbw = rospy.Publisher('/desherbor_ensta/joint_right_bottom_wheel/command', Float64, queue_size = 2)
        pub_lbw = rospy.Publisher('/desherbor_ensta/joint_left_bottom_wheel/command', Float64, queue_size = 2)

        pub = np.array([pub_rtw, pub_ltw, pub_rbw, pub_lbw])

        while(1):

            if not rospy.is_shutdown():
                ###
                rospy.init_node('control_desherbor')
                rospy.Subscriber('/desherbor_ensta/position', Quaternion, callback, callback_args = pub )
                rospy.spin()

    except ROSInterruptException:
        break
