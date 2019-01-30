#include "gen_position.h"

double angle_min, angle_max, angle_increment, range_min, range_max, cap, angularvelocityZ;
std::vector<float> ranges;
bool firstTimeLidar = true;
bool firstTimeImu = true;
double roll, pitch, yaw;
double pos_x = 0;
double pos_y = 0;

/**
 * This tutorial demonstrates simple receipt of messages over the ROS system.
 */
void callbackLidar(const sensor_msgs::LaserScan::ConstPtr& msgLIDAR)
{
  angle_min = msgLIDAR->angle_min;
  angle_max = msgLIDAR->angle_max;
  angle_increment = msgLIDAR->angle_increment;
  range_min = msgLIDAR->range_min;
  range_max = msgLIDAR->range_max;
  ranges = msgLIDAR->ranges;
  firstTimeLidar = false;
}

void callbackImu(const sensor_msgs::Imu::ConstPtr& msgImu) {
  toEulerAngle(msgImu->orientation);
  firstTimeImu = false;
}


static void toEulerAngle(const geometry_msgs::Quaternion & q)
{
	// roll (x-axis rotation)
	double sinr_cosp = +2.0 * (q.w * q.x + q.y * q.z);
	double cosr_cosp = +1.0 - 2.0 * (q.x * q.x + q.y * q.y);
	roll = atan2(sinr_cosp, cosr_cosp);

	// pitch (y-axis rotation)
	double sinp = +2.0 * (q.w * q.y - q.z * q.x);
	if (fabs(sinp) >= 1)
		pitch = copysign(M_PI / 2, sinp); // use 90 degrees if out of range
	else
		pitch = asin(sinp);

	// yaw (z-axis rotation)
	double siny_cosp = +2.0 * (q.w * q.z + q.x * q.y);
	double cosy_cosp = +1.0 - 2.0 * (q.y * q.y + q.z * q.z);
	yaw = atan2(siny_cosp, cosy_cosp);
}

static double modulo(double cap){
  return fmod(fmod(cap,2*M_PI)+2*M_PI,2*M_PI);
}

static void getPosition(double yaw, std::vector<float> ranges, double * pos_x, double * pos_y){
  double north = modulo(-yaw);
  double east = modulo(M_PI/2 - yaw);
  double south = modulo(M_PI - yaw);
  double west = modulo(3*M_PI/2 - yaw);
  int northInd = int(north / angle_increment);
  int eastInd = int(east / angle_increment);
  int southInd = int(south / angle_increment);
  int westInd = int(west / angle_increment);
  double high = ranges.at(northInd) + ranges.at(southInd);
  double width = ranges.at(eastInd) + ranges.at(westInd);

  *pos_x = ranges.at(southInd) - high/2;
  *pos_y = ranges.at(westInd) - width/2;
}

int main(int argc, char **argv)
{
  ros::init(argc, argv, "gen_position");
  ros::NodeHandle n;

  ros::Subscriber subLidar = n.subscribe("/scan", 1000, callbackLidar);
  ros::Subscriber subImu = n.subscribe("/imu", 1000, callbackImu);
  ros::Rate r(5);
  ros::Publisher chatter_pub = n.advertise<geometry_msgs::Pose2D>("/position", 1000);

  geometry_msgs::Pose2D msg;
    // Main loop.
  while (n.ok()){
    if (!firstTimeImu && !firstTimeLidar){
      getPosition(yaw,ranges,&pos_x, &pos_y);
      msg.x = pos_x;
      msg.y = pos_y;
      msg.theta = yaw;

      chatter_pub.publish(msg);
    }
    r.sleep();
    ros::spinOnce();
  }

  return 0;
}
