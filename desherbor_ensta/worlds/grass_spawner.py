#!/usr/bin/env python

import rospy
from gazebo_msgs.srv import SpawnModel, SpawnModelRequest,DeleteModel
import random
import numpy as np
import std_msgs.msg
from geometry_msgs.msg import Point

rospy.init_node("grass_spawner")

file_path = rospy.get_param("/grass_spawner/chemin")
NbHerbe = rospy.get_param("/grass_spawner/NbHerbe")

f = open(file_path, "r")
strdebase = "<radius>0.2</radius>"

strcolorbase = "<diffuse>0 1 0 1</diffuse>"

filesdf = f.read()

rospy.wait_for_service('/gazebo/spawn_sdf_model')

gazeboSpawnModel = rospy.ServiceProxy("/gazebo/spawn_sdf_model", SpawnModel)

pubHerbe = rospy.Publisher('/Les_Herbes', std_msgs.msg.String)

HerbeX =0
HerbeY =0
HerbeZ =0


Name = []
X=[]
Y=[]
Rayon=[]
HerbesStr = ""

for i in range(NbHerbe):
    x = 10 * random.random() -5
    y = 10 * random.random()- 5
    rayon = 0.06*random.random() + 0.01

    X.append(x)
    Y.append(y)
    Rayon.append(rayon)
    Name.append("Grass"+str(i))

    #Creation aleatoire d'herbe.{value for value in variable}
    strtochange = "<radius>"+str(rayon)+"</radius>"
    filesdf = filesdf.replace(strdebase,strtochange)
    strdebase = strtochange
    request = SpawnModelRequest()
    request.model_name = "Grass"+str(i)
    request.model_xml = filesdf
    request.robot_namespace = "Herbe"+str(i)
    request.initial_pose.position.x = x
    request.initial_pose.position.y = y
    request.initial_pose.position.z = 0.05
    request.initial_pose.orientation.x = 0
    request.initial_pose.orientation.y = 0
    request.initial_pose.orientation.z = 0
    request.initial_pose.orientation.w = 1.0
    response = gazeboSpawnModel(request)

    # Herbe = "Grass"+str(i)+" "+str(x) +" "+str(y)+" "+str(rayon)+" "
    #HerbesStr+=Herbe

#rossrv info SpawnModel
#geometry_msgs/Point

def distance(xherb,yherb,xest,yest):
    return np.sqrt((xherb-xest)**2+(yherb-yest)**2)

def callback(data):
     global HerbeX
     global HerbeY
     global Herbey

     rospy.loginfo("I heard %s",data.x)
     HerbeX = data.x
     HerbeY = data.y
     HerbeZ = data.z


def destroy(data):
    global filesdf
    global strdebase
    global strcolorbase

    global HerbeX
    global HerbeY
    global Herbey
    dist = []

    DistanceMaxSuppression =0.2

    for i in range(NbHerbe):
        dist.append(distance(X[i],Y[i],HerbeX,HerbeY))
    dist_min = min(dist)
    print("distance minimun ="+str(dist_min))
    if dist_min<DistanceMaxSuppression:
        ind_min = dist.index(dist_min)

        #destruction
        rospy.wait_for_service('/gazebo/delete_model')
        gazeboDeleteModel = rospy.ServiceProxy("/gazebo/delete_model", DeleteModel)

        requestDel = "Grass"+str(ind_min)
        gazeboDeleteModel(requestDel)

        #respawn
        #requestRespawn

        strtochange = "<radius>"+str(Rayon[ind_min])+"</radius>"
        filesdf = filesdf.replace(strdebase,strtochange)
        strdebase = strtochange

        strambientochange = "<ambient> 0 0 0 1</ambient>"
        strambiantbefore = "<ambient> 0.3 1 0.3 1</ambient>"

        strcolorchange = "<diffuse>0 0 0 1</diffuse>"
        filesdf = filesdf.replace(strcolorbase,strcolorchange)
        strcolorbase = strcolorchange

        filesdf = filesdf.replace(strambiantbefore,strambientochange)

        requestRespawn = SpawnModelRequest()
        requestRespawn.model_name = "Grass"+str(ind_min)
        requestRespawn.model_xml = filesdf
        requestRespawn.robot_namespace = "Herbe"+str(ind_min)
        requestRespawn.initial_pose.position.x = X[ind_min]
        requestRespawn.initial_pose.position.y = Y[ind_min]
        requestRespawn.initial_pose.position.z = 0
        requestRespawn.initial_pose.orientation.x = 0
        requestRespawn.initial_pose.orientation.y = 0
        requestRespawn.initial_pose.orientation.z = 0
        requestRespawn.initial_pose.orientation.w = 1.0

        gazeboSpawnModel(requestRespawn)
    else :
        print "C'est bien trop loin"

def listener():
    rospy.Subscriber("/HerbePos", Point, callback)

    rospy.Subscriber("/Destroy",std_msgs.msg.Empty, destroy)
     # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

listener()
