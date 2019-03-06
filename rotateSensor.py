#!/usr/bin/python

# Import a few system libraries that will be needed
from time import sleep
import sys, os

# This tells Python to look for additional libraries in the parent directory of this program
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Import the ev3dev specific library
from ev3dev.auto import *

usMotor = LargeMotor(OUTPUT_B)
def rotateSensor(duration):
    usMotor.run_direct(duty_cycle_sp=-40)
    while duration > 0:
        sleep(0.1)
        duration -= 0.1
Leds.set_color(Leds.LEFT, Leds.YELLOW)
Leds.set_color(Leds.RIGHT, Leds.YELLOW)
rotateSensor(0.35)
Leds.set_color(Leds.LEFT, Leds.GREEN)
Leds.set_color(Leds.RIGHT, Leds.GREEN)
