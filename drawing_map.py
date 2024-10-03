import time
import numpy as np
import cv2
import pypot.dynamixel
from pypot.dynamixel import DxlIO
# Constants
WHEEL_BASE = 0.14  # distance between left and right wheels in meters
WHEEL_RADIUS = 0.026  # radius of the wheel in meters
IMG_SIZE = (800, 800)  # Size of the image to visualize path
dt = 0.1  # Time step in seconds

# Initialize robot position and orientation
x, y, theta = IMG_SIZE[0] // 2, IMG_SIZE[1] // 2, 0  # Starting at the center of the image

# Initialize OpenCV image to draw the path
image = np.ones((IMG_SIZE[1], IMG_SIZE[0], 3), dtype=np.uint8) * 255

# Set up motors
ports = pypot.dynamixel.get_available_ports()

if not ports:
    exit('No port found')

# Initialize DxlIO with the first available port
dxl_io = pypot.dynamixel.DxlIO(ports[0])


# Assuming that wheel motors have IDs 1 and 2 (left and right wheels)
motor_ids = [1, 2]
# Continuously get motor speeds and update the robot's positiona
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
    
    # Convert x, y to integer values for drawing
    x_int, y_int = int(x), int(y)
    
    # Draw the current position as a dot on the image
    cv2.circle(image, (x_int, y_int), 2, (0, 0, 255), -1)
    
    
    # Check for user input to stop the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    # Wait for the next time step
    time.sleep(dt)

# Save 
cv2.imwrite("robot_path",image)
# Cleanup
cv2.destroyAllWindows()

