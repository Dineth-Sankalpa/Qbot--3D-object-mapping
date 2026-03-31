import math
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient

from geometry_msgs.msg import TwistStamped  
from nav_msgs.msg import Odometry

from interfaces.action import Navigation
from interfaces.msg import Position

INDEX_NUMBER = "230522H"  

class QbotControllerNode(Node):
    def __init__(self):
        super().__init__('qbot_controller')
        self.declare_parameter('linear_speed', 0.5)
        self.linear_speed = self.get_parameter('linear_speed').get_parameter_value().double_value

        self.current_yaw = 0.0
        self.goal_achieved = False
        self.goal_sent = False

        self.odom_sub = self.create_subscription(Odometry, '/odom', self.update_yaw_from_odom, 10)
        self.cmd_pub = self.create_publisher(TwistStamped, '/cmd_vel', 10)
        self._action_client = ActionClient(self, Navigation, 'navigate')
        self.timer = self.create_timer(1.0, self.send_navigation_goal_once)

        self.get_logger().info("Qbot Controller Node initialized.")

    @staticmethod
    def calculate_goal_from_index(index_number: str):
        digits = [int(ch) for ch in index_number if ch.isdigit()]
        sum_digits = sum(digits)
        product_digits = 1
        has_non_zero = False
        for digit in digits:
            if digit == 0: continue
            has_non_zero = True
            product_digits *= digit
        if not has_non_zero: product_digits = 0
        return float(sum_digits // 25), float(product_digits // 25)
    
    @staticmethod
    def compute_yaw_error(a, b):
        diff = a - b
        return math.atan2(math.sin(diff), math.cos(diff))

    def update_yaw_from_odom(self, msg: Odometry):
        q = msg.pose.pose.orientation
        siny_cosp = 2.0 * (q.w * q.z)
        cosy_cosp = 1.0 - 2.0 * (q.z * q.z)
        self.current_yaw = math.atan2(siny_cosp, cosy_cosp)

    def send_navigation_goal_once(self):
        if self.goal_sent: return
        if not self._action_client.server_is_ready():
            self.get_logger().info("Waiting for action server...")
            return

        goal_msg = Navigation.Goal()
        goal_x, goal_y = self.calculate_goal_from_index(INDEX_NUMBER)
        
        target_pos = Position()
        target_pos.x, target_pos.y = goal_x, goal_y
        goal_msg.end_position = target_pos
        self.goal_sent = True

        self.get_logger().info(f"Sending goal: x={goal_x}, y={goal_y}")
        send_goal_future = self._action_client.send_goal_async(goal_msg, feedback_callback=self.handle_navigation_feedback)
        send_goal_future.add_done_callback(self.handle_navigation_goal_response)

    def handle_navigation_goal_response(self, navigation_goal_response):
        goal_handle = navigation_goal_response.result()
        if not goal_handle.accepted: return
        get_result_future = goal_handle.get_result_async()
        get_result_future.add_done_callback(self.handle_navigation_result)

    def handle_navigation_result(self, navigation_result):
        result = navigation_result.result().result
        self.goal_achieved = True

        stop_cmd = TwistStamped()
        stop_cmd.header.stamp = self.get_clock().now().to_msg()
        stop_cmd.header.frame_id = 'base_link'
        stop_cmd.twist.linear.x = 0.0
        stop_cmd.twist.angular.z = 0.0
        self.cmd_pub.publish(stop_cmd)

    def handle_navigation_feedback(self, feedback_msg):
        if self.goal_achieved: return
        yaw_error = self.compute_yaw_error(feedback_msg.feedback.direction, self.current_yaw)

        cmd = TwistStamped()
        cmd.header.stamp = self.get_clock().now().to_msg()
        cmd.header.frame_id = 'base_link'
        cmd.twist.linear.x = self.linear_speed
        cmd.twist.angular.z = 2.0 * yaw_error
        self.cmd_pub.publish(cmd)

def main(args=None):
    rclpy.init(args=args)
    node = QbotControllerNode()
    try: rclpy.spin(node)
    except KeyboardInterrupt: pass
    finally:
        node.destroy_node()
        if rclpy.ok(): rclpy.shutdown()

if __name__ == '__main__':
    main()