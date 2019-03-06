#!/usr/bin/python

# Import a few system libraries that will be needed
from time import sleep
import sys, os

# This tells Python to look for additional libraries in the parent directory of this program
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Import the ev3dev specific library
from ev3dev.auto import *

#Connect motors
rightMotor = LargeMotor(OUTPUT_A)
leftMotor  = LargeMotor(OUTPUT_D)
clampMotor = MediumMotor(OUTPUT_C)
usMotor    = LargeMotor(OUTPUT_B)

# Connect touch sensors.
ts = TouchSensor();	assert ts.connected
cl = ColorSensor(); assert cl.connected
us = UltrasonicSensor(); assert us.connected
gs = GyroSensor(); assert gs.connected

gs.mode = 'GYRO-RATE'	# Changing the mode resets the gyro
gs.mode = 'GYRO-ANG'	# Set gyro mode to return compass angle

def run_motors(left, right, duration):
    leftMotor.run_direct(duty_cycle_sp=left)
    rightMotor.run_direct(duty_cycle_sp=right)

    while duration > 0:
        sleep(0.1)
        duration -= 0.1
        """
        if ts.value():
            raise Touch(-1)
        """
def gyro_reset():
    gs.mode = 'GYRO-RATE'
    gs.mode = 'GYRO-ANG'

def reverse():
    run_motors(-50, -50, 0.75)

def uTurn():
    gyro_reset()
    reverse()
    gyro_reset()    
    while gs.value() < 180:
        run_motors(20, -20, 0.1)
    gyro_reset()

def color_check():
    if cl.value() == 5 and ts.value() == 1:
        Sound.tone([(800, 200, 0),(1000, 200, 0),(1200, 500, 500)])
        uTurn() #once the robot detects the can, it will execute uTurn function which turns the robot around(clamp is mounted at the back)

run_motors(40,40,5)
color_check()
