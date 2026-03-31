import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import math

class CircularScannerNode(Node):
    def __init__(self):
        # Initialize the node with the name 'circular_scanner_mock'
        super().__init__('circular_scanner_mock')
        
        # Create a publisher to the /cmd_vel topic
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        
        # --- Configurable Parameters ---
        self.fov_vertical_deg = 24.0
        self.object_height = 0.5   # meters
        self.scan_duration = 60.0  # seconds for a full 360-degree orbit
        self.safety_margin = 1.2   # 20% padding
        
        # Calculate Kinematics
        self.radius = self.calculate_radius()
        self.linear_vel, self.angular_vel = self.calculate_velocities()
        
        # Pre-fill the Twist message
        self.twist_msg = Twist()
        self.twist_msg.linear.x = self.linear_vel
        self.twist_msg.angular.z = self.angular_vel
        
        # Create a timer to publish at 10 Hz (0.1 seconds)
        timer_period = 0.1  
        self.timer = self.create_timer(timer_period, self.timer_callback)
        
        self.get_logger().info('Starting mock circular trajectory. Press Ctrl+C to stop.')

    def calculate_radius(self):
        """Calculates required radius based on FOV and object height."""
        fov_rad = math.radians(self.fov_vertical_deg)
        # R = H / (2 * tan(theta / 2))
        min_radius = self.object_height / (2 * math.tan(fov_rad / 2))
        target_radius = min_radius * self.safety_margin
        
        self.get_logger().info(f'Object Height: {self.object_height}m | Target Radius: {target_radius:.3f}m')
        return target_radius

    def calculate_velocities(self):
        """Calculates linear and angular velocities for the trajectory."""
        # omega = 2*pi / T
        omega = (2 * math.pi) / self.scan_duration
        # v = omega * R
        v = omega * self.radius
        
        self.get_logger().info(f'Calculated linear_vel: {v:.3f} m/s | angular_vel: {omega:.3f} rad/s')
        return v, omega

    def timer_callback(self):
        """This function runs every 0.1 seconds to publish the velocity."""
        self.cmd_pub.publish(self.twist_msg)

def main(args=None):
    # Initialize the ROS 2 Python client library
    rclpy.init(args=args)
    
    # Instantiate the node
    scanner = CircularScannerNode()
    
    # Keep the node running
    try:
        rclpy.spin(scanner)
    except KeyboardInterrupt:
        pass
    finally:
        # Clean up on shutdown
        scanner.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()