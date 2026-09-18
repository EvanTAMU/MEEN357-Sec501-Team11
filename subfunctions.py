#import libraries
import numpy as np
import matplotlib.pyplot as plt
import math as mp

#from sqlalchemy import false

# DONE!

def tau_dcmotor(omega: np.ndarray | int | float, motor: dict) -> np.ndarray | float | int:
    """Returns  the  motor  shaft  torque  when  given  motor  shaft  speed  
    and  a  dictionary  containing important specifications for the motor"""

    # INPUT CHECKS
    # omega
    if not isinstance(omega,(np.ndarray,int,float)):
        print(type(omega))
        raise Exception('Omega is not a valid input type => np.ndarray | float | int')
    # motor
    if not isinstance(motor,dict):
        raise Exception('motor is not a valid input type => dict')

    speed_noload = motor["speed_noload"] # rad/s | No load speed (MAX)
    torque_stall = motor["torque_stall"] # Nm | Motor Stall torque (MAX)
    torque_noload = motor["torque_noload"] # Nm | No load torque (0)
    
    # Do a loop if an array, otherwise just run the math
    if isinstance(omega,np.ndarray):
        tau = [] # make it a list then a numpy array (easier!)

        for w in range(len(omega)):
            if (omega[w] < 0):
                # The wheel is turning BACKWARDS, a force is pushing it back
                #print("Motor is spinning backwards~")
                tau.append(torque_stall)
            if (omega[w] > speed_noload):
                #print("Wheel is being spun forward~")
                tau.append(0) # Return tau = 0 if wheel is being forced faster than possible

            # Do this for every element in the numpy array

            else: tau.append((torque_stall - (((torque_stall - torque_noload) / speed_noload) * omega[w])))

        return np.array(tau)

    else: 
        tau = None
        if (omega < 0):
            # The wheel is turning BACKWARDS, a force is pushing it back
            tau = torque_stall
        if (omega > speed_noload):
            # Return tau = 0 if wheel is being forced faster than possible
            tau = 0
        tau = (torque_stall - (((torque_stall - torque_noload) / speed_noload) * omega))

        return float(tau) # Return a scalar, if input is not nparray

def get_gear_ratio():
    """Returns the speed reduction ratio for the speed reducer based on speed_reducer dict."""
    

def get_mass(rover):
    """Computes the total mass of the rover. Uses information in the rover dict."""

    #rover dictionary for all masses of the rover components
    #this would find "chassis" in the rover dictionary and then look at its "mass"
    chassis_mass = rover['chassis']['mass'] 
    power_subsystem_mass = rover['power_subsystem']['mass']
    payload_mass = rover['payload']['mass']

    #subdictionary for the wheel assembly that contians the motor, speed reducer, and the wheels.
    motor_mass = rover['wheel_assembly']['motor']['mass']
    speed_reducer = rover['wheel_assembly']['speed_reducer']['mass']
    wheel_mass = rover['wheel_assembly']['wheel']['mass']

    #multiple the wheel assembly mass by 6 because there are 6 wheels on the rover
    wheel_assembly_mass = 6*(motor_mass + speed_reducer + wheel_mass)

    mass_total = chassis_mass + power_subsystem_mass + payload_mass + wheel_assembly_mass
    return mass_total


def F_drive(omega,rover):
    """Returns the force applied to the rover by the drive system given information about the drive 
    system (wheel_assembly) and the motor shaft speed. """
    
    

def F_gravity(terrain_angle, rover, planet):
    """Returns  the  magnitude  of  the  force  component  acting  on  the  rover  in  the  direction  of  its 
    translational  motion  due  to  gravity  as  a  function  of  terrain  inclination  angle  and  rover 
    properties. """
    # terrain angle comes from a numpy array. the 
    # if the angles are given as an array fgt will be an array of the same size, this is the nature of numpy
    
    fgt = rover['chassis']['mass'] * planet['g'] * np.sin(np.radians(terrain_angle))
    return fgt


def F_rolling(omega, terrain_angle, rover, planet, Crr):
    """Returns  the  magnitude  of  the  force  acting  on  the  rover  in  the  direction  of  its  translational 
    motion  due  to  rolling  resistances  given  the  terrain  inclination  angle,  rover  properties,  and  a 
    rolling resistance coefficient. """
    while not done:
        if np.isscalar(omega) is False:
            raise Exception('motor shaft speed is not a scalar')
        if np.isscalar(terrain_angle) is False:
            raise Exception('terrain angle is not a scalar')
        if size(omega) != size(terrain_angle):
            raise Exception('motor shaft speed and terrain angle are not the same size')
        if (-75 < terrain_angle < 75) is False:
            raise Exception('terrain angle is out of range')
        if isinstance(rover, dict) is False:
            raise Exception('rover is not dict')
        if isinstance(planet, dict) is False:
            raise Exception('planet is not dict')
        if (np.isscalar(Crr) and Crr > 0) is False:
            raise Exception('Crr is not a positive scalar')
        else:
            done = True

def F_net(omega, terrain_angle, rover, planet, Crr):
    """Returns  the  magnitude  of  net  force  acting  on  the  rover  in  the  direction  of  its  translational 
    motion."""
    #call functions
    F_drive = F_drive(omega, rover)
    F_gravity = F_gravity(terrain_angle, rover, planet)
    F_rolling(omega, terrain_angle, rover, planet, Crr)

    #check parameters
    done = False
    while not done:
        if np.isscalar(omega) is False:
            raise Exception('motor shaft speed is not a scalar')
        if np.isscalar(terrain_angle) is False:
            raise Exception('terrain angle is not a scalar')
        if size(omega) != size(terrain_angle):
            raise Exception('motor shaft speed and terrain angle are not the same size')
        if (-75 < terrain_angle < 75) is False:
            raise Exception('terrain angle is out of range')
        if isinstance(rover, dict) is False:
            raise Exception('rover is not dict')
        if isinstance(planet, dict) is False:
            raise Exception('planet is not dict')
        if (np.isscalar(Crr) and Crr > 0) is False:
            raise Exception('Crr is not a positive scalar')
        else:
            done = True
    #execute calculations for net force
    if terrain_angle == 0:
        fx = F_drive - F_rolling
        fy = F_gravity
        F_net = mp.sqrt((fx**2) + (fy**2))
    elif -75 < terrain_angle < 0:
        fx = F_drive - F_rolling + (F_gravity * mp.sin(mp.radians(terrain_angle)))
        fy = F_gravity * mp.cos(mp.radians(terrain_angle))
        F_net = mp.sqrt((fx**2) + (fy**2))
    elif 0 < terrain_angle < 75:
        fx = F_drive - F_rolling - F_gravity * mp.sin(mp.radians(terrain_angle))
        fy = F_gravity * mp.cos(mp.radians(terrain_angle))
        F_net = mp.sqrt((fx**2) + (fy**2))
    else:
        print('error')



    
