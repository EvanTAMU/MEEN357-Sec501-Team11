#import library functions
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import bisect

#import necessary subfunctions
from subfunctions import get_gear_ratio, F_net

# define rover and planet dictionaries # used AI to create rover dictionary
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


planet = {
    'g':3.72 # acceleration due to gravity on Mars
    }

speed_reducer = {
    'reverted'
}


#set parameters
slope_array_deg = np.linspace(-15,35,25)
Crr = .015

#define more parameters for bisect 
left = 0  
right = rover['wheel_assembly']['motor']['speed_noload']  
radius = rover['wheel_assembly']['wheel']['radius']

# call function to get the gear ratio Ng for converting omega to velocity
Ng = get_gear_ratio(rover['wheel_assembly']['speed_reducer'])

#store vmax values
v_max = []

for slope_deg in slope_array_deg : 

    force = lambda omega: F_net(omega, slope_deg, rover, planet, Crr)

    try: 
        #find the root using bisect 
        omega_root = bisect(force, left, right)

        #convert the root from angular to translational
        v_max_value = radius*(omega_root/Ng)

        v_max.append(v_max_value)
   
    except : 
        # append a null value if no root present
        v_max.append(np.nan) 


#plot vmax vs slope
plt.plot(v_max,slope_array_deg)
plt.xlabel('Incline Angle: degrees')
plt.ylabel('Maximum Velocity: m/s')
plt.grid(True)
plt.show()


        


