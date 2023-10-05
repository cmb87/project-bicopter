import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

class ImagePub(Node):

    def __init__(self):

        super().__init__('rpi_image_pub')

        self.declare_parameter("pubtopic", "rpi_video_feed")
        self.declare_parameter("pubperiod", 0.5)
        self.declare_parameter("width", 352)
        self.declare_parameter("height", 288)
        self.declare_parameter("cameraId", 0)

        self.get_logger().info('Publishing to topic: "%s"' % self.get_parameter('pubtopic').value)

        self.timer = self.create_timer(self.get_parameter('pubperiod').value, self.camera_callback)

        self.publisher_ = self.create_publisher(Image, self.get_parameter('pubtopic').value, 10)

        self.cap = cv2.VideoCapture(self.get_parameter('cameraId').value)
       # self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT,self.get_parameter('height').value)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH,self.get_parameter('width').value)



        self.bridge = CvBridge()

    def camera_callback(self):
        ret, frame = self.cap.read()

        if ret:
            self.get_logger().info(f"Image shape {frame.shape}")

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            frame = self.bridge.cv2_to_imgmsg(frame, 'mono8')
            self.publisher_.publish(frame)



def main(args=None):
    rclpy.init(args=args)
    publisher = ImagePub()
    rclpy.spin(publisher)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()