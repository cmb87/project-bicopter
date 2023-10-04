import rclpy
from rclpy.node import Node

from std_msgs.msg import String, Float32
from geometry_msgs.msg import Wrench, Vector3
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from sensor_msgs.msg import Joy


class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('propeller')


        # Parameters
        self.declare_parameter("jointsTopic", '/set_joint_trajectory')
        self.declare_parameter("engineRTopic",'/cmd/prop_right')
        self.declare_parameter("engineLTopic",'/cmd/prop_left')
        self.declare_parameter("cmdTopic",'/joy')


        subtopic = self.get_parameter('cmdTopic').value

        pubJoints = self.get_parameter('jointsTopic').value
        pubEngineRight = self.get_parameter('engineRTopic').value
        pubEngineLeft  = self.get_parameter('engineLTopic').value
        

        self.publisherJoints = self.create_publisher(JointTrajectory, pubJoints, 10)
        self.publisherEngineR = self.create_publisher(Float32, pubEngineRight, 10)
        self.publisherEngineL = self.create_publisher(Float32 , pubEngineLeft, 10)

        self.subscription = self.create_subscription(
            Joy,
            subtopic,
            self.listener_callback,
            10
        )

        self.subscription # prevent unused variable warning
        self.get_logger().info(f'Controller Online!')

    def listener_callback(self, msg):

        now = self.get_clock().now()

        [r,p,t,y,_] = msg.axes

        throttle = 5.0*(t+1.0)/2.0


        engineR = throttle - 1.0*r
        engineL = throttle + 1.0*r

        jointR = 0.5*p - y
        jointL = 0.5*p + y

        points = JointTrajectoryPoint()
        points.positions = [jointR, jointL]

        jointMsg = JointTrajectory()
        jointMsg.header.stamp = now.to_msg()
        jointMsg.header.frame_id = "world"
        jointMsg.joint_names = ["arm_right__motor_right", "arm_left__motor_left"]
        jointMsg.points = [points]

        engineRMsg = Float32()
        engineRMsg.data = engineR
        engineLMsg = Float32()
        engineLMsg.data = engineL


        self.publisherEngineR.publish(engineRMsg)
        self.publisherEngineL.publish(engineLMsg)
        self.publisherJoints.publish(jointMsg)


def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()

    rclpy.spin(minimal_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()