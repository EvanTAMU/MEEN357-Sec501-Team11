# ALMOST the exact same as graphs_motor.py, but utilizes the values from the speed reducer
# NOT VALUES FROM THE SHAFT!

from graphs_motor import graph_motor
from subfunctions import tau_dcmotor, get_gear_ratio

gear_ratio = get_gear_ratio()

motor_speed = None * gear_ratio
motor_power = None * gear_ratio
motor_torque = tau_dcmotor() * gear_ratio

graph_motor(motor_speed,motor_power,motor_torque)