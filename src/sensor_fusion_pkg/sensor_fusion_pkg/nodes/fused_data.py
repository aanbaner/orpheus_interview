import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu
from std_msgs.msg import Float32

class FusedDataNode(Node):
    def __init__(self): 
        super().__init__('fused_data_node')
        self.get_logger().info('Starting Fused Data Node')
        self.imu_sub = self.create_subscription(Imu, '/imu/data', self.get_imu_data, 10)
        self.depth_sub = self.create_subscription(Float32, '/depth', self.get_depth_data, 10)
        self.publisher_ = self.create_publisher(Float32, '/vertical_velocity', 10)

        # estimator dT
        self.est_dt = 0.05
        self.timer = self.create_timer(0.05, self.estimate_pub) # run faster than the sensors

        # estimator gains
        self.k_accel_to_acc = 0.8 # we mostly trust the accel
        self.k_accel_to_vel = 0.1 # let the propagate velocity dominate
        self.k_accel_to_pos = 0.00001 # barely any effect 

        self.k_depth_to_acc = 0.001 # some trust to correct old accel drifts
        self.k_depth_to_vel = 0.22 # let the depth measurement discipline velocity with more authority than accels
        self.k_depth_to_pos = 0.6 # trust over the model slightly

        # estimator state initial conditions
        self.pos_hat = 0.0
        self.vel_hat = 0.0
        self.acc_hat = 0.0

        # initialize data for our estimator
        self.imu_data = Imu()
        self.depth_data = Float32()


    def get_imu_data(self, msg):
        self.imu_data = msg
        self.get_logger().info(f'Received IMU data: {msg.linear_acceleration.z}')
    
    def get_depth_data(self, msg):
        self.depth_data = msg
        self.get_logger().info(f'Received depth data: {msg.data}')

    def estimate_pub(self):
        msg = Float32()

        # get state measurement data from sensor msgs:
        accel_z_acc = self.imu_data.linear_acceleration.z
        depth_z_pos = self.depth_data.data

        # estimator
        
        # get errors
        accel_err = accel_z_acc - self.acc_hat
        depth_err = depth_z_pos - self.pos_hat

        # propagate internal dynamics model (A * x propagations)
        self.pos_hat += self.vel_hat * self.est_dt
        self.vel_hat += self.acc_hat * self.est_dt
        self.acc_hat = self.acc_hat

        # propagate error corrections (K * err propagations)
        self.acc_hat += (self.k_accel_to_acc * accel_err) + (self.k_depth_to_acc * depth_err) 
        self.vel_hat += (self.k_accel_to_vel * accel_err) + (self.k_depth_to_vel * depth_err) 
        self.pos_hat += (self.k_accel_to_pos * accel_err) + (self.k_depth_to_pos * depth_err)

        # populate message
        msg.data = self.vel_hat

        # publish velocity
        self.publisher_.publish(msg)
        self.get_logger().info(f'Published vertical velocity estimate: {self.vel_hat}')

def main(args=None):
    rclpy.init(args=args)
    node = FusedDataNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()