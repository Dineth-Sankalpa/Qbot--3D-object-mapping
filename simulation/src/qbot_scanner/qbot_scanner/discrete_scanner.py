import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import math

class DiscreteScanner(Node):
    def __init__(self):
        super().__init__('discrete_scanner')
        
        # Publishers and Subscribers
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.odom_sub = self.create_subscription(Odometry, '/odom', self.odom_callback, 10)
        self.image_sub = self.create_subscription(Image, '/camera/color/image_raw', self.image_callback, 10)
        
        self.bridge = CvBridge()
        
        # State Variables
        self.current_yaw = 0.0
        self.target_yaw = 0.0
        self.starting_yaw = None
        self.images_captured = 0
        self.state = 'INIT' # INIT, TURN, STOP, CAPTURE, DONE
        
        # Constants
        self.angle_increment = math.radians(15.0)
        self.tolerance = 0.05
        self.max_images = int(360 / 15)
        self.latest_image = None

        self.timer = self.create_timer(0.1, self.control_loop)
        self.get_logger().info("Discrete Scanner Initialized.")

    def get_yaw_from_quaternion(self, q):
        # Math for quaternion to yaw
        siny_cosp = 2 * (q.w * q.z + q.x * q.y)
        cosy_cosp = 1 - 2 * (q.y * q.y + q.z * q.z)
        return math.atan2(siny_cosp, cosy_cosp)

    def odom_callback(self, msg):
        self.current_yaw = self.get_yaw_from_quaternion(msg.pose.pose.orientation)
        if self.starting_yaw is None:
            self.starting_yaw = self.current_yaw
            self.target_yaw = self.current_yaw

    def image_callback(self, msg):
        self.latest_image = msg

    def control_loop(self):
        if self.state == 'DONE':
            return
            
        if self.starting_yaw is None:
            return # Waiting for odom

        msg = Twist()

        if self.state == 'INIT':
            self.state = 'CAPTURE'

        elif self.state == 'CAPTURE':
            if self.latest_image is not None:
                cv_img = self.bridge.imgmsg_to_cv2(self.latest_image, "bgr8")
                filename = f"scan_frame_{self.images_captured:02d}.png"
                cv2.imwrite(filename, cv_img)
                self.get_logger().info(f"Captured {filename}")
                
                self.images_captured += 1
                if self.images_captured >= self.max_images:
                    self.state = 'DONE'
                    self.get_logger().info("Scanning Complete.")
                else:
                    self.target_yaw = (self.target_yaw + self.angle_increment) % (2 * math.pi)
                    if self.target_yaw > math.pi:
                        self.target_yaw -= 2 * math.pi
                    self.state = 'TURN'

        elif self.state == 'TURN':
            error = self.target_yaw - self.current_yaw
            # Normalize error
            if error > math.pi: error -= 2 * math.pi
            if error < -math.pi: error += 2 * math.pi

            if abs(error) > self.tolerance:
                msg.angular.z = 0.3 if error > 0 else -0.3 # Fixed turn speed
                self.cmd_pub.publish(msg)
            else:
                msg.angular.z = 0.0
                self.cmd_pub.publish(msg)
                self.state = 'STOP'
                self.stop_time = self.get_clock().now()

        elif self.state == 'STOP':
            # Wait 1 second to let camera settle and prevent motion blur
            if (self.get_clock().now() - self.stop_time).nanoseconds > 1e9:
                self.state = 'CAPTURE'

def main(args=None):
    rclpy.init(args=args)
    node = DiscreteScanner()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()