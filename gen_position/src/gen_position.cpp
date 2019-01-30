#include "gen_position.h"

double angle_min, angle_max, angle_increment, range_min, range_max, cap, angularvelocityZ;
std::vector<float> range;
bool firstTimeLidar = true;
bool firstTimeImu = true;

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
  range = msgLIDAR->ranges;
  firstTimeLidar = false;
}

void callbackImu(const sensor_msgs::Imu::ConstPtr& msgImu) {
  cap = msgImu->orientation.w;
  angularvelocityZ = msgImu->angular_velocity.z;
  firstTimeImu = false;
}

int main(int argc, char **argv)
{
  /**
   * The ros::init() function needs to see argc and argv so that it can perform
   * any ROS arguments and name remapping that were provided at the command line.
   * For programmatic remappings you can use a different version of init() which takes
   * remappings directly, but for most command-line programs, passing argc and argv is
   * the easiest way to do it.  The third argument to init() is the name of the node.
   *
   * You must call one of the versions of ros::init() before using any other
   * part of the ROS system.
   */
  ros::init(argc, argv, "gen_position");

  /**
   * NodeHandle is the main access point to communications with the ROS system.
   * The first NodeHandle constructed will fully initialize this node, and the last
   * NodeHandle destructed will close down the node.
   */
  ros::NodeHandle n;

  /**
   * The subscribe() call is how you tell ROS that you want to receive messages
   * on a given topic.  This invokes a call to the ROS
   * master node, which keeps a registry of who is publishing and who
   * is subscribing.  Messages are passed to a callback function, here
   * called chatterCallback.  subscribe() returns a Subscriber object that you
   * must hold on to until you want to unsubscribe.  When all copies of the Subscriber
   * object go out of scope, this callback will automatically be unsubscribed from
   * this topic.
   *
   * The second parameter to the subscribe() function is the size of the message
   * queue.  If messages are arriving faster than they are being processed, this
   * is the number of messages that will be buffered up before beginning to throw
   * away the oldest ones.
   */
  ros::Subscriber subLidar = n.subscribe("/scan", 1000, callbackLidar);

  ros::Subscriber subImu = n.subscribe("/imu", 1000, callbackImu);

  ros::Rate r(5);

    // Main loop.
  while (n.ok()){
    if (!firstTimeLidar) {
      printf("I heard from LIDAR: [%f]\n", range.at(0));
    }
    if (!firstTimeImu) {
      printf("I heard from IMU: [%f]\n", angularvelocityZ);
    }
    ros::spinOnce();
  }

  return 0;
}
