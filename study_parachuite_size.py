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
p_diameter = np.arange(14, 19, 0.5) # outputs an array

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
parachute_diameters = np.arange(14, 19.5, 0.5)
time_data = []
velocity_data = []

for diameter in parachute_diameters: # runs the sim for each parachute diameter 
    # run the main_edl_simulation with the changed parachute diameter. 
    # *************************************
    # load dicts that define the EDL system (includes rover), planet,
    # mission events and so forth.
    edl_system = define_edl_system_1()
    mars = define_planet()
    mission_events = define_mission_events()


    # Overrides what might be in the loaded data to establish our desired
    # initial conditions
    edl_system['altitude'] = 11000    # [m] initial altitude
    edl_system['velocity'] = -590     # [m/s] initial velocity
    edl_system['parachute']['deployed'] = True   # our parachute is open
    edl_system['parachute']['ejected'] = False   # and still attached
    edl_system['rover']['on_ground'] = False # the rover has not yet landed
    edl_system['parachute']['diameter'] = diameter

    tmax = 2000   # [s] maximum simulated time

    # the simulation. changing last argument to false turns off message echo
    [t, Y, edl_system] = simulate_edl(edl_system, mars, mission_events, tmax, True)

    # THIS CORRECTLY RUNS

    # now appending data into lists for my charts
    time_data = np.append[] #appends termination time 
    speed_data = np.append[] #appends speed at termination time 

# make the plots

plot1 = plt.figure(0)
plt.title = ('time at termination of simulation vs. parachute diameter')


plot2 = plt.figure(1)
plt.title = ('speed vs time at termination vs. parachute diameter')

plot3 = plt.figure(2)
plt.title = ('Rover landing success (1=success; 0=failure) vs. parachute diameter')


    




