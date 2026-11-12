import numpy as np
import matplotlib.pyplot as plt
from define_edl_system import *
from subfunctions_EDL import *
from define_planet import *
from define_mission_events import *
import scipy.interpolate as interp

# upadte drag model used in F_drag_descent 
# use to convert from m/s to mach def v2M_Mars(v, a)

# create a model for the 𝑀𝐸𝐹 value at a given Mach number

# 1. grab velocity data from sub functions and then convert it into a mach
# 2. Interpolate mach value found in step 1 to found correct MEF value 
# 3. Use MEF value to find the coefficient of drag modified



# TABLES FROM PDF FOR MACH AND MEF
mach = np.array([
    0.25, 0.5, 0.65, 0.7, 0.8, 0.9, 0.95, 1.0, 1.1, 1.2,
    1.3, 1.4, 1.5, 1.6, 1.8, 1.9, 2.0, 2.2, 2.5, 2.6
])

mef = np.array([
    1.0, 1.0, 1.0, 0.97, 0.91, 0.72, 0.66, 0.75, 0.90, 0.96,
    0.990, 0.999, 0.992, 0.98, 0.91, 0.85, 0.82, 0.75, 0.64, 0.62
])

#1. 
#interpolation function through MEF for a given M value
mef_interp = interp.interp1d(mach, mef, kind='linear', fill_value="extrapolate")


mef_interp(mach)


