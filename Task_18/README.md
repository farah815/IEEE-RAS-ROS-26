# Task 18

This repository contains a starter differential-drive robot for ROS 2 Jazzy and Gazebo Harmonic.

The robot model is already prepared with:

* Robot body
* Left and right wheels
* Wheel joints
* Caster wheel
* LiDAR link
* IMU link
* Gazebo world
* Robot spawn launch file

The Gazebo plugins, sensors, and ROS-Gazebo bridge configuration are intentionally not implemented.

## Build

```bash
cd ~/ros2_ws
colcon build --packages-select task_18
source install/setup.bash
```

## Launch

To launch the complete simulation with RViz:

```bash
ros2 launch task_18 robot.launch.py rviz:=True
```



