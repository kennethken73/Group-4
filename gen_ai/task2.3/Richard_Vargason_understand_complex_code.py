import numpy as np
from ackermann_msgs.msg import AckermannDriveStamped

class WallFollower:
    LOOKAHEAD_DISTANCE = 1.0  # Default lookahead distance
    THETA = np.radians(30)  # Angle between beams
    FRONT_LOOKAHEAD_ANGLE = np.radians(55)  # Front lookahead for dead-end detection
    DEAD_END_THRESHOLD = 1.0  # Distance threshold for detecting dead-ends

    def __init__(self):
        self.kp = 0.5
        self.ki = 0.01
        self.kd = 0.1
        self.integral = 0.0
        self.prev_error = 0.0
        self.lookahead_distance = self.LOOKAHEAD_DISTANCE
        self.drive_publisher = None  # To be initialized outside

    def get_error(self, range_data, desired_distance):
        """
        Calculates the lateral error to the wall using LiDAR data.

        Args:
            range_data: LiDAR range readings
            desired_distance: Target distance to the wall

        Returns:
            error (float): Distance error for PID correction
            dead_end_detected (bool): True if a dead-end is detected
        """
        beam_at_theta = self.get_range(range_data, np.pi / 2 - self.THETA)
        perpendicular_beam = self.get_range(range_data, np.pi / 2)

        if beam_at_theta == 0 or perpendicular_beam == 0:
            return 0.0, False  # Prevent errors in case of faulty readings

        alpha = np.arctan2(
            beam_at_theta * np.cos(self.THETA) - perpendicular_beam,
            beam_at_theta * np.sin(self.THETA)
        )
        current_wall_dist = perpendicular_beam * np.cos(alpha)

        # Dynamically adjust lookahead distance in turns
        lookahead = self.lookahead_distance * (0.5 if perpendicular_beam > 3.0 else 1.0)
        predicted_wall_dist = current_wall_dist + lookahead * np.sin(alpha)

        error = predicted_wall_dist - desired_distance

        # **Detect obstacles in front**
        front_distance = self.get_range(range_data, self.FRONT_LOOKAHEAD_ANGLE)
        dead_end_detected = front_distance < self.DEAD_END_THRESHOLD

        return error, dead_end_detected

    def pid_control(self, error, velocity):
        """
        Applies PID control to calculate the steering angle based on the error.

        Args:
            error (float): Wall-following error
            velocity (float): Desired velocity

        Returns:
            None
        """
        # Exponential decay for integral windup
        if abs(error) < 0.05:
            self.integral *= 0.9  # Gradually decay instead of resetting to zero

        self.integral += error
        derivative = error - self.prev_error
        self.prev_error = error

        damping_factor = 0.85  # Reduce excessive steering oscillations
        steering_angle = (self.kp * error + self.ki * self.integral + self.kd * derivative) * damping_factor

        # Publish drive message
        drive_msg = AckermannDriveStamped()
        drive_msg.drive.speed = velocity
        drive_msg.drive.steering_angle = steering_angle
        self.drive_publisher.publish(drive_msg)