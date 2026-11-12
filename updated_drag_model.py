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

#data storage lists
time_data = []
velocity_data = []
success_data = []

# run some sort of loop that appends time and speed data into a fresh array
for diameter in parachute_diameters:
    # Load dicts that define the EDL system, planet, and mission events
    edl_system = define_edl_system_1()
    mars = define_planet()
    mission_events = define_mission_events()

    # Override with desired initial conditions
    edl_system['altitude'] = 11000               # [m] initial altitude
    edl_system['velocity'] = -590                # [m/s] initial velocity
    edl_system['parachute']['deployed'] = True   # Parachute is open
    edl_system['parachute']['ejected'] = False   # Still attached
    edl_system['rover']['on_ground'] = False     # Rover has not yet landed
    edl_system['parachute']['diameter'] = diameter # Update diameter for this run

    tmax = 2000  # [s] maximum simulated time

    # Run the simulation (passing False as last argument turns off message echo)
    [t, Y, edl_system] = simulate_edl(edl_system, mars, mission_events, tmax, False)

    # Capture simulated time at termination
    t_termination = t[-1]
    time_data.append(t_termination)

    # Capture rover speed (relative to ground) at termination
    final_velocity = abs(edl_system['velocity'])
    velocity_data.append(final_velocity)

    # Determine rover landing success (1 = success; 0 = failure)
    # Check if the rover is on the ground and moving slowly enough to survive v <1 m/s
    if edl_system['rover']['on_ground'] == True and final_velocity < 1.0:
        success_data.append(1)
    else:
        success_data.append(0)

# Convert lists to NumPy arrays for plotting
time_data = np.array(time_data)
velocity_data = np.array(velocity_data)
success_data = np.array(success_data)

# Create a figure window
plt.figure(figsize=(8, 8))

# p1 
plt.subplot(3, 1, 1)  
plt.plot(parachute_diameters, time_data, color='blue', marker='o')
plt.title('Parachute Size with MEF study (14m to 19m)')
plt.ylabel('simulation time s')
plt.grid(True)

# p2
plt.subplot(3, 1, 2)  
plt.plot(parachute_diameters, velocity_data, color='red', marker='o')
plt.ylabel('Final velocity m/s')
plt.grid(True)

# p3
plt.subplot(3, 1, 3)  
plt.plot(parachute_diameters, success_data, color='green', marker='o')
plt.ylabel('Success')
plt.xlabel('Parachute diameter m')
plt.yticks([0, 1])
plt.grid(True)


plt.tight_layout()
plt.show()
