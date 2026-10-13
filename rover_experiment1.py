# simulate trajectory of the rover using simulate_rover function

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

from define_experiment import experiment1
from subfunctions import simulate_rover


experiment, end_event = experiment1()
# experiment and end_event are dictionaries of data

end_event['max_distance'] = 1000
end_event['max_time'] = 10000
end_event['min_velocity'] = 0.01

planet = {
    'g':3.72 # [m/s^2] acceleration due to gravity on Mars
}

# # used AI to create rover dictionary
rover = {
    'wheel_assembly': {
        'wheel': {
            'radius': 0.3,    # Radius of drive wheel [m]
            'mass': 1.0       # Mass of one drive wheel [kg]
        },
        'speed_reducer': {
            'type': 'reverted',  # Reducer type (reverted gear train)
            'diam_pinion': 0.04, # Pinion diameter d1 [m]
            'diam_gear': 0.07,   # Gear diameter d2 [m]
            'mass': 1.5          # Mass of speed reducer assembly [kg]
        },
        'motor': {
            'torque_stall': 170.0,  # Motor stall torque [N-m]
            'torque_noload': 0.0,   # Motor no-load torque [N-m]
            'speed_noload': 3.80,   # Motor no-load speed [rad/s]
            'mass': 5.0             # Mass of motor [kg]
        }
    },
    'chassis': {
        'mass': 659.0  # Mass of rover chassis [kg]
    },
    'science_payload': {
        'mass': 75.0   # Combined mass of all scientific instruments [kg]
    },
    'power_subsys': {
        'mass': 90.0   # Mass of RTG power subsystem [kg]
    }
}

# Need 3x1 Figure with these subfigures:
# Position vs. time
# Velocity vs. time
# Power vs. time


rover = simulate_rover(rover,planet,experiment,end_event)

def rover_experiment(rover,):

    return None

# If module is imported, dosent run the function for no reason
if __name__ == "__main__":
    rover_experiment(rover,)