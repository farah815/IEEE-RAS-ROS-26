
# Task 10 — ROS 2 Turtlesim Control

## Successful Installation

The ROS 2 Jazzy desktop was installed successfully, including all required packages such as `ros-jazzy-desktop`, `libpcl-dev`, and `libvtk9-dev`.

![Successful Installation](successful_installation_screenshot.png)

---

## Nodes, Topics, and Services

### Terminal Output

![Nodes Topics Services](list_of_nodes_topics_and_services_screenshots.png)

### Active Nodes
- `/turtlesim` — runs the simulation window and controls the turtle
- `/teleop_turtle` — reads keyboard input and sends movement commands

### Active Topics
- `/turtle1/cmd_vel` — receives movement commands (linear and angular velocity)
- `/turtle1/pose` — continuously publishes the turtle's current position
- `/turtle1/color_sensor` — publishes the color under the turtle's pen
- `/parameter_events`, `/rosout` — internal ROS 2 system topics

### Active Services
- `/clear` — removes all drawings from the screen
- `/reset` — returns the turtle to its starting position
- `/spawn` — creates a new turtle in the simulation
- `/kill` — removes a turtle from the simulation
- `/turtle1/set_pen` — changes the pen color or thickness
- `/turtle1/teleport_absolute` / `/teleport_relative` — instantly moves the turtle

---

## Notes: Nodes, Topics, and Services

**Nodes** are independent running programs in ROS 2. Each node performs a specific task such as controlling a robot, processing sensor data, or running a simulation. In this task, `/turtlesim` displays and controls the turtle, while `/teleop_turtle` handles keyboard input.

**Topics** are communication channels used for continuous data exchange between nodes. One node publishes data to a topic and other nodes subscribe to receive it. For example, `/turtle1/cmd_vel` is used to send movement commands to the turtle, and `/turtle1/pose` provides the turtle's real-time position.

**Services** are used for one-time request and response actions. Unlike topics, they do not continuously stream data — a node sends a single request and receives a single response. For example, `/clear` removes all drawings from the screen and `/reset` returns the turtle to its initial state.

---

## Talker and Listener Nodes

The talker node (`demo_nodes_cpp talker`) publishes "Hello World" messages continuously to a topic.

![Talker Node](talker_node_screenshot.png)

The listener node (`demo_nodes_py listener`) subscribes to that topic and prints every message it receives.

![Listener Node](listener_node_screenshot.png)

This demonstrates the basic **publish/subscribe** pattern in ROS 2.

---

## Manual Control (Teleop)

The turtle was controlled manually using keyboard input via the `teleop_turtle` node. Arrow keys move the turtle forward/backward and rotate it left/right.

![Manual Control](manual_control_screenshot.png)

---

## Drawing a Circle

### Command Used
```bash
ros2 topic pub --rate 10 /turtle1/cmd_vel geometry_msgs/msg/Twist "{linear: {x: 2.0}, angular: {z: 1.0}}"
```

![Circle Command](circle_command_screenshot.png)

![Circle Result](circle_screenshot.png)

### Why `--rate` is Used
The `--rate 10` flag publishes the command **10 times per second** continuously. Without it, the command would be sent only once (`--once`) and the turtle would stop immediately after a tiny movement. Continuous publishing at a fixed rate is what keeps the turtle moving in a smooth, sustained circle.

### Linear x / Angular z Logic
- **`linear.x`** controls forward speed — the higher the value, the faster the turtle moves forward
- **`angular.z`** controls rotation speed — a positive value turns left, negative turns right
- When both are set simultaneously (e.g., `linear.x: 2.0, angular.z: 1.0`), the turtle moves in a **circle**. The radius of the circle depends on the ratio: `radius = linear.x / angular.z`

---

## Drawing a Manual Star

### Commands Used

The star was drawn by alternating between moving forward and turning by a specific angle. A 5-pointed star requires turning **144°** (in radians: ~2.5 rad) between each point.

```bash
# Step 1 — Move forward
ros2 topic pub --once /turtle1/cmd_vel geometry_msgs/msg/Twist "{linear: {x: 4.0}, angular: {z: 0.0}}"

# Step 2 — Turn right 144°
ros2 topic pub --once /turtle1/cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.0}, angular: {z: -2.5}}"
```

Repeat the above two commands **5 times** to complete the star.

![Star Commands](commands_for_star_screenshot.png)

![Star Result](star_screenshot.png)

### Difference: Manual vs Teleop Movement

| | Teleop (`teleop_turtle`) | Terminal (`topic pub`) |
|---|---|---|
| Control method | Keyboard arrow keys | Terminal commands |
| Movement type | Real-time, continuous | One command at a time |
| Precision | Low — depends on human reaction | High — exact values specified |
| Use case | Quick exploration | Precise shapes and automation |

With **teleop**, movement is continuous as long as a key is held. With **terminal pub**, each command sends an exact velocity for one moment (`--once`) or at a fixed rate (`--rate`), giving full control over speed and angle.

---

## Demo Video

A short video demonstrating both keyboard control (teleop) and terminal control (topic pub), explaining the Linear x / Angular z logic, the `--rate` flag, and the difference between manual and teleop movement.

[Watch Demo Video](ros_task10-2026-05-11_01_47_50.mp4)
