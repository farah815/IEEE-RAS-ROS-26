import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Pose2D
from std_msgs.msg import Int32

SAFETY_ZONE_RADIUS = 2.0

ROBOT_PRIORITIES = {
    1: 3,
    2: 5,
    3: 1,
    4: 4,
}
ALL_ROBOT_IDS = list(ROBOT_PRIORITIES.keys())


class TrafficManager(Node):
    def __init__(self):
        super().__init__("traffic_manager")
        self.robots = {}

        for rid in ALL_ROBOT_IDS:
            self.robots[rid] = {"x": None, "y": None, "priority": None}
            self.create_subscription(
                Pose2D, f"/robot_{rid}/pose", self.make_pose_callback(rid), 10
            )
            self.create_subscription(
                Int32, f"/robot_{rid}/priority", self.make_priority_callback(rid), 10
            )

        self.create_timer(0.1, self.decision_loop)

    def make_pose_callback(self, rid):
        def callback(msg):
            self.robots[rid]["x"] = msg.x
            self.robots[rid]["y"] = msg.y
        return callback

    def make_priority_callback(self, rid):
        def callback(msg):
            self.robots[rid]["priority"] = msg.data
        return callback

    def decision_loop(self):
        lines = []
        lines.append("=" * 70)
        lines.append("               CENTRAL TRAFFIC MANAGER")
        lines.append("=" * 70)

        # ---- centralized nested-loop: compare every UNIQUE pair once ----
        # id2 always starts right after id1, so (1,2) is checked but not (2,1) again
        for i, id1 in enumerate(ALL_ROBOT_IDS):
            robot1 = self.robots[id1]
            if robot1["x"] is None or robot1["priority"] is None:
                continue

            for id2 in ALL_ROBOT_IDS[i + 1:]:
                robot2 = self.robots[id2]
                if robot2["x"] is None or robot2["priority"] is None:
                    continue

                dx = robot2["x"] - robot1["x"]
                dy = robot2["y"] - robot1["y"]
                distance = math.sqrt(dx * dx + dy * dy)

                pair_label = f"Robot {id1} vs Robot {id2} | distance={distance:.2f} m"

                if distance < SAFETY_ZONE_RADIUS:
                    # lower priority yields; equal priority -> lower id yields
                    if robot1["priority"] > robot2["priority"]:
                        winner, loser = id1, id2
                    elif robot2["priority"] > robot1["priority"]:
                        winner, loser = id2, id1
                    else:
                        winner, loser = id2, id1  # tie -> lower id (id1) yields

                    decision = (
                        f"{pair_label} | TOO CLOSE -> "
                        f"Robot {loser} (priority={self.robots[loser]['priority']}) "
                        f"YIELDS to Robot {winner} (priority={self.robots[winner]['priority']})"
                    )
                else:
                    decision = f"{pair_label} | SAFE -> both CLEAR"

                lines.append(decision)

        lines.append("=" * 70)

        # single print call -> no interleaving between cycles/threads
        print("\n".join(lines), flush=True)


def main(args=None):
    rclpy.init(args=args)
    node = TrafficManager()
    print("[traffic_manager] Centralized Traffic Manager Running")
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
