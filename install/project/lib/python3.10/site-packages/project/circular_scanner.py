#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TwistStamped  # Changed from Twist for Gazebo compatibility
import math

class CircularScannerNode(Node):
    def __init__(self):
        super().__init__('circular_scanner')
       
        # Publisher to the /cmd_vel topic using TwistStamped
        self.cmd_pub = self.create_publisher(TwistStamped, '/cmd_vel', 10)
       
        # --- Configurable Parameters ---
        self.fov_vertical_deg = 24.0
        self.object_height = 0.5   # meters
        self.scan_duration = 60.0  # seconds for a full 360-degree orbit
        self.safety_margin = 1.2   # 20% padding
       
        # Calculate Kinematics
        self.radius = self.calculate_radius()
        self.linear_vel, self.angular_vel = self.calculate_velocities()
       
        # Create a timer to publish at 10 Hz (0.1 seconds)
        self.timer = self.create_timer(0.1, self.timer_callback)
        self.get_logger().info('Starting continuous circular trajectory. Press Ctrl+C to stop.')

    def calculate_radius(self):
        """Calculates required radius based on FOV and object height."""
        fov_rad = math.radians(self.fov_vertical_deg)
        min_radius = self.object_height / (2 * math.tan(fov_rad / 2))
        target_radius = min_radius * self.safety_margin
        self.get_logger().info(f'Object Height: {self.object_height}m | Target Radius: {target_radius:.3f}m')
        return target_radius

    def calculate_velocities(self):
        """Calculates linear and angular velocities for the trajectory."""
        omega = (2 * math.pi) / self.scan_duration
        v = omega * self.radius
        self.get_logger().info(f'Calculated linear_vel: {v:.3f} m/s | angular_vel: {omega:.3f} rad/s')
        return v, omega

    def timer_callback(self):
        """This function runs every 0.1 seconds to publish the stamped velocity."""
        cmd = TwistStamped()
       
        # Required for Lab 06 diff_drive_controller
        cmd.header.stamp = self.get_clock().now().to_msg()
        cmd.header.frame_id = 'base_link'
       
        cmd.twist.linear.x = self.linear_vel
        cmd.twist.angular.z = self.angular_vel
       
        self.cmd_pub.publish(cmd)

def main(args=None):
    rclpy.init(args=args)
    scanner = CircularScannerNode()
    try:
        rclpy.spin(scanner)
    except KeyboardInterrupt:
        pass
    finally:
        scanner.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()