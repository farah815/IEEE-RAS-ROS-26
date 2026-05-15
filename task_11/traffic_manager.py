import math
import rclpy
from rclpy.node import Node
from rclpy.executors import ExternalShutdownException
from geometry_msgs.msg import Pose2D
from std_msgs.msg import Int32

MY_ROBOT_ID        = 1
MY_PRIORITY        = 3
SAFETY_ZONE_RADIUS = 2.0
FLEET_IDS          = [2, 3, 4]


class TrafficManager(Node):

    def __init__(self):
        super().__init__("traffic_manager")

        self.my_x = 0.0
        self.my_y = 0.0

        self.fleet = {rid: {"x": None, "y": None, "priority": None}
                      for rid in FLEET_IDS}

        self.create_subscription(
            Pose2D,
            f"/robot_{MY_ROBOT_ID}/pose",
            self._own_pose_cb,
            10,
        )

        for rid in FLEET_IDS:
            self.create_subscription(
                Pose2D,
                f"/robot_{rid}/pose",
                self._make_pose_cb(rid),
                10,
            )
            self.create_subscription(
                Int32,
                f"/robot_{rid}/priority",
                self._make_priority_cb(rid),
                10,
            )

        self.create_timer(0.1, self._decision_loop)

    def _make_pose_cb(self, rid):
        def cb(msg):
            self.fleet[rid]["x"] = msg.x
            self.fleet[rid]["y"] = msg.y
        return cb

    def _make_priority_cb(self, rid):
        def cb(msg):
            self.fleet[rid]["priority"] = msg.data
        return cb

    def _own_pose_cb(self, msg):
        self.my_x = msg.x
        self.my_y = msg.y

    def _decision_loop(self):
        danger_detected = False
        log_lines = []

        for rid, data in self.fleet.items():
            if data["x"] is None or data["priority"] is None:
                continue

            dx       = data["x"] - self.my_x
            dy       = data["y"] - self.my_y
            distance = math.sqrt(dx ** 2 + dy ** 2)

            in_zone         = distance < SAFETY_ZONE_RADIUS
            higher_priority = data["priority"] > MY_PRIORITY

            if in_zone and higher_priority:
                danger_detected = True
                log_lines.append(
                    f"   Robot {rid} | dist={distance:.2f} m | "
                    f"priority={data['priority']} > mine={MY_PRIORITY}  "
                )
            else:
                status = "in zone, lower priority" if in_zone else f"dist={distance:.2f} m"
                log_lines.append(
                    f"    Robot {rid} | {status} | priority={data['priority']}"
                )

        separator = "─" * 52
        tag = "[DANGER!]  YIELD REQUIRED" if danger_detected else "[CLEAR]   PATH IS CLEAR"

        print(separator)
        print(f"  Self  :pos=({self.my_x:.2f}, {self.my_y:.2f})  priority={MY_PRIORITY}")
        for line in log_lines:
            print(line)
        print(f"  STATUS: {tag}")
        print(separator)


def main(args=None):
    rclpy.init(args=args)
    node = TrafficManager()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()

