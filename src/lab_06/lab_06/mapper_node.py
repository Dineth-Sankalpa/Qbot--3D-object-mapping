import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
# import matplotlib.pyplot as plt


class MapperNode(Node):

    def __init__(self):
        super().__init__('mapper_node')
        
        self.subscription = self.create_subscription(
            Odometry,
            '/odom',
            self.listener_callback,
            10
        )
        
        # Lists to store the path
        self.path_x = []
        self.path_y = []
        
        self.get_logger().info('Mapper Node Started. Recording path...')

    def listener_callback(self, msg):
        # Extract position
        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y
        
        # Store for plotting
        self.path_x.append(x)
        self.path_y.append(y)
        
        # Log every 10th point to avoid console spam
        if len(self.path_x) % 10 == 0:
            self.get_logger().info(f'Recording path... Points: {len(self.path_x)}')

    def save_plot(self):
        try:
            import matplotlib.pyplot as plt
            self.get_logger().info('Saving plot to robot_path.png...')
            
            if not self.path_x:
                self.get_logger().warn('No path data to plot!')
                return

            plt.figure()
            plt.plot(self.path_x, self.path_y, label='Robot Path')
            plt.scatter(self.path_x[0], self.path_y[0], color='green', label='Start', zorder=5)
            plt.scatter(self.path_x[-1], self.path_y[-1], color='red', label='End', zorder=5)
            plt.title('Robot Trajectory')
            plt.xlabel('X Position')
            plt.ylabel('Y Position')
            plt.grid(True)
            plt.legend()
            plt.axis('equal') 
            
            # Save the figure
            plt.savefig('robot_path.png')
            self.get_logger().info('Plot saved successfully.')
        except ImportError:
            self.get_logger().info('Matplotlib is not installed. Cannot save plot.')

def main(args=None):
    rclpy.init(args=args)
    node = MapperNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.save_plot() # Save before destroying
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()

if __name__ == '__main__':
    main()