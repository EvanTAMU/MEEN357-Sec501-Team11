# Use a root finding method to determine the speed of the rover at various values
# Using the coefficient of rolling resistance AND terrain slope

import numpy as np
import matplotlib.pyplot as plt

def bisection(fun,space,errTol=1e-6,iterMax=100,funTol=1e-6):
    '''Bisection method'''
    # assign x_low and x_upper    
    xl = space[0]
    xu = space[-1]
    iterNum = 0
    done = False

    while not done and iterNum < iterMax:
        iterNum += 1
        # Disect the interval
        xr = (xl+xu)/2 #New x value
        fl = fun(xl)
        fr = fun(xr) # New point value

        err_est = (((xr-xl)/xr)*100)

        if (err_est <= errTol):
            # Error Tolerance achieved
            break
        if (fr < funTol):
            # Function Tolerance achieved
            break

        if (fr*fl) < 0:
            xu = xr
        else: xl = xr
    return

def vmax_calculations(CRR,SLOPE):
    # Rolling resistance coefficients
    Crr_array = np.linspace(0.01,0.5,25)

    # Array of terain angles
    slope_array_deg = np.linspace(-15,35,25)

    # Turn arrays into matricies
    CRR, SLOPE = np.meshgrid(Crr_array,slope_array_deg)

    # Matrix of zeros the same size as CRR and SLOPE
    VMAX = np.zeros(np.shape(CRR), dtype=float)

    # determine matrix size
    N = np.shape(CRR)[0]

    for i in range(N):
        for j in range(N):
            Crr_sample = float(CRR[i,j])
            slope_sample = float(SLOPE[i,j])
            VMAX[i,j] = None# Put code to find max speed at Crr_sample and slope_sample
            
    # Now repreesnt the data


if __name__ == "__main__":
    vmax_calculations()