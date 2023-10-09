import rclpy
from rclpy.node import Node

from std_msgs.msg import String, Float32
from geometry_msgs.msg import Wrench, Vector3



class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')


        # Parameters
        self.publisherArmLeft  = self.create_publisher(Wrench, '/force/prop_left', 10)
        self.publisherArmRight = self.create_publisher(Wrench, '/force/prop_right', 10)

        self.subscriptionCmdLeft = self.create_subscription(
            Float32,
            '/cmd/prop_left',
            self.listener_callback_left,
            10
        )

        self.subscriptionCmdRight = self.create_subscription(
            Float32,
            '/cmd/prop_right',
            self.listener_callback_right,
            10
        )

        self.subscriptionCmdLeft  # prevent unused variable warning
        self.subscriptionCmdRight  # prevent unused variable warning
        self.get_logger().info('Propeller Online!')
        # ros2 topic pub -1 /cmd/prop_left  std_msgs/Float32 '{data: 3.0}'


    def listener_callback_right(self, msg):

        self.get_logger().info('Publishing Right Prop: "%s"' % msg.data)

        force = Vector3()
        force.x = 0.0
        force.y = 0.0
        force.z = msg.data

        torque = Vector3()
        torque.x = 0.0
        torque.y = 0.0
        torque.z = 0.0

        msg = Wrench()
        msg.force = force
        msg.torque = torque

        self.publisherArmRight.publish(msg)


    def listener_callback_left(self, msg):

        self.get_logger().info('Publishing Left Prop: "%s"' % msg.data)

        force = Vector3()
        force.x = 0.0
        force.y = 0.0
        force.z = msg.data

        torque = Vector3()
        torque.x = 0.0
        torque.y = 0.0
        torque.z = 0.0

        msg = Wrench()
        msg.force = force
        msg.torque = torque

        self.publisherArmLeft.publish(msg)



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