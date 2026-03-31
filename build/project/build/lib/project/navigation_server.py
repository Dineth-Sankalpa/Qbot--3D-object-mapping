import math
import time
import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup

# Import standard messages and our custom interface
from interfaces.msg import Position
from nav_msgs.msg import Odometry
from interfaces.action import Navigation

class NavigationServer(Node):

    def __init__(self):
        super().__init__('navigation_server')

        # 1. Declare Parameters (Section 3.3)
        # Default: goal_tolerance=2.0, feedback_rate=4.0 [cite: 60]
        self.declare_parameter('goal_tolerance', 0.1)
        self.declare_parameter('feedback_rate', 4.0)

        # 2. Internal State for Robot Position
        self.current_x = 0.0
        self.current_y = 0.0
        
        # Use a ReentrantCallbackGroup to allow callbacks to run in parallel
        self.callback_group = ReentrantCallbackGroup()

        # 3. Subscriber to /odom (Section 3.2.2) 
        self.subscription = self.create_subscription(
            Odometry,
            '/odom',
            self.odom_callback,
            10,
            callback_group=self.callback_group
        )

        # 4. Action Server (Section 3.2.2) 
        self._action_server = ActionServer(
            self,
            Navigation,
            'navigate',
            self.execute_callback,
            callback_group=self.callback_group
        )
        
        self.get_logger().info('Navigation Action Server has been started.')

    def odom_callback(self, msg):
        # Update current position from odometry
        self.current_x = msg.pose.pose.position.x
        self.current_y = msg.pose.pose.position.y

    def execute_callback(self, goal_handle):
        self.get_logger().info('Executing goal...')

        # Get parameter values
        goal_tolerance = self.get_parameter('goal_tolerance').value
        feedback_rate = self.get_parameter('feedback_rate').value
        loop_rate = 1.0 / feedback_rate

        # Extract target goal from the request [cite: 28]
        target_x = goal_handle.request.end_position.x
        target_y = goal_handle.request.end_position.y

        feedback_msg = Navigation.Feedback()
        result = Navigation.Result()

        # Loop until the goal is reached
        while rclpy.ok():
            # Check if goal is cancelled
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                self.get_logger().info('Goal canceled')
                return result

            # Calculate Euclidean distance [cite: 37]
            diff_x = target_x - self.current_x
            diff_y = target_y - self.current_y
            distance = math.sqrt(diff_x**2 + diff_y**2)

            # Check if we reached the goal [cite: 38]
            if distance < goal_tolerance:
                self.get_logger().info(f'Goal reached! Distance: {distance:.2f}')
                goal_handle.succeed()
                result.success = True
                return result

            # If not reached, send feedback (Direction) [cite: 39]
            # Calculate angle to goal (direction)
            direction = math.atan2(diff_y, diff_x)
            
            feedback_msg.direction = float(direction)
            goal_handle.publish_feedback(feedback_msg)
            
            # self.get_logger().info(f'Distance: {distance:.2f}, Sending direction: {direction:.2f}')

            # Sleep to maintain feedback rate
            time.sleep(loop_rate)

def main(args=None):
    rclpy.init(args=args)
    
    node = NavigationServer()
    
    # Use MultiThreadedExecutor so the Action loop doesn't block the Odom subscriber 
    executor = MultiThreadedExecutor()
    executor.add_node(node)
    
    try:
        executor.spin()
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()