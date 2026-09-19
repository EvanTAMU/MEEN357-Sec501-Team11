# Use a root finding method to determine the speed of the rover at various values
# Using the coefficient of rolling resistance AND terrain slope

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from subfunctions import get_gear_ratio, F_net

# define rover and planet dictionaries 
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

planet = {
    'g':3.72 # [m/s^2] acceleration due to gravity on Mars
}

speed_reducer = {
    'type':'reverted',
    'diam_pinion':0.04, # [m]
    'diam_gear':0.07, # [m]
    'mass':1.5 # [kg]
}

# Rolling resistance coefficients

Crr_array = np.linspace(0.01,0.5,25)

# Array of terain angles
slope_array_deg = np.linspace(-15,35,25)

# Turn arrays into matricies
CRR, SLOPE = np.meshgrid(Crr_array,slope_array_deg)

def bisection(fun,a,b,errTol=1e-6,iterMax=100,funTol=1e-6):
    '''Bisection method'''
    # Check inital values
    fl = fun(a)
    fu = fun(b)
    if fl*fu > 0:
        raise ValueError("The values must be one positive and one negative")

    # assign x_low and x_upper    
    xl = a
    xu = b
    iterNum = 0

    while iterNum < iterMax:
        iterNum += 1

        # Bisect the interval
        xr = (xl + xu) / 2.0 #New x value
        fr = fun(xr) # New point value

        # Absolute erro estimate
        err_est = (xu - xl) / 2.0

        if (err_est <= errTol):
            # Error Tolerance achieved
            break
        if (abs(fr) < funTol):
            # Function Tolerance achieved
            break

        # Assign bounds
        if fr == 0.0:
            break
        elif (fr*fl) < 0:
            xu = xr
        else: 
            xl = xr
            fl = fr

    return xr

def vmax_calculations(CRR,SLOPE):
    # Matrix of zeros the same size as CRR and SLOPE
    VMAX = np.zeros(np.shape(CRR), dtype=float)

    # determine matrix size
    N = np.shape(CRR)[0]

    # Assign values for math
    ratio = get_gear_ratio(speed_reducer)
    radius = rover['wheel_assembly']['wheel']['radius']

    bisection_low = 0 # No omega value
    bisection_high = rover['wheel_assembly']['motor']['speed_noload'] # Max omega value

    for i in range(N):
        for j in range(N):
            Crr_sample = float(CRR[i,j])
            slope_sample = float(SLOPE[i,j])
            # force function
            force = lambda omega : F_net(omega, slope_sample, rover, planet, Crr_sample)
            # Find F=0 for omega_max value
            try:
                omega_max = bisection(force, bisection_low, bisection_high)
            except ValueError:
                # When two positive values are entered, they must be skipped, return with NAN
                omega_max = np.nan

            # Plot the value accordingly with ratios in mind
            VMAX[i,j] =  radius * (omega_max / ratio) # Put code to find max speed at Crr_sample and slope_sample

    # Now repreesnt the data
    colormap = 'plasma'
    # 3D surface method
    figure = plt.figure()
    ax = figure.add_subplot(111, projection='3d')
    ax.plot_surface(CRR, SLOPE, VMAX, cmap=colormap)
    # viewing angle
    ax.view_init(elev=30, azim=135)
    # formatting
    ax.set_title('Maximum Rover Speed vs. Rolling Resistance and Terrain Slope')
    ax.set_xlabel('Coefficient of Rolling Resistance')
    ax.set_ylabel('Terrain Slope (degrees)')
    ax.set_zlabel('Maximum Velocity (m/s)')
    # show
    plt.show()

    # contour 2D method
    contour = plt.contourf(CRR, SLOPE, VMAX, 100, cmap=colormap)

    # color scale legend
    plt.colorbar(contour, label='Maximum Velocity (m/s)')

    # formatting
    plt.title('Maximum Rover Speed vs. Rolling Resistance and Terrain Slope')
    plt.xlabel('Coefficient of Rolling Resistance')
    plt.ylabel('Terrain Slope (degrees)')
    # show
    plt.show()

if __name__ == "__main__":
    vmax_calculations(CRR,SLOPE)