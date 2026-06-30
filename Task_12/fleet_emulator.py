import rclpy
from rclpy.node import Node
from rclpy.executors import SingleThreadedExecutor
from rclpy.executors import ExternalShutdownException
from geometry_msgs.msg import Pose2D
from std_msgs.msg import Int32
import math
import threading

FLEET_CONFIG = [
    {"id": 1, "x": 0.0, "y": 0.0, "vx": 0.05, "vy": 0.02, "priority": 3},
    {"id": 2, "x": 5.0, "y": 3.0, "vx": -0.04, "vy": 0.03, "priority": 5},
    {"id": 3, "x": 2.0, "y": 7.0, "vx": 0.03, "vy": -0.05, "priority": 1},
    {"id": 4, "x": 8.0, "y": 1.0, "vx": -0.02, "vy": 0.04, "priority": 4},
]


class RobotEmulator(Node):
    def __init__(self, robot_cfg):
        node_name = f"robot_{robot_cfg['id']}_emulator"
        super().__init__(node_name)
        self.robot_id = robot_cfg["id"]
        self.x = robot_cfg["x"]
        self.y = robot_cfg["y"]
        self.vx = robot_cfg["vx"]
        self.vy = robot_cfg["vy"]
        self.priority = robot_cfg["priority"]

        pose_topic = f"/robot_{self.robot_id}/pose"
        priority_topic = f"/robot_{self.robot_id}/priority"

        self.pose_pub = self.create_publisher(Pose2D, pose_topic, 10)
        self.priority_pub = self.create_publisher(Int32, priority_topic, 10)

        self.create_timer(0.1, self.broadcast)

    def broadcast(self):
        self.x = (self.x + self.vx) % 10.0
        self.y = (self.y + self.vy) % 10.0

        pose_msg = Pose2D()
        pose_msg.x = self.x
        pose_msg.y = self.y
        pose_msg.theta = math.atan2(self.vy, self.vx)
        self.pose_pub.publish(pose_msg)

        prio_msg = Int32()
        prio_msg.data = self.priority
        self.priority_pub.publish(prio_msg)


def spin_node(node):
    executor = SingleThreadedExecutor()
    executor.add_node(node)
    try:
        executor.spin()
    except ExternalShutdownException:
        pass
    finally:
        executor.shutdown()


def main(args=None):
    rclpy.init(args=args)
    nodes = []
    threads = []

    for cfg in FLEET_CONFIG:
        node = RobotEmulator(cfg)
        nodes.append(node)
        t = threading.Thread(target=spin_node, args=(node,), daemon=True)
        t.start()
        threads.append(t)

    print("[fleet_emulator] All robots running.")

    try:
        for t in threads:
            t.join()
    except KeyboardInterrupt:
        pass
    finally:
        rclpy.shutdown()
        for node in nodes:
            node.destroy_node()


if __name__ == "__main__":
    main()
