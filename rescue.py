#!/usr/bin/python

# Import a few system libraries that will be needed
from time import sleep
import sys, os

# This tells Python to look for additional libraries in the parent directory of this program
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Import the ev3dev specific library
from ev3dev.auto import *

class Colour(Exception):
    def __init__(self, which_side):
        self.value = which_side

class ButtonPress(Exception):
    def __init__(self, message):
        self.message = message

#Connect motors
rightMotor = LargeMotor(OUTPUT_A)
leftMotor  = LargeMotor(OUTPUT_D)
clampMotor = MediumMotor(OUTPUT_C)
usMotor    = LargeMotor(OUTPUT_B)

# Connect touch sensors.
us1 = UltrasonicSensor(INPUT_1); assert us1.connected
us4 = UltrasonicSensor(INPUT_4); assert us4.connected
cl = ColorSensor(); assert cl.connected
gs = GyroSensor(); assert gs.connected

gs.mode = 'GYRO-RATE'   # Changing the mode resets the gyro
gs.mode = 'GYRO-ANG'    # Set gyro mode to return compass angle

cl.mode = 'COL-COLOR'

# We will need to check EV3 buttons state.
btn = Button()

def run_motors(left, right, duration):
    leftMotor.run_direct(duty_cycle_sp=left)
    rightMotor.run_direct(duty_cycle_sp=right)

    while duration > 0:
        sleep(0.1)
        duration -= 0.1
            
        if btn.any():
            raise ButtonPress("Stop robot")
        """
        if ts.value():
            raise Touch(-1)
        """

def lights_green():
    Leds.set_color(Leds.LEFT, Leds.GREEN)
    Leds.set_color(Leds.RIGHT, Leds.GREEN)

def lights_yellow():
    Leds.set_color(Leds.LEFT, Leds.YELLOW)
    Leds.set_color(Leds.RIGHT, Leds.YELLOW)

def lights_red():
    Leds.set_color(Leds.LEFT, Leds.RED)
    Leds.set_color(Leds.RIGHT, Leds.RED)

def gyro_correct():
    gyro_reset()
    if gs.value() < -5:
        run_motors(30, 75, 0.25)
    elif gs.value() > 5:
        run_motors(75, 30, 0.25)
    stop()
        
def gyro_reset():
    gs.mode = 'GYRO-RATE'
    gs.mode = 'GYRO-ANG'

# turn_left/right functions using the gyro sensor
# start here

def turn_left():
    lights_yellow()
    run_motors(50, 50, 0.25)
    while gs.value() >= -90:
        run_motors(-30, 30, 0.1)
        if cl.value() == 5 and count == 0:
            Sound.tone([(800, 200, 0),(1000, 200, 0),(1200, 500, 500)])
            runClamp(1.2)
            rotateSensor(0.55, -40)
            exitMaze()
    run_motors(75, 75, 1.0)
    gyro_reset()

def turn_right():
    lights_yellow()
    run_motors(50, 50, 0.25)
    while gs.value() <= 90:
        run_motors(30,-30,0.1)
        if cl.value() == 5 and count == 0:
            Sound.tone([(800, 200, 0),(1000, 200, 0),(1200, 500, 500)])
            runClamp(1.2)
            rotateSensor(0.55, -40)
            exitMaze()
    run_motors(75, 75, 1.0)
    gyro_reset()

# end here

def reverse():
    lights_red()
    run_motors(-50, -50, 0.25)
    stop()

def uTurn():
    lights_yellow()
    gyro_reset()
    run_motors(-35, -35, 1)
    while gs.value() < 180:
        run_motors(40, -40, 0.1)
    stop()

def runClamp(duration):
    clampMotor.run_direct(duty_cycle_sp=-75)
    while duration > 0:
        sleep(0.1)
        duration -= 0.1
    clampMotor.stop(stop_command='brake')

def rotateSensor(duration, direction):
    usMotor.run_direct(duty_cycle_sp=direction)
    while duration > 0:
        sleep(0.1)
        duration -= 0.1
    usMotor.stop(stop_command='brake')

def exitMaze():
    while True:
        try:
            lights_green
            if us1.value() <= 350:
                if us4.value() <= 25:
                    stop()
                    reverse()
                    rotateSensor(0.6, 40)
                    sleep(1)
                    if us1.value() <= 350:
                        rotateSensor(0.6, -40)
                        uTurn() #if we can't uTurn just reverse out
                    else:
                        rotateSensor(0.6 , -40)
                        turn_right()
                else:
                    lights_green()
                    run_motors(50, 50, 0.5)
                    gyro_correct()
            else:
                turn_left()

        except ButtonPress:
            stop()
            sys.exit()
    stop()

def stop():
    # Stop both motors
    leftMotor.stop(stop_command='brake')  
    rightMotor.stop(stop_command='brake')
    lights_green()
    
""" 
def backup(dir):
    # Sound backup alarm.
    Sound.tone([(1000, 500, 500)] * 3)

    # Turn backup lights on:
    lights_red()

    try:
        # Stop both motors and reverse for 1.5 seconds
        # then turn the wheels in opposite directions for 0.25 seconds
        run_motors(-50, -50, 1.5)
        run_motors(dir*75, -dir*75, 0.25)
    except ButtonPress:
        stop()
        sys.exit()
"""

# Run the robot

# ------------------------------------------------
# MAIN PROGRAM BEGINS HERE
# ------------------------------------------------

# Set the lights to green when the program begins
lights_green()

while not btn.any():
    pass

count = 0
while True:
    try:
        lights_green
        if us1.value() <= 350:
            if cl.value() == 5 and count == 0:
                count +=1
                Sound.tone([(800, 200, 0),(1000, 200, 0),(1200, 500, 500)])
                runClamp(2.5)
                uTurn()
                rotateSensor(0.6, -40)
            elif count == 1:
                exitMaze()
            elif us4.value() <= 25 and count == 0:
                stop()
                reverse()
                rotateSensor(0.6, -40)
                sleep(1)
                if us1.value() <= 350:
                    rotateSensor(0.6, 40)
                    uTurn() #if we can't uTurn just reverse out
                else:
                    rotateSensor(0.6, 40)
                    turn_left()
            else:
                lights_green()
                run_motors(50, 50, 0.5)
                gyro_correct()
        else:
            turn_right()

    except ButtonPress:
        stop()
        sys.exit()

# Stop the motors before exiting.
stop()
