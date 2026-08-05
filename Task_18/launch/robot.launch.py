
import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, GroupAction, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration

from launch_ros.actions import Node


def generate_launch_description():

    package_name = "task_18"

    world = LaunchConfiguration("world")
    rviz = LaunchConfiguration("rviz")

    package_dir = get_package_share_directory(package_name)

    world_path = os.path.join(
        package_dir,
        "worlds",
        "world.sdf",
    )

    urdf_path = os.path.join(
        package_dir,
        "urdf",
        "robot.urdf",
    )

    rviz_config_file = os.path.join(
        package_dir,
        "rviz",
        "bot.rviz",
    )

    bridge_config_file = os.path.join(
        package_dir,
        "config",
        "gz_bridge.yaml",
    )



    declare_world = DeclareLaunchArgument(
        "world",
        default_value=world_path,
        description="Full path to the Gazebo world file",
    )

    declare_rviz = DeclareLaunchArgument(
        "rviz",
        default_value="False",
        description="Open RViz if set to True",
    )



    robot_state_publisher = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                package_dir,
                "launch",
                "rsp.launch.py",
            )
        ),
        launch_arguments={
            "use_sim_time": "true",
            "urdf": urdf_path,
        }.items(),
    )



    gazebo_server = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory("ros_gz_sim"),
                "launch",
                "gz_sim.launch.py",
            )
        ),
        launch_arguments={
            "gz_args": ["-r -s -v1 ", world],
            "on_exit_shutdown": "true",
        }.items(),
    )



    gazebo_client = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory("ros_gz_sim"),
                "launch",
                "gz_sim.launch.py",
            )
        ),
        launch_arguments={
            "gz_args": "-g",
        }.items(),
    )

  

    spawn_robot = Node(
        package="ros_gz_sim",
        executable="create",
        arguments=[
            "-topic",
            "robot_description",
            "-name",
            "diff_bot",
            "-z",
            "0.2",
        ],
        output="screen",
    )

   

    bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        parameters=[
            {
                "config_file": bridge_config_file,
            }
        ],
        output="screen",
    )



    rviz2 = GroupAction(
        condition=IfCondition(rviz),
        actions=[
            Node(
                package="rviz2",
                executable="rviz2",
                arguments=[
                    "-d",
                    rviz_config_file,
                ],
                output="screen",
            )
        ],
    )



    slam_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                package_dir,
                "launch",
                "slam.launch.py",
            )
        )
    )


    return LaunchDescription(
        [
            # Arguments
            declare_world,
            declare_rviz,

            # Robot
            robot_state_publisher,

            # Gazebo
            gazebo_server,
            gazebo_client,

            # ROS <-> Gazebo
            bridge,

            # Spawn robot
            spawn_robot,

            # RViz
            rviz2,

            # SLAM Toolbox
            slam_launch,
        ]
    )
