import time
import numpy as np
import matplotlib.pyplot as plt
import pypot.dynamixel
from pypot.dynamixel import DxlIO

# Constants
WHEEL_BASE = 0.14  # distance between left and right wheels in meters
WHEEL_RADIUS = 0.026  # radius of the wheel in meters
dt = 0.1  # Time step in seconds

# Initialize robot position and orientation
x, y, theta = 0, 0, 0  # Start at the origin (0, 0)

# List to store the path points (x, y)
path_x = []
path_y = []

# Set up motors
ports = pypot.dynamixel.get_available_ports()

if not ports:
    exit('No port found')

# Initialize DxlIO with the first available port
dxl_io = pypot.dynamixel.DxlIO(ports[0])

# Assuming that wheel motors have IDs 1 and 2 (left and right wheels)
motor_ids = [1, 2]

# Continuously get motor speeds and update the robot's position
try:
    while True:
        # Get angular velocity from motors (in rad/s)
        speeds = dxl_io.get_present_speed(motor_ids)  # Returns list of speeds for each motor ID
        
        left_wheel_speed = speeds[0] * WHEEL_RADIUS  # Convert to linear speed (m/s)
        right_wheel_speed = speeds[1] * WHEEL_RADIUS  # Convert to linear speed (m/s)
        
        # Differential drive kinematics
        v = (right_wheel_speed + left_wheel_speed) / 2  # Linear velocity
        omega = (right_wheel_speed - left_wheel_speed) / WHEEL_BASE  # Angular velocity
        
        # Update pose (x, y, theta) using the kinematic model
        theta += omega * dt
        x += v * np.cos(theta) * dt
        y += v * np.sin(theta) * dt
        
        # Store the (x, y) position for later plotting
        path_x.append(x)
        path_y.append(y)
        
        # Check for user input to stop the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        # Wait for the next time step
        time.sleep(dt)
except KeyboardInterrupt:
    # If interrupted by keyboard, we stop the loop
    pass

# Plot the path using matplotlib
plt.figure()
plt.plot(path_x, path_y, marker='o', color='r')
plt.title("Robot Path")
plt.xlabel("X Position (m)")
plt.ylabel("Y Position (m)")
plt.grid(True)
plt.axis('equal')  # To keep aspect ratio equal
plt.show()

# Cleanup
dxl_io.close()
