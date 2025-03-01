# ROS2 Safety Node for F1Tenth Vehicle

## Overview
The **SafetyNode** is a ROS2 node designed to monitor the vehicle's surroundings using LiDAR data and execute emergency braking if an imminent collision is detected. The node subscribes to **LaserScan** messages to assess obstacles in front of the vehicle and to **Odometry** messages to determine its current speed. If the calculated **Time-To-Collision (TTC)** is below a defined threshold, the node will publish a braking command.

---

## Node Functionality
### Subscribed Topics
- **`/scan` (sensor_msgs/LaserScan)**: Provides distance readings (ranges) at different angles around the vehicle.
- **`/ego_racecar/odom` (nav_msgs/Odometry)**: Supplies the current velocity of the vehicle.

### Published Topics
- **`/drive` (ackermann_msgs/AckermannDriveStamped)**: Controls the vehicle’s speed. If a collision is detected, a braking command is published to stop the vehicle.

### Parameters
- **`mode`** (`string`, default: `sim`) – Defines the operating mode (e.g., simulation or real-world operation).
- **`ttc`** (`double`, default: `2.0`) – Sets the time-to-collision threshold (in seconds) before braking is triggered.
- **`student`** (`string`, default: `richard`) – A placeholder parameter that does not affect functionality.

---

## Understanding LaserScan and TTC Calculation
### LaserScan Data
The **LaserScan** message provides:
- **Ranges**: A list of distances from the LiDAR sensor to obstacles.
- **Angles**: Defined by `angle_min` (starting angle) and `angle_increment` (angle difference between measurements).

The vehicle receives a **sweep of distance values**, where each index in `ranges` corresponds to an angle in the sensor's field of view.

### Time-To-Collision (TTC) Calculation
To determine **TTC**, the following steps are performed:
1. **Convert the scan ranges into a NumPy array**, replacing invalid (NaN, Inf) values with `np.inf`.
2. **Compute the angles** of each beam using:
   
   ```python
   angles = angle_min + np.arange(len(ranges)) * angle_increment
   ```
   
3. **Compute range rates** based on the vehicle’s speed and angle:
   
   ```python
   range_rates = -self.speed * np.cos(angles)
   ```
   
   - This estimates how quickly the vehicle is approaching each detected obstacle.
   - Negative `range_rates` mean the vehicle is moving **towards** an obstacle.
   
4. **Compute individual TTC values**:
   
   ```python
   ittc = ranges / np.maximum(-range_rates, 1e-6)
   ```
   
   - `ranges` is the obstacle distance.
   - `-range_rates` is the closing speed to the obstacle.
   - A small epsilon `1e-6` is used to avoid division by zero.
   
5. **Trigger braking if any TTC is below the threshold (`ttc_threshold`)**:
   
   ```python
   if np.any(ittc < self.ttc_threshold):
       self.get_logger().warn("Collision imminent! Applying brakes.")
       self.brake()
   ```

---

## Code Breakdown
### 1. **Initialization (`__init__`)**
- Declares parameters and sets up **subscribers** and **publishers**.
- Stores initial speed (`self.speed = 0.0`).
- Logs the current mode and TTC threshold.

### 2. **Odometry Callback (`odom_callback`)**
- Updates the vehicle’s speed based on the odometry message:
  
  ```python
  self.speed = odom_msg.twist.twist.linear.x
  ```

### 3. **LaserScan Callback (`scan_callback`)**
- Retrieves **distance readings** (`ranges`) and **angles**.
- Computes **time-to-collision** (`ittc`) for each beam.
- If any **TTC** is **too low**, the node triggers emergency braking.

### 4. **Braking Command (`brake`)**
- Creates a `AckermannDriveStamped` message with `speed = 0.0`.
- Publishes the command to `/drive`, stopping the vehicle.

### 5. **Main Function (`main`)**
- Initializes the node and starts the ROS2 event loop with `rclpy.spin()`.
- Gracefully shuts down the node when stopped.

---

## Summary
- This node **monitors the vehicle’s surroundings** using a **LiDAR sensor**.
- It **computes TTC** to detect potential collisions based on speed and obstacle distances.
- If a **collision is imminent**, it **publishes a braking command** to stop the vehicle.
- The **TTC threshold** can be adjusted to fine-tune the emergency braking behavior.

This system is crucial for **collision prevention** in autonomous racing and robotics applications, ensuring the vehicle reacts in time to avoid obstacles in its path.