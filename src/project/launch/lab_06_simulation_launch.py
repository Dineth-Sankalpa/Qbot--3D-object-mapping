import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    # 1. Get package directories
    qbot_desc_dir = get_package_share_directory('qbot_description')
    project_dir = get_package_share_directory('project')

    # 2. Include the Simulation (Gazebo + RViz)
    simulation_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(qbot_desc_dir, 'launch', 'simulation.launch.py')
        )
    )

    # 3. SLAM Toolbox Node 
    # Make sure this points to the exact folder where you fixed the base_frame!
    slam_params_file = os.path.join(project_dir, 'config', 'slam_toolbox_params.yaml')
    
    slam_node = Node(
        package='slam_toolbox',
        executable='async_slam_toolbox_node',
        name='slam_toolbox',
        output='screen',
        parameters=[
            slam_params_file,
            {'use_sim_time': True}
        ],
        
        
    )

    # 4. Navigation Action Server
    navigation_node = Node(
        package='project',
        executable='navigation_server', 
        output='screen',
        parameters=[{'use_sim_time': True}],
        remappings=[                                            
            ('/cmd_vel', '/diff_drive_controller/cmd_vel'),     
            ('/odom', '/diff_drive_controller/odom')            
        ]                                                       
    )

    # 5. Qbot Controller Node 
    controller_node = Node(
        package='project',
        executable='qbot_controller',
        output='screen',
        parameters=[{'use_sim_time': True}],
        remappings=[
            ('/cmd_vel', '/diff_drive_controller/cmd_vel'),
            ('/odom', '/diff_drive_controller/odom')
        ]
    )

    return LaunchDescription([
        simulation_launch,
        slam_node,
        navigation_node,
        controller_node
    ])