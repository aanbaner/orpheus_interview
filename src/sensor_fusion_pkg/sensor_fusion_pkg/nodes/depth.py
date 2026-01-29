import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
import time

class DepthNode(Node):
    def __init__(self):
        super().__init__('depth_node')
        self.get_logger().info('Starting Depth node')
        self.publisher_ = self.create_publisher(Float32, '/depth', 10)
        self.timer = self.create_timer(0.5, self.publish_data) # arbitrary publish rate: 2Hz

    def publish_data(self):
        # construct and populate a float32 message
        msg = Float32()

        # dummy data assuming constant acceleration of 10.0 and initial conditions of pos=0 vel=0
        depth = 10.0 * (time.time() ** 2)
        
        self.publisher_.publish(msg)
        self.get_logger().info(f'depth reads: {msg.data}')

def main(args=None):
    rclpy.init(args=args)
    node = DepthNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()