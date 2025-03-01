import numpy as np
from ackermann_msgs.msg import AckermannDriveStamped

class WallFollower:
    LOOKAHEAD_DISTANCE = 1.0  # Default lookahead distance
    THETA = np.radians(30)  # Angle between beams
    FRONT_LOOKAHEAD_ANGLE = np.radians(55)  # Angle for detecting dead-ends
    DEAD_END_THRESHOLD = 1.0  # Distance threshold for detecting dead-ends

    def __init__(self, drive_publisher):
        """
        Initializes the WallFollower class.

        Args:
            drive_publisher: ROS publisher for AckermannDrive messages
        """
        # PID coefficients
        self.kp = 0.5
        self.ki = 0.01
        self.kd = 0.1

        # PID state
        self.integral = 0.0
        self.prev_error = 0.0

        # Lookahead configuration
        self.lookahead_distance = self.LOOKAHEAD_DISTANCE

        # ROS publisher
        self.drive_publisher = drive_publisher

    def get_error(self, range_data, desired_distance):
        """
        Computes the error in lateral distance to the wall.

        Args:
            range_data: LiDAR range readings
            desired_distance: Desired distance from the wall

        Returns:
            Tuple (error, dead_end_detected)
        """
        beam_at_theta = self.get_range(range_data, np.pi / 2 - self.THETA)
        perpendicular_beam = self.get_range(range_data, np.pi / 2)

        # Handle edge cases where LiDAR readings are invalid (e.g., zero readings)
        if beam_at_theta == 0 or perpendicular_beam == 0:
            return 0.0, False  

        # Compute the wall angle (alpha)
        alpha = np.arctan2(
            beam_at_theta * np.cos(self.THETA) - perpendicular_beam,
            beam_at_theta * np.sin(self.THETA)
        )

        # Compute the current lateral distance to the wall
        current_wall_dist = perpendicular_beam * np.cos(alpha)

        # Adjust lookahead dynamically based on the perpendicular distance
        lookahead = self.lookahead_distance * (0.5 if perpendicular_beam > 3.0 else 1.0)

        # Predict the future lateral distance to the wall
        predicted_wall_dist = current_wall_dist + lookahead * np.sin(alpha)

        # Compute the final error
        error = predicted_wall_dist - desired_distance

        # **Dead-end detection**
        front_distance = self.get_range(range_data, self.FRONT_LOOKAHEAD_ANGLE)
        dead_end_detected = front_distance < self.DEAD_END_THRESHOLD

        return error, dead_end_detected

    def pid_control(self, error, velocity):
        """
        Computes the steering angle using a PID controller and publishes the drive command.

        Args:
            error (float): The calculated wall-following error
            velocity (float): Desired vehicle velocity

        Returns:
            None
        """
        # **Integral Windup Prevention**: Gradually decay integral error
        if abs(error) < 0.05:
            self.integral *= 0.9  
        else:
            self.integral += error

        # Compute derivative term
        derivative = error - self.prev_error
        self.prev_error = error

        # **Compute Steering Angle (PID output)**
        damping_factor = 0.85  # Damps excessive steering oscillations
        steering_angle = (self.kp * error + self.ki * self.integral + self.kd * derivative) * damping_factor

        # **Publish Drive Message**
        if self.drive_publisher is not None:
            drive_msg = AckermannDriveStamped()
            drive_msg.drive.speed = velocity
            drive_msg.drive.steering_angle = steering_angle
            self.drive_publisher.publish(drive_msg)
        else:
            print("Warning: Drive publisher not initialized!")

    def get_range(self, range_data, angle):
        """
        Retrieves the LiDAR reading at a specified angle.

        Args:
            range_data: LiDAR scan data
            angle (float): Angle in radians

        Returns:
            Distance at the given angle
        """
        index = int(angle * len(range_data) / (2 * np.pi))  # Convert angle to LiDAR index
        return range_data[index] if 0 <= index < len(range_data) else 0.0
