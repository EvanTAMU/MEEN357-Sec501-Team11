# ALMOST the exact same as graphs_motor.py, but utilizes the values from the speed reducer
# NOT VALUES FROM THE SHAFT!

import numpy as np
import matplotlib.pyplot as plt

from subfunctions import tau_dcmotor, get_gear_ratio

# Dictionaries for testing
motor = {"speed_noload":3.8,"torque_noload":0,"torque_stall":170, "mass":5.0}
speed_reducer = {"type":"reverted","diam_pinion":0.04,"diam_gear":0.07,"mass":1.5}


# Value functions
gear_ratio = get_gear_ratio(speed_reducer) # Returns a unitless scalar, divide the speed, multiply the torque

# lambda func for finding mechanical power
powerCalc = lambda motor_speed, motor_torque : motor_speed*motor_torque

# All values are based on motor_speed linspace, so no size errors
unreduced_motor_speed = np.linspace(0,motor["speed_noload"],num=250)
motor_torque = tau_dcmotor(unreduced_motor_speed, motor) * gear_ratio
motor_speed = unreduced_motor_speed / gear_ratio

def graph_motor (motor_speed, motor_torque):
    # Get motor Mechanical Power
    motor_power = powerCalc(motor_speed, motor_torque)

    # Assign a style
    plt.style.use('bmh')

    # Create the figures
    fig, axs = plt.subplots(3,1, figsize=(7,9))

    # Plot the values
    axs[0].plot(motor_torque,motor_speed,'r')
    axs[0].set_ylabel("motor shaft speed [rad/s]",rotation ='horizontal',ha="right")
    axs[0].set_xlabel("motor shaft torque [Nm]")

    axs[1].plot(motor_torque,motor_power,'b')
    axs[1].set_ylabel("motor power [W]",rotation ='horizontal',ha="right")
    axs[1].set_xlabel("motor shaft torque [Nm]")

    axs[2].plot(motor_speed,motor_power,'g')
    axs[2].set_ylabel("motor power [W]",rotation ='horizontal',ha="right")
    axs[2].set_xlabel("motor shaft speed [rad/s]")

    # Apply layout and show
    fig.suptitle("Motor Values Graph", fontsize=16,fontweight="bold")

    plt.tight_layout()
    plt.subplots_adjust()
    plt.show()

# If module is imported, dosent run the function for no reason
if __name__ == "__main__":
    graph_motor(motor_speed,motor_torque)