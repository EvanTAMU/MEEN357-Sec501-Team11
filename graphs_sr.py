# ALMOST the exact same as graphs_motor.py, but utilizes the values from the speed reducer
# NOT VALUES FROM THE SHAFT!

import numpy as np
import matplotlib.pyplot as plt

from graphs_motor import graph_motor
from subfunctions import tau_dcmotor, get_gear_ratio

# Dictionaries for testing
motor = {"speed_noload":3.8,"torque_noload":0,"torque_stall":170, "mass":5.0}
speed_reducer = {"type":"reverted","diam_pinion":0.04,"diam_gear":0.07,"mass":1.5}


# Value functions
gear_ratio = get_gear_ratio(speed_reducer) # Returns a unitless scalar, divide the speed, multiply the torque

# lambda func for finding mechanical power
powerCalc = lambda motor_speed, motor_torque : motor_speed*motor_torque

# All values are based on motor_speed linspace, so no size errors
motor_speed = np.linspace(0,motor["speed_noload"],num=250) / gear_ratio
motor_torque = tau_dcmotor(motor_speed, motor) * gear_ratio

# If module is imported, dosent run the function for no reason
if __name__ == "__main__":
    graph_motor(motor_speed,motor_torque)