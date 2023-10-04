import rclpy
from rclpy.node import Node

from std_msgs.msg import String, Float32
from geometry_msgs.msg import Wrench, Vector3



class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('propeller')


        # Parameters
        self.declare_parameter("topicPropellerForce", '/force/prop')
        self.declare_parameter("topicPropellerCmd",'/cmd/prop')

        
        subtopic = self.get_parameter('topicPropellerCmd').value
        pubtopic = self.get_parameter('topicPropellerForce').value

        self.publisher = self.create_publisher(Wrench, pubtopic, 10)

        self.subscription = self.create_subscription(
            Float32,
            subtopic,
            self.listener_callback,
            10
        )

        self.subscription # prevent unused variable warning
        self.get_logger().info(f'Propeller Online! Subscribing to {subtopic} - publishing to {pubtopic}')
        # ros2 topic pub -1 /cmd/prop_left  std_msgs/Float32 '{data: 3.0}'


    def listener_callback(self, msg):

        #self.get_logger().info('Publishing Prop: "%s"' % msg.data)

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

        self.publisher.publish(msg)




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