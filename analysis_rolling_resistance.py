# - Assume a terrain slope of 0 degrees (horizontal terrain) 
# • Generate rolling resistance coefficients to test with the following line of code:  
# o Crr_array = numpy.linspace(0.01,0.5,25); 
# • Store the maximum velocity [m/s] at each rolling resistance coefficient in a vector called v_max. 
# • Plot v_max versus Crr_array. Make sure to label the axes and indicate their units. 
# • Do not display anything to the console

#import library functions
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import bisect

#import subfunctions
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

# establish arrays 
Crr_array = np.linspace(0.01,0.5,25)  # 25 numbers of rolling resistance coefficients between 0.01 and 0.5
v_max = []

#define parameters
left = 0  
right = rover['wheel_assembly']['motor']['speed_noload']  
radius = rover['wheel_assembly']['wheel']['radius']
Ng = get_gear_ratio(rover['wheel_assembly']['speed_reducer'])

# iterate through the Crr array to find max velocity with each Crr and then store it into v_max
for Crr in Crr_array: 

    # function of the force with omega as the only changing variable
    force = lambda omega : F_net(omega, 0, rover, planet, Crr)


    try: 
    #find the root using bisect 
        omega_root = bisect(force, left, right)

            #convert the root from angular to translational
        v_max_value = radius*(omega_root/Ng)

        v_max.append(v_max_value)

    except: 
        # append a null value if no root present
        v_max.append(np.nan) 
        print ('howdy')


# create plot showing v_max versus Crr_array
plt.plot (Crr_array, v_max)
plt.title('Rover max velocity vs Crr')
plt.xlabel('Coefficient of rolling resistance')
plt.ylabel('velocity (m/s)')
plt.grid(True)
plt.show()





    


    


