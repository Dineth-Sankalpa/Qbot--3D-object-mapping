import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess, RegisterEventHandler, TimerAction
from launch_ros.actions import Node
from launch.event_handlers import OnProcessStart
from launch.substitutions import Command  # <-- ADDED THIS IMPORT
from launch.actions import SetEnvironmentVariable
def generate_launch_description():
    pkg_dir = get_package_share_directory('qbot_description')

    # Build file paths
    urdf_file = os.path.join(pkg_dir, 'urdf', 'qbot.urdf')
    world_file = os.path.join(pkg_dir, 'sdf', 'qbot_world.sdf')
    rviz_config_file = os.path.join(pkg_dir, 'rviz', 'qbot.rviz')

    # <-- CHANGED THIS: We now use Xacro to parse the file so $(find ...) works!
    robot_desc = Command(['xacro ', urdf_file])

    # Set environment variables for Gazebo so it can find plugins 
    os.environ['IGN_GAZEBO_SYSTEM_PLUGIN_PATH'] = '/opt/ros/humble/lib'
    os.environ['IGN_GAZEBO_RESOURCE_PATH'] = os.path.join(pkg_dir, 'sdf')
    
    # Add LD_LIBRARY_PATH so the ign_ros2_control library is found
    current_ld_library_path = os.environ.get('LD_LIBRARY_PATH', '')
    os.environ['LD_LIBRARY_PATH'] = f'/opt/ros/humble/lib:{current_ld_library_path}'

    # Node: Robot State Publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_desc, 'use_sim_time': True}]
    )

    # Action: Start Gazebo (Fortress)
    start_gazebo = ExecuteProcess(
        cmd=['ign', 'gazebo', '-r', world_file],
        cwd=os.path.join(pkg_dir, 'sdf'), 
        output='screen'
    )

    # Node: RViz2
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config_file],
        parameters=[{'use_sim_time': True}]
    )

    # ROS-Gazebo Bridge for Lidar
    bridge_node = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/scan@sensor_msgs/msg/LaserScan[ignition.msgs.LaserScan'
        ],
        output='screen'
    )

    # Bridge for /clock from Gazebo to ROS
    bridge_clock = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=['/clock@rosgraph_msgs/msg/Clock[ignition.msgs.Clock'], # <-- Removed the ']' at the very end
        output='screen',
        parameters=[{'use_sim_time': True}]
    )

    # Controllers
    joint_state_broadcaster = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster"],
    )

    diff_drive_controller = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["diff_drive_controller"],
    )

    # Delay controllers to let Gazebo load 
    delay_joint_state_broadcaster = RegisterEventHandler(
        event_handler=OnProcessStart(
            target_action=start_gazebo,
            on_start=[TimerAction(period=3.0, actions=[joint_state_broadcaster])]
        )
    )

    delay_diff_drive_controller = RegisterEventHandler(
        event_handler=OnProcessStart(
            target_action=joint_state_broadcaster,
            on_start=[TimerAction(period=2.0, actions=[diff_drive_controller])]
        )
    )

    return LaunchDescription([
        SetEnvironmentVariable('IGN_GAZEBO_RESOURCE_PATH', os.path.join(get_package_share_directory('qbot_description'), '..')),
        robot_state_publisher,
        start_gazebo,
        rviz_node,
        bridge_node,
        bridge_clock,
        delay_joint_state_broadcaster,
        delay_diff_drive_controller
    ])