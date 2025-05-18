# Screesaver Movement Script
# This program is a screensaver-esque movement script for the EV3 robot.
# It uses the EV3 brick, motors, ultrasonic sensor, and color sensors to navigate and avoid obstacles.
# The screensaver nomenclature is used to describe the robot's movement pattern, which is similar to a screensaver on a computer.
# The robot begins by turning to 45 degrees, then moves forward in a zigzag pattern, turning at 90-degree angles.
# The robot also uses the ultrasonic sensor to detect obstacles or color sensors to detect borders and avoid them by turning away.
# The robot's movement is controlled by the DriveBase class, which allows for easy control of the robot's motors and movement.
# The forward colour sensor is used to detect the color of the block the robot is approaching, helping it differentiate targets and obstacles,
# While the downward color sensor is used to detect the color of the surface below the robot.


# IMPORT LIBRARIES
# This program is a screensaver-esque movement script for the EV3 robot.
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, UltrasonicSensor, ColorSensor
from pybricks.parameters import Port, Stop, Color
from pybricks.robotics import DriveBase
from pybricks.tools import wait
import time


# Initialize the EV3 brick and motors.
ev3 = EV3Brick()
L_servo = Motor(Port.B)
R_servo = Motor(Port.C)
LiftArm = Motor(Port.A)


# Initialize the ultrasonic sensor and color sensors.
Obs = UltrasonicSensor(Port.S4)
ColFwd = ColorSensor(Port.S1)
ColDown = ColorSensor(Port.S2)


# Initialize the robot's drive base with the left and right motors, wheel diameter, and axle track.
robot = DriveBase(L_servo, R_servo, wheel_diameter=55.5, axle_track=104)


# Define Functions


def TargetAlignment():
                # Align the robot with the block based on reflection intensity.
                # Account for ambient lighting by calibrating the reflection thresholds.
                ambient_light = ColFwd.ambient()  # Measure ambient light intensity in percentage (0-100%).
                target_low = ambient_light + 5  # Adjust threshold for lower bound.
                target_high = ambient_light + 15  # Adjust threshold for upper bound.


                # Fine-tune alignment with small incremental turns.
                while not (target_low <= ColFwd.reflection() <= target_high):
                    if ColFwd.reflection() < target_low:
                        robot.turn(0.5)  # Small turn to align with the block.
                    elif ColFwd.reflection() > target_high:
                        robot.turn(-0.5)  # Small turn in the opposite direction.


def screensaver():
    master = Obs.distance() > 50
    # Set the initial heading to 45 degrees.
    hdg = 45
    # Turn the robot to the initial heading.
    robot.turn(hdg)
    # Move forward in a zigzag pattern, turning at 90-degree angles.
    while not master:
        robot.straight(1)
   
    if master:
        if ColFwd.color() == Color.RED or ColFwd.color() == Color.GREEN or ColFwd.color() == Color.BLUE or ColFwd.color() == Color.YELLOW:
            # If the forward color sensor detects a  target colour, recognise it, align the robot, and move forward to intercept the target.
            # Signal that a target color has been detected.
            ev3.speaker.beep(1000, 500)  # High-pitched beep for 0.5 seconds.
            TargetAlignment()
            ev3.speaker.beep(500, 500)  # Low-pitched beep for 0.5 seconds.
            robot.straight(47)
            LiftArm.run_angle(100, 90, Stop.HOLD, False)  # Lift the arm to pick up the block.
           
       

