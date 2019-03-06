#!/usr/bin/python

# Import a few system libraries that will be needed
from time import sleep
import sys, os

# This tells Python to look for additional libraries in the parent directory of this program
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Import the ev3dev specific library
from ev3dev.auto import *

#Connect motors
usMotor    = LargeMotor(OUTPUT_B)

def rotateSensor(duration, direction):
    usMotor.run_direct(duty_cycle_sp=direction)
    while duration > 0:
        sleep(0.1)
        duration -= 0.1
    usMotor.stop(stop_command='brake')

rotateSensor(0.63, 40)
sleep(5)
rotateSensor(0.63, -40)
