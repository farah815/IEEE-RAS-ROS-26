from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():

    slam_toolbox_dir = get_package_share_directory('slam_toolbox')
    task_18_dir = get_package_share_directory('task_18')

    slam_launch = os.path.join(
        slam_toolbox_dir,
        'launch',
        'online_async_launch.py'
    )

    slam_config = os.path.join(
        task_18_dir,
        'config',
        'slam_toolbox.yaml'
    )

    return LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(slam_launch),
            launch_arguments={
                'slam_params_file': slam_config,
                'use_sim_time': 'true'
            }.items()
        )
    ])