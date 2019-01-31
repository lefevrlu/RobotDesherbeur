#include "ros/ros.h"
#include <sensor_msgs/LaserScan.h>
#include <sensor_msgs/Imu.h>
#include <geometry_msgs/Quaternion.h>
#include <geometry_msgs/Pose2D.h>
#include <vector>
#include <math.h>

static void toEulerAngle(const geometry_msgs::Quaternion & q);

void callbackImu(const sensor_msgs::Imu::ConstPtr& msgImu);

void callbackLidar(const sensor_msgs::LaserScan::ConstPtr& msgLIDAR);

static void getPosition(double yaw, std::vector<float> ranges, double * pos_x, double * pos_y);

static double modulo(double cap);
