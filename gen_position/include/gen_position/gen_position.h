#include "ros/ros.h"
#include <sensor_msgs/LaserScan.h>
#include <sensor_msgs/Imu.h>
#include <geometry_msgs/Quaternion.h>
#include <vector>
#include <math.h> 

void callback(const sensor_msgs::LaserScan::ConstPtr& msgLIDAR, const sensor_msgs::Imu::ConstPtr& msgImu);
