#

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

rover = {
    "wheel_assembly": {
        "motor": {
            "effcy_tau": [0, 10, 20, 40, 70, 165],
            "effcy": [0, 0.55, 0.75, 0.71, 0.50, 0.05]
        }
    }
}

effcy_tau = rover["wheel_assembly"]["motor"]["effcy_tau"]
effcy = rover["wheel_assembly"]["motor"]["effcy"]

min_distance = np.min(effcy_tau)
max_distance = np.max(effcy_tau)

value_range = np.linspace(min_distance,max_distance, num=100)

def effcy_torque(effcy_tau, effcy, value_range):

    effcy_fun = interp1d(effcy_tau, effcy, kind = 'cubic') # fit the cubic spline

    plt.plot(value_range,effcy_fun(value_range), '-', label='Cubic Spline', color='brown')
    plt.plot(effcy_tau, effcy, label = 'Original Data', color='black')
    plt.title('Efficiency vs. Torque')
    plt.xlabel('Torque (Nm)')
    plt.ylabel('Efficiency')
    plt.legend()
    plt.show()

# If module is imported, dosent run the function for no reason
if __name__ == "__main__":
    effcy_torque(effcy_tau, effcy, value_range)