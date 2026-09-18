# Do not display anything to the console
# Plot the following three graphs in a 3x1 array
# Use matplotlib.pyplot.subplot
# Motor shaft speed [rad/s] vs. motor shaft torque [Nm] (on x-axis)
# Motor power [W] vs. motor shaft torque [Nm] (on x-axis)
# Motor power [W] vs. motor shaft speed [rad/s]

# All graphs need axes labeled clearly with units
# Use matplotlib.pyplot.xlabel and matbplotlib.pyplot.ylabel commands

# Modules
import matplotlib.pyplot as plt
import numpy as np

# Import from files
from subfunctions import tau_dcmotor

# Dictionary for testing
motor = {"speed_noload":3.8,"torque_noload":0,"torque_stall":170, "mass":5.0}

# Lambda func do find mechanical power of motor
powerCalc = lambda motor_speed, motor_torque : motor_speed*motor_torque

# linspace needs to go from 0 to omega_max (3.8)
# All values are based on motor_speed linspace, so no size errors
motor_speed = np.linspace(0,motor["speed_noload"],num=250)
motor_torque = tau_dcmotor(motor_speed, motor)


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
if __name__ == "main":
    graph_motor(motor_speed,motor_torque)