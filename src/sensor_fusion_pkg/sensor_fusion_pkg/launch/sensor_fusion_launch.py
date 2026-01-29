from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # IMU publisher node
        Node(
            package='sensor_fusion_pkg',
            executable='imu_data',
            name='imu_data_node',
            output='screen'
        ),

        # Depth publisher node
        Node(
            package='sensor_fusion_pkg',
            executable='depth_data',
            name='depth_node',
            output='screen'
        ),

        # Fused data subscriber/publisher node
        Node(
            package='sensor_fusion_pkg',
            executable='fused_data',
            name='fused_data_node',
            output='screen'
        ),
    ])
