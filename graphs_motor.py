# Do not display anything to the console
# Plot the following three graphs in a 3x1 array
# Use matplotlib.pyplot.subplot
# Motor shaft speed [rad/s] vs. motor shaft torque [Nm] (on x-axis)
# Motor power [W] vs. motor shaft torque [Nm] (on x-axis)
# Motor power [W] vs. motor shaft speed [rad/s]

# All graphs need axes labeled clearly with units
# Use matplotlib.pyplot.xlabel and matbplotlib.pyplot.ylabel commands

import matplotlib.pyplot as plt
import numpy as np

from subfunctions import tau_dcmotor



x = np.linspace(0,10, 400)
y = np.linspace(0,30, 400)
z = np.linspace(0,20, 400)

motor_speed = None
motor_power = None
motor_torque = None


def graph_motor (motor_speed, motor_power, motor_torque):
    # Assign a style
    plt.style.use('bmh')

    # Create the figures
    fig, axs = plt.subplots(3,1,sharey=True)

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

graph_motor(x,y,z)