import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TwistStamped


class AutonomousMover(Node):

    def __init__(self):
        super().__init__('autonomous_mover')

        self.publisher = self.create_publisher(
            TwistStamped,
            '/cmd_vel',
            10
        )

        # Save start time
        self.start_time = self.get_clock().now()

        # Timer runs every 0.1 s
        self.timer = self.create_timer(
            0.1,
            self.move_robot
        )

        self.get_logger().info('Autonomous mover started')

    def move_robot(self):

        msg = TwistStamped()

        # Header
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = ''

        # Time since start
        elapsed = (
            self.get_clock().now() - self.start_time
        ).nanoseconds / 1e9

        # 1. Forward 2 m (10 s)
        if elapsed < 10.0:
            msg.twist.linear.x = 0.2
            msg.twist.angular.z = 0.0

        # 2. Turn left 90° (3.14 s)
        elif elapsed < 13.14:
            msg.twist.linear.x = 0.0
            msg.twist.angular.z = 1.2

        # 3. Forward 8 m (40 s)
        elif elapsed < 45:
            msg.twist.linear.x = 0.2
            msg.twist.angular.z = 0.0

        # 4. Turn right 90° (3.14 s)
        elif elapsed < 65:
            msg.twist.linear.x = 0.0
            msg.twist.angular.z = -0.5

        # 5. Forward 2 m (10 s)
        elif elapsed < 80:
            msg.twist.linear.x = -0.2
            msg.twist.angular.z = 0.0

        # 6. Turn left 90° (3.14 s)
        elif elapsed < 100:
            msg.twist.linear.x = 0.0
            msg.twist.angular.z = 0.5

        # 7. Forward 1 m (5 s)
        elif elapsed < 120:
            msg.twist.linear.x = 0.2
            msg.twist.angular.z = 0.0

        # 8. Stop
        else:
            msg.twist.linear.x = 0.0
            msg.twist.angular.z = 0.0

        self.publisher.publish(msg)


def main(args=None):

    rclpy.init(args=args)

    node = AutonomousMover()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
