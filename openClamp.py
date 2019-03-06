#!/usr/bin/python

# Import a few system libraries that will be needed
from time import sleep
import sys, os

# This tells Python to look for additional libraries in the parent directory of this program
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Import the ev3dev specific library
from ev3dev.auto import *

clampMotor = MediumMotor(OUTPUT_C)
def closeClamp(duration):
    clampMotor.run_direct(duty_cycle_sp=-75)
    while duration > 0:
        sleep(0.1)
        duration -= 0.1

def openClamp(duration):
    clampMotor.run_direct(duty_cycle_sp=75)
    while duration > 0:
        sleep(0.1)
        duration -= 0.1

openClamp(1)
#closeClamp(0.2)
