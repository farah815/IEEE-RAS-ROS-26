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

        # Movement
        msg.twist.linear.x = 0.2
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
