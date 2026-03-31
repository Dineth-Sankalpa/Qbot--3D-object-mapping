#!/usr/bin/env python3
from geometry_msgs.msg import Quaternion, TransformStamped
from sensor_msgs.msg import JointState
from tf2_ros import TransformBroadcaster
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Quaternion
from interfaces.action import Navigation
from interfaces.msg import Position
import math
import random

INDEX_NUMBER = "230522H"

class OdometryNode(Node):

    def __init__(self):
        super().__init__('odom_node')

        # 1. Declare Parameters
        self.declare_parameter('step_size', 0.1)     
        self.declare_parameter('noise_sigma', 0.1)   
        self.declare_parameter('publish_rate', 10.0) 

        # 2. Internal State
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0 
        self.goal_sent = False

        # 3. Publisher
        self.odom_pub = self.create_publisher(Odometry, '/odom', 10)

        # Timer: Publish to /odom at the defined rate
        pub_rate = self.get_parameter('publish_rate').value
        self.timer = self.create_timer(1.0 / pub_rate, self.publish_odom)

        # 4. Action Client
        self._action_client = ActionClient(self, Navigation, 'navigate')

        # Timer: Check server availability and send goal
        self.goal_timer = self.create_timer(1.0, self.send_goal)
        
        self.get_logger().info('Odometry Node (Action Client) initialized.')

        # Create publisher for joint states and a TF broadcaster
        self.joint_pub = self.create_publisher(JointState, '/joint_states', 10)
        self.tf_broadcaster = TransformBroadcaster(self)

        # Robot parameters 
        self.declare_parameter('odom_frame', 'odom')
        self.declare_parameter('base_frame', 'base_link')
        self.declare_parameter('left_wheel_joint', 'wheel_left_joint')
        self.declare_parameter('right_wheel_joint', 'wheel_right_joint')
        self.declare_parameter('wheel_radius', 0.05)
        self.declare_parameter('wheel_separation', 0.386)

        self.odom_frame = self.get_parameter('odom_frame').value
        self.base_frame = 'base_footprint'
        self.left_wheel_joint = self.get_parameter('left_wheel_joint').value
        self.right_wheel_joint = self.get_parameter('right_wheel_joint').value
        self.wheel_radius = self.get_parameter('wheel_radius').value
        self.wheel_separation = self.get_parameter('wheel_separation').value

        # Internal wheel state variables
        self.left_wheel_pos = 0.0
        self.right_wheel_pos = 0.0
        self.last_direction = 0.0

    @staticmethod
    def calculate_goal_from_index(index_number: str):
        digits = [int(ch) for ch in index_number if ch.isdigit()]
        if not digits:
            return 10.0, 10.0 
            
        sum_digits = sum(digits)
        
        product_digits = 1
        has_non_zero = False
        for digit in digits:
            if digit == 0:
                continue
            has_non_zero = True
            product_digits *= digit
        if not has_non_zero:
            product_digits = 0
            
        goal_x = sum_digits // 25
        goal_y = product_digits // 25
        return float(goal_x), float(goal_y)

    def send_goal(self, goal_x=None, goal_y=None):
        if self.goal_sent:
            return

        # Wait for Action Server
        if not self._action_client.wait_for_server(timeout_sec=1.0):
            self.get_logger().info('Waiting for navigation action server...')
            return

        # Prepare Goal
        if goal_x is None or goal_y is None:
            goal_x, goal_y = self.calculate_goal_from_index(INDEX_NUMBER)
        goal_msg = Navigation.Goal()
        goal_msg.end_position.x = goal_x
        goal_msg.end_position.y = goal_y
        self.get_logger().info(f'Sending Goal: x={goal_msg.end_position.x}, y={goal_msg.end_position.y}')
        
        # Send Goal
        self._send_goal_future = self._action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback
        )
        self._send_goal_future.add_done_callback(self.goal_response_callback)
        
        self.goal_sent = True
        self.goal_timer.cancel()

    def feedback_callback(self, feedback_msg):
        direction = feedback_msg.feedback.direction
        step_size = self.get_parameter('step_size').value
        distance = step_size

        # Update internal state 
        self.x += step_size * math.cos(direction)
        self.y += step_size * math.sin(direction)
        self.theta = direction 

        # Wheel Kinematics
        delta_yaw = self.theta - self.last_direction
        
        # Convert base motion to left/right wheel distances
        left_distance = distance - (delta_yaw * self.wheel_separation / 2.0)
        right_distance = distance + (delta_yaw * self.wheel_separation / 2.0)
        
        # Convert wheel distances to wheel angle increments
        left_delta = left_distance / self.wheel_radius
        right_delta = right_distance / self.wheel_radius
        
        # Accumulate wheel positions
        self.left_wheel_pos += left_delta
        self.right_wheel_pos += right_delta
        
        self.last_direction = self.theta

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected :(')
            return

        self.get_logger().info('Goal accepted!')
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        result = future.result().result
        if result.success:
            self.get_logger().info('Navigation Success: Goal Reached!')
            self.timer.cancel()
            self.destroy_publisher(self.odom_pub)
            self.destroy_publisher(self.joint_pub)
        else:
            self.get_logger().info('Navigation Finished (No Success).')

    @staticmethod
    def yaw_to_quaternion(yaw):
        return Quaternion(
            x=0.0,
            y=0.0,
            z=math.sin(yaw / 2.0),
            w=math.cos(yaw / 2.0)
        )

    def publish_tf(self, stamp, x_pos, y_pos, yaw):
        tf_msg = TransformStamped()
        tf_msg.header.stamp = stamp
        tf_msg.header.frame_id = self.odom_frame
        tf_msg.child_frame_id = self.base_frame
        tf_msg.transform.translation.x = x_pos
        tf_msg.transform.translation.y = y_pos
        tf_msg.transform.translation.z = 0.0
        tf_msg.transform.rotation = self.yaw_to_quaternion(yaw)
        self.tf_broadcaster.sendTransform(tf_msg)

    def publish_joint_state(self, stamp, left_velocity, right_velocity):
        joint_msg = JointState()
        joint_msg.header.stamp = stamp
        joint_msg.name = [self.left_wheel_joint, self.right_wheel_joint]
        joint_msg.position = [self.left_wheel_pos, self.right_wheel_pos]
        joint_msg.velocity = [left_velocity, right_velocity]
        self.joint_pub.publish(joint_msg)

    def publish_odom(self):
        msg = Odometry()
        stamp = self.get_clock().now().to_msg()
        msg.header.stamp = stamp
        msg.header.frame_id = "odom"
        msg.child_frame_id = "base_footprint"

        # Add Noise
        sigma = self.get_parameter('noise_sigma').value
        noisy_x = self.x + random.gauss(0, sigma)
        noisy_y = self.y + random.gauss(0, sigma)

        # Set Position
        msg.pose.pose.position.x = noisy_x
        msg.pose.pose.position.y = noisy_y
        msg.pose.pose.position.z = 0.0

        # Set Orientation 
        msg.pose.pose.orientation = self.yaw_to_quaternion(self.theta)

        self.odom_pub.publish(msg)

        # --- Call the new TF and Joint State publishers ---
        # We publish 0.0 for velocity here since we are just visualizing positions
        self.publish_tf(stamp, noisy_x, noisy_y, self.theta)
        self.publish_joint_state(stamp, 0.0, 0.0)

def main(args=None):
    rclpy.init(args=args)
    node = OdometryNode()

    goal_x, goal_y = node.calculate_goal_from_index(INDEX_NUMBER)
    node.send_goal(goal_x, goal_y)
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        # Save plot if it is the mapper node
        if hasattr(node, 'save_plot'): 
            node.save_plot()
            
        node.destroy_node()
        # Check before shutting down to avoid the error
        if rclpy.ok():
            rclpy.shutdown()

if __name__ == '__main__':
    main()