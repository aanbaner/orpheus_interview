# HOW TO RUN

#### Start Docker Container

```bash
docker run -it -v /ros2_ws:/ros2_ws ros2-humble
```

### Build and Set Source

```bash
cd /ros2_ws
colcon build
source install/setup.bash
```

### Run
```bash
ros2 launch sensor_fusion_pkg sensor_fusion_launch.py
```

### Inspect messages
```bash
ros2 topic echo /imu/data
ros2 topic echo /depth
ros2 topic echo /vertical_velocity
```

You should see that `/vertical_velocity` steadily climbs as the estimator converges on the constant acceleration infromation baked into the dummy data in `imu.py` and `depth.py`