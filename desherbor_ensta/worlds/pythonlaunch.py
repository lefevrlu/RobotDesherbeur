import rospy
from gazebo_msgs.srv import SpawnModel, SpawnModelRequest



f = open("../models/Herbe/model.sdf", "r")
filesdf = f.read()

rospy.init_node("grass_spawner")

gazeboSpawnModel = rospy.ServiceProxy("/gazebo/spawn_sdf_model", SpawnModel)

for i in range(10):
    request = SpawnModelRequest()
    request.model_name = "Grass"+str(i)
    request.model_xml = filesdf
    request.robot_namespace = "Herbe"+str(i)
    request.initial_pose.position.x = 1.0
    request.initial_pose.position.y = 0
    request.initial_pose.position.z = 0
    request.initial_pose.orientation.x = 0
    request.initial_pose.orientation.y = 0
    request.initial_pose.orientation.z = 0
    request.initial_pose.orientation.w = 1.0


#rossrv info SpawnModel

response = gazeboSpawnModel(request)
