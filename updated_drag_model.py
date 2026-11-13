import numpy as np
import matplotlib.pyplot as plt
from define_edl_system import *
from subfunctions_EDL import *
from define_planet import *
from define_mission_events import *


# this pizza slice is almost cooked


# create a 3x1 plot of the parachute study 

# inititial condititions 
    # EDL System Altitude 11 km
    # EDL System Velocity -590 m/s
    # Rockets Off
    # Parachute Deployed, not ejected
    # Heat shield Not ejected
    # Sky crane Off
    # Speed controller Off
    # Position controller Off

# use F_drag_descent subfunction in subfunctions_EDL.py for analysis 
# Pass three different diameters into edl_system['parachute']['diameter']. 
    # 3 Diameters:  14 to 19 meters at 0.5 meter intervals
        # linspace(14,19,0.5)

# PLOTS
    # 1. Simulated time (i.e., time at termination of simulation) vs. parachute diameter
    # 2. Rover speed (relative to ground) at simulation termination vs. parachute diameter
    # 3. Rover landing success (1=success; 0=failure) vs. parachute diameter


# PSUEDO CODE 
# define the test range of the parachute diameter


# use the redefined_eld_system in the subfunctions_EDL
    # redefined_eld_system accounts for the initial conditions
    # main_edl_simulation overrites the necessary items before running the sim
        # main_edl is ouputting sim results. Changed NaN to nan (update thing)
    # update the main_edl sim to include the varying diameters edl_system['parachute']['diameter'] = p_diamter
    # update the dictionary for the edl_system['parachute']['diameter'] to equal the an array rather than the set value

# main edl sim provides time of termination and speed at time of termination. 

# what happens when I pass the array of the different diamters in. 
    # output of time and speed for d1
    # outpute of time and speed for d2
    # continued
        # I need to capture that data and throw it into a plot 
        # create another array of time and speed data that corresponds to the diameter data. 

# run some sort of loop that appends time and speed data into a fresh dict
# Define the test range of the parachute diameter (14 to 19 meters at 0.5 meter intervals)
parachute_diameters = np.arange(14, 19.5, 0.5)

#data storage lists (now arrays, cleaner and dont need to convert!)
time_data = np.zeros(len(parachute_diameters))
speed_data = np.zeros(len(parachute_diameters))
success_data = np.zeros(len(parachute_diameters))

tmax = 2000  # [s] maximum simulated time

# run some sort of loop that appends time and speed data into a fresh array
for i, diameter in enumerate(parachute_diameters):
    # Load dicts that define the EDL system, planet, and mission events
    edl_system = define_edl_system_1()
    mars = define_planet()
    mission_events = define_mission_events()

    # Override with desired initial conditions
    edl_system['altitude'] = 11000               # [m] initial altitude
    edl_system['velocity'] = -590                # [m/s] initial velocity
    edl_system['rocket']['on'] = False           # Rockets Off
    edl_system['parachute']['deployed'] = True   # Parachute is open
    edl_system['parachute']['ejected'] = False   # Still attached
    edl_system['heat_shield']['ejected'] = False # Not ejected
    edl_system['sky_crane']['on'] = False        # Disable Sky crane
    edl_system['speed_control']['on'] = False # Disable Speed controller
    edl_system['position_control']['on'] = False # Postion controller disabled

    # Update diameter for current iteration
    edl_system['parachute']['diameter'] = diameter # Update diameter for this run

    edl_system['parachute']['use_MEF'] = True # Enables MEF, no backwards compatibility issuses (this time haha)

    # Run the simulation (passing False as last argument turns off message echo)
    t, Y, edl_system = simulate_edl(edl_system, mars, mission_events, tmax, False)

    # Capture simulated time at termination
    time_data[i] = t[-1]

    # Capture rover speed (relative to ground) at termination
    final_speed = abs(edl_system['velocity'])
    speed_data[i] = final_speed

    # Determine rover landing success (1 = success; 0 = failure)
    # Check if the rover is on the ground and moving slowly enough to survive v <1 m/s
    if edl_system['rover']['on_ground'] and final_speed < 1.0:
        success_data[i] = 1
    else:
        success_data[i] = 0

# Create 3x1 subplot array using plt.subplots
fig, axs = plt.subplots(3, 1, figsize=(8, 9))

# Plot 1: Simulated time vs. parachute diameter
axs[0].plot(parachute_diameters, time_data, color='blue', marker='o', linewidth=1.5)
axs[0].set_title('Impact of Parachute Diameter with Modified Drag Model (MEF)')
axs[0].set_xlabel('Parachute Diameter [m]')
axs[0].set_ylabel('Simulated Time [s]')
axs[0].grid(True)

# Plot 2: Rover speed at termination vs. parachute diameter
axs[1].plot(parachute_diameters, speed_data, color='red', marker='o', linewidth=1.5)
axs[1].set_xlabel('Parachute Diameter [m]')
axs[1].set_ylabel('Termination Speed [m/s]')
axs[1].grid(True)

# Plot 3: Rover landing success vs. parachute diameter
axs[2].plot(parachute_diameters, success_data, color='green', marker='o', linewidth=1.5)
axs[2].set_xlabel('Parachute Diameter [m]')
axs[2].set_ylabel('Landing Success [1/0]')
axs[2].set_yticks([0, 1])
axs[2].set_ylim([-0.15, 1.15])
axs[2].grid(True)

plt.tight_layout()
plt.show()

# Added graph for data visualization

# import numpy as np
# import matplotlib.pyplot as plt
# import scipy.interpolate as interp

# # Experimental data from PDF table
# mach = np.array([
#     0.25, 0.5, 0.65, 0.7, 0.8, 0.9, 0.95, 1.0, 1.1, 1.2,
#     1.3, 1.4, 1.5, 1.6, 1.8, 1.9, 2.0, 2.2, 2.5, 2.6
# ])

# mef = np.array([
#     1.0, 1.0, 1.0, 0.97, 0.91, 0.72, 0.66, 0.75, 0.90, 0.96,
#     0.990, 0.999, 0.992, 0.98, 0.91, 0.85, 0.82, 0.75, 0.64, 0.62
# ])

# # Piecewise linear interpolation model with clamped boundary fill values
# mef_interp = interp.interp1d(mach, mef, kind='linear', bounds_error=False, fill_value=(1.0, 0.62))

# # Generate continuous Mach domain (including regions < 0.25 and > 2.6 to show clamping)
# mach_continuous = np.linspace(0.0, 3.0, 500)
# mef_continuous = mef_interp(mach_continuous)

# plt.figure(figsize=(8, 4.5))
# plt.plot(mach_continuous, mef_continuous, 'b-', linewidth=1.8, label='Continuous Linear Interpolation (mef_interp)')
# plt.scatter(mach, mef, color='red', zorder=5, label='Experimental Test Data')
# plt.title('Continuous Mach Efficiency Factor (MEF) Model vs. Mach Number')
# plt.xlabel('Mach Number, M [-]')
# plt.ylabel('Mach Efficiency Factor, MEF [-]')
# plt.ylim([0.55, 1.05])
# plt.grid(True)
# plt.legend()
# plt.tight_layout()
# plt.show()