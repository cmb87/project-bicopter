#include <iostream>
#include <cmath>
#include <functional>
#include <thread>
#include <mutex>
#include <ros/ros.h>
#include <std_msgs/Float32.h>
#include <geometry_msgs/PoseStamped.h>
#include <sensor_msgs/JointState.h>
#include <kair_drone/Pose.h>
#include <kair_drone/MotorSpeed.h>
#include <gazebo/gazebo.hh>
#include <gazebo/physics/physics.hh>
#include <gazebo/common/common.hh>
#include <tf/transform_broadcaster.h>


class DronePlugin : public gazebo::ModelPlugin {
public:
  DronePlugin() : gazebo::ModelPlugin() {
    std::cout << "Starting drone_plugin" << std::endl;
  }
  
  virtual ~DronePlugin() {
    std::cout << "Closing drone_plugin" << std::endl;
    delete _nh;
  }

  void Load(gazebo::physics::ModelPtr parent, sdf::ElementPtr sdf) {
    _model = parent;
    
    if (sdf->HasElement("updateRate")) {
      _rate = sdf->GetElement("updateRate")->Get<double>();
    } else {
      _rate = 100.0;
    }
    
    if (sdf->HasElement("publishTf")) {
      _publish_tf = sdf->GetElement("publishTf")->Get<bool>();
    } else {
      _publish_tf = true;
    }
    
    if (sdf->HasElement("rotorThrustCoeff")) {
      _rotor_thrust_coeff = sdf->GetElement("rotorThrustCoeff")->Get<double>();
    } else {
      _rotor_thrust_coeff = 0.00025;
    }
    
    if (sdf->HasElement("rotorTorqueCoeff")) {
      _rotor_torque_coeff = sdf->GetElement("rotorTorqueCoeff")->Get<double>();
    } else {
      _rotor_torque_coeff = 0.0000074;
    }
    
    if (!ros::isInitialized()) {
      int argc = 0;
      char** argv = NULL;
      ros::init(argc, argv, "kair_drone", ros::init_options::NoSigintHandler);
    }
    
    _nh = new ros::NodeHandle("");
    _pose_pub = _nh->advertise<kair_drone::Pose>("pose", 100);
    _cmd_sub = _nh->subscribe("motor_speed_cmd", 100, &DronePlugin::onMotorSpeedsMsg, this);
    _ros_thread = std::thread(std::bind(&DronePlugin::rosThread, this));
    
    _updateConnection = gazebo::event::Events::ConnectWorldUpdateBegin(std::bind(&DronePlugin::onUpdate, this));
  }
  
  void onUpdate() {
    _pose_mtx.lock();
    _pose = _model->GetWorldPose();
    _pose_mtx.unlock();
    
    updateThrust();
  }
  
  void rosThread() {
    ros::Rate rate(_rate);
    while (ros::ok()) {
      ros::spinOnce();
      publishDronePose();
      rate.sleep();
    }
  }
  
  void publishDronePose() {
    _pose_mtx.lock();
    gazebo::math::Pose pose = _pose;
    _pose_mtx.unlock();
    
    gazebo::math::Vector3 rpy = pose.rot.GetAsEuler();
    tf::Quaternion q(pose.rot.x, pose.rot.y, pose.rot.z, pose.rot.w);
    tf::Matrix3x3 m(q);
    double roll, pitch, yaw;
    m.getRPY(roll, pitch, yaw);
    
    kair_drone::Pose pose_msg;
    pose_msg.x = pose.pos.x;
    pose_msg.y = pose.pos.y;
    pose_msg.z = pose.pos.z;
    pose_msg.roll = roll;
    pose_msg.pitch = -pitch;
    pose_msg.yaw = yaw;
    _pose_pub.publish(pose_msg);
    
    if (_publish_tf) {
      tf::Transform T;
      T.setOrigin(tf::Vector3(pose.pos.x, pose.pos.y, pose.pos.z));
      T.setRotation(tf::Quaternion(pose.rot.x, pose.rot.y, pose.rot.z, pose.rot.w));
      _tf.sendTransform(tf::StampedTransform(T, ros::Time::now(), "world", "drone"));
    }
  }
  
  double calculateThrust(double w) {
    double thrust = _rotor_thrust_coeff * w * w;
    return thrust;
  }
  
  double calculateTorque(double w) {
    double torque = copysign(_rotor_torque_coeff * w * w, w);
    return torque;
  }
  
  void updateThrust() {
    _cmd_mtx.lock();
    kair_drone::MotorSpeed cmd = _motor_speed_msg;
    _cmd_mtx.unlock();
    
    int n = cmd.name.size();
    for (int i = 0; i < n; ++i) {
      double thrust = calculateThrust(cmd.velocity[i]);
      double torque = calculateTorque(cmd.velocity[i]);
      //ROS_INFO("torque: %f", torque);
      gazebo::physics::LinkPtr link = _model->GetLink(cmd.name[i]);
      if (link != NULL) {
        link->AddLinkForce(gazebo::math::Vector3(0, 0, thrust));
        link->AddRelativeTorque(gazebo::math::Vector3(0, 0, torque));
      }
    }
  }
  
  void onMotorSpeedsMsg(const kair_drone::MotorSpeed::ConstPtr& msg) {
    _cmd_mtx.lock();
    _motor_speed_msg = *msg;
    _cmd_mtx.unlock();
  }

private:
  ros::NodeHandle* _nh;
  ros::Publisher _pose_pub;
  ros::Subscriber _cmd_sub;
  tf::TransformBroadcaster _tf;
  std::thread _ros_thread;
  std::mutex _pose_mtx;
  std::mutex _cmd_mtx;
  double _rate;
  bool _publish_tf;
  double _rotor_thrust_coeff;
  double _rotor_torque_coeff;
  kair_drone::MotorSpeed _motor_speed_msg;
  
  gazebo::physics::ModelPtr _model;
  gazebo::event::ConnectionPtr _updateConnection;
  gazebo::math::Pose _pose;
};
  
GZ_REGISTER_MODEL_PLUGIN(DronePlugin)
