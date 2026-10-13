#

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

from define_experiment import experiment1


experiment, end_event = experiment1()
# experiment and end_event are dictionaries of data


alpha_dist = experiment['alpha_dist']
alpha_deg = experiment['alpha_deg']

min_distance = np.min(alpha_dist)
max_distance = np.max(alpha_dist)

value_range = np.linspace(min_distance,max_distance, num=100)


def define_terrain(alpha_dist,alpha_deg,value_range):

    # fit the cubic spline
    alpha_fun = interp1d(alpha_dist, alpha_deg, kind = 'cubic', fill_value='extrapolate')

    plt.plot(value_range,alpha_fun(value_range), '-', label='Cubic Spline', color='brown')
    plt.plot(alpha_dist, alpha_deg, 'b*', label = 'Original Data', color='black')
    plt.title('Terrain Angle vs. Position')
    plt.xlabel('Distance (m)')
    plt.ylabel('Angle (degrees)')
    plt.legend()
    plt.show()

# If module is imported, dosent run the function for no reason
if __name__ == "__main__":
    define_terrain(alpha_dist,alpha_deg,value_range)