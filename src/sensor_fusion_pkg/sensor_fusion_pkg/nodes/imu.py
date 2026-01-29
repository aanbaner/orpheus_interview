import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu
from std_msgs.msg import Header

class ImuDataNode(Node):
    def __init__(self):
        super().__init__('imu_data_node')
        self.get_logger().info('Starting IMU Data node')
        self.publisher_ = self.create_publisher(Imu, '/imu/data', 10)
        self.timer = self.create_timer(0.1, self.publish_data) # arbitrary publish rate: 10Hz

    def publish_data(self):
        # construct and populate an IMU message
        msg = Imu()
        msg.header = Header()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'imu_link'

        # dummy data

        # quaternion producing the identity DCM
        msg.orientation.w = 1.0
        msg.orientation.x = 0.0
        msg.orientation.y = 0.0
        msg.orientation.z = 0.0

        # let's assume gyros and mag read \vec{\omega} = \vec{0}
        msg.angular_velocity.x = 0.0
        msg.angular_velocity.y = 0.0
        msg.angular_velocity.z = 0.0

        # assume we are experiencing a constant force in the z (depth) axis
        msg.linear_acceleration.x = 0.0
        msg.linear_acceleration.y = 0.0
        msg.linear_acceleration.z = 10.0

        self.publisher_.publish(msg)
        self.get_logger().info(f'z-axis accel reads: {msg.linear_acceleration.z}')

def main(args=None):
    rclpy.init(args=args)
    node = ImuDataNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()