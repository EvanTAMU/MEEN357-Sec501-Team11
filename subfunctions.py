#import libraries#
import numpy as np
import matplotlib.pyplot as plt
import math as mp


def tau_dcmotor(omega: np.array,motor) -> float:
    """Returns  the  motor  shaft  torque  when  given  motor  shaft  speed  and  a  dictionary  containing 
    important specifications for the motor"""
    # 6 motors
    omega_max = int() # No load speed (MAX)
    tau_max = int()

    if (omega < 0):
        # The wheel is turning BACKWARDS, a force is pushing it back
        print("Motor is spinning backwards~")
        return tau_max
    if (omega > omega_max):
        print("Wheel is being spun forward~")
        return 0 # Return tau = 0 if wheeling is being forced faster than possible

    tau = None



    return tau
    

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


def F_drive():
    """Returns the force applied to the rover by the drive system given information about the drive 
    system (wheel_assembly) and the motor shaft speed. """
    

def F_gravity():
    """Returns  the  magnitude  of  the  force  component  acting  on  the  rover  in  the  direction  of  its 
    translational  motion  due  to  gravity  as  a  function  of  terrain  inclination  angle  and  rover 
    properties. """
    

def F_rolling():
    """Returns  the  magnitude  of  the  force  acting  on  the  rover  in  the  direction  of  its  translational 
    motion  due  to  rolling  resistances  given  the  terrain  inclination  angle,  rover  properties,  and  a 
    rolling resistance coefficient. """
    

def F_net():
    """Returns  the  magnitude  of  net  force  acting  on  the  rover  in  the  direction  of  its  translational 
    motion."""
    

