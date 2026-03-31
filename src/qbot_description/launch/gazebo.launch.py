import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, AppendEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    pkg_qbot_description = get_package_share_directory('qbot_description')
    pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')

    # Tell Gazebo where to look for files
    set_model_path = AppendEnvironmentVariable(
        'IGN_GAZEBO_RESOURCE_PATH',
        os.path.join(pkg_qbot_description, 'sdf')
    )

    # Path to the worlld file
    world_file = os.path.join(pkg_qbot_description, 'sdf', 'qbot_world.sdf')

    # Launch Gazebo 
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={'gz_args': f'-r {world_file}'}.items(),
    )

    return LaunchDescription([
        set_model_path,
        gazebo
    ])