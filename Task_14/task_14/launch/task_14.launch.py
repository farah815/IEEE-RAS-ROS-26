from launch import LaunchDescription
from launch.actions import (
    ExecuteProcess,
    IncludeLaunchDescription,
    TimerAction,
    SetEnvironmentVariable,
)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():

    # Path to custom world
    world = os.path.join(
        get_package_share_directory('task_14'),
        'worlds',
        'my_world.sdf'
    )

    # TurtleBot3 model path
    resource_path = os.path.join(
        os.environ['HOME'],
        'turtlebot3_ws',
        'install',
        'turtlebot3_gazebo',
        'share',
        'turtlebot3_gazebo',
        'models'
    )

    # Add TurtleBot3 models to Gazebo search path
    set_resource_path = SetEnvironmentVariable(
        name='GZ_SIM_RESOURCE_PATH',
        value=os.environ.get('GZ_SIM_RESOURCE_PATH', '') + ':' + resource_path
    )

    # Set TurtleBot3 model
    set_model = SetEnvironmentVariable(
        name='TURTLEBOT3_MODEL',
        value='waffle'
    )

    # Start Gazebo
    gazebo = ExecuteProcess(
        cmd=[
            'gz',
            'sim',
            world,
            '-r'
        ],
        output='screen'
    )

    # Spawn TurtleBot3 after Gazebo loads
    spawn_robot = TimerAction(
        period=3.0,
        actions=[
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    os.path.join(
                        get_package_share_directory('turtlebot3_gazebo'),
                        'launch',
                        'spawn_turtlebot3.launch.py'
                    )
                )
            )
        ]
    )

    # Start autonomous controller
    autonomous = TimerAction(
        period=5.0,
        actions=[
            Node(
                package='task_14',
                executable='autonomous_mover',
                output='screen'
            )
        ]
    )

    return LaunchDescription([
        set_resource_path,
        set_model,
        gazebo,
        spawn_robot,
        autonomous,
    ])
