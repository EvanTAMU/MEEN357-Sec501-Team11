#import libraries
import numpy as np
import matplotlib.pyplot as plt
import math

def tau_dcmotor(omega, motor):
    """Returns  the  motor  shaft  torque  when  given  motor  shaft  speed  
    and  a  dictionary  containing important specifications for the motor"""

    # Rewritten code for dcmotor, now with key checker
    if not isinstance(motor,dict):
        raise Exception('motor is not a valid input type; dict')
    
    required_keys = ["speed_noload", "torque_stall", "torque_noload"]
    if not all(key in motor for key in required_keys):
        raise Exception('motor dictionary is missing required specifications')
    
    is_scalar = np.isscalar(omega)
    is_vector = isinstance(omega, np.ndarray) and omega.ndim == 1

    if not (is_scalar or is_vector):
        raise Exception('omega must be a scaler or a 1D numpy array (vector)')

    # Get motor propertires
    speed_noload = motor["speed_noload"] # rad/s | No load speed (MAX)
    torque_stall = motor["torque_stall"] # Nm | Motor Stall torque (MAX)
    torque_noload = motor["torque_noload"] # Nm | No load torque (0)

    slope = (torque_stall - torque_noload) / speed_noload
    tau = torque_stall - (slope * omega)

    tau = np.where(omega < 0, torque_stall, tau)
    tau = np.where(omega > speed_noload, 0, tau)

    if is_scalar:
        return float(tau)
    else:
        return np.asarray(tau)

def get_gear_ratio(speed_reducer):
    """Returns the speed reduction ratio for the speed reducer based on speed_reducer dict."""

    #CHECK INPUTS
    #check that speed_reducer is a dictionary
    if not isinstance(speed_reducer,dict):
        raise Exception('speed_reducer is not a valid input type; dict')

    #String comparison function
    lower_case_speed_reducer_type = speed_reducer['type'].lower() #turns type into lower case
    if not lower_case_speed_reducer_type == 'reverted': 
        raise Exception('speed_reducer[type] is not a valid input type; \"reverted\"')

    #CALCULATION
    d2 = speed_reducer['diam_gear'] 
    d1 = speed_reducer['diam_pinion'] 
    Ng = (d2/d1)**2 #speed reduction ratio for the speed reducer

    # ensure returned value is a float
    return float(Ng)

def get_mass(rover):
    """Computes the total mass of the rover. Uses information in the rover dict."""


    #INPUT CHECKS 
    #check that rover is a dictionary 
    if not isinstance(rover,dict):
        raise Exception('rover is not a valid input type;  dict')
    

    #rover dictionary for all masses of the rover components
    #this would find "chassis" in the rover dictionary and then look at its "mass"
    chassis_mass = rover['chassis']['mass'] 
    power_subsystem_mass = rover['power_subsys']['mass']
    payload_mass = rover['science_payload']['mass']

    #subdictionary for the wheel assembly that contians the motor, speed reducer, and the wheels.
    motor_mass = rover['wheel_assembly']['motor']['mass']
    speed_reducer_mass = rover['wheel_assembly']['speed_reducer']['mass']
    wheel_mass = rover['wheel_assembly']['wheel']['mass']

    #multiple the wheel assembly mass by 6 because there are 6 wheels on the rover
    wheel_assembly_mass = 6*(motor_mass + speed_reducer_mass + wheel_mass)

    mass_total = chassis_mass + power_subsystem_mass + payload_mass + wheel_assembly_mass
    return mass_total


def F_drive(omega,rover):
    """Returns the force applied to the rover by the drive system given information about the drive 
    system (wheel_assembly) and the motor shaft speed. """

    #INPUT CHECKS
    #check that omega is a scalar or vector
    if not isinstance(omega,(np.ndarray,np.number,int,float)):
        raise Exception('omega must be a scaler or a 1D numpy array (vector)')
    #check that rover is a dictionary
    if not isinstance(rover,dict): 
        raise Exception('rover is not a valid input type; dict')


    #Call tau-dcmotor to get the torque at the motor shaft
    tau_motor = tau_dcmotor(omega,rover['wheel_assembly']['motor']) # n*m

    #call gear ratio to get speed reduction ratio (Ng)
    Ng = get_gear_ratio(rover['wheel_assembly']['speed_reducer']) 

    #radius of the wheel 
    radius = rover['wheel_assembly']['wheel']['radius'] 

    #Force exerted by one wheel on the ground
    Fd_one = (tau_motor*Ng)/radius

    #Total force exerted by all 6 wheels on the ground
    Fd = 6*Fd_one
    return Fd


def F_gravity(terrain_angle, rover, planet):
    """Returns  the  magnitude  of  the  force  component  acting  on  the  rover  in  the  direction  of  its 
    translational  motion  due  to  gravity  as  a  function  of  terrain  inclination  angle  and  rover 
    properties. """
    # terrain angle comes from a numpy array. the 
    # if the angles are given as an array fgt will be an array of the same size, this is the nature of numpy
    
    #INPUT CHECKS
    #check terrain angle is a scalar of vector
    if not isinstance(terrain_angle,(np.ndarray,np.number,int,float)):
        raise Exception('Terrain angle is not a valid input type; np.ndarray, float, int')

    # Validating input angle is within range [-75,75] degrees
    # use np.asanarray to convert terrain_angle into array if not already. allows for scalar or vector pass through
    angle_array = np.asanyarray(terrain_angle)
    if not np.all((angle_array >= -75) & (angle_array <= 75)):
        raise Exception('Terrain angle is not a valid input value; -75 to 75 degrees')

    # check rover is dict
    if not isinstance(rover,dict):
        raise Exception('Rover is not a valid input type;  dict')

    # check planet is dict
    if not isinstance(planet,dict):
        raise Exception('Planet is not a valid input type;  dict')

    # call get_mass to get the total mass of the rover
    total_mass = get_mass(rover)

    #multiply by -1 to account for sign convention. + angle = - F
    fgt = -1 * total_mass * planet['g'] * np.sin(np.radians(terrain_angle))

    return fgt


def F_rolling(omega, terrain_angle, rover, planet, Crr):
    """Returns  the  magnitude  of  the  force  acting  on  the  rover  in  the  direction  of  its  translational 
    motion  due  to  rolling  resistances  given  the  terrain  inclination  angle,  rover  properties,  and  a 
    rolling resistance coefficient. """

    #check parameters, CAN BE A VECTOR
    
    # First check dicts
    if not isinstance(rover, dict) :
        raise Exception('rover is not a valid input type; dict')
    
    if not isinstance(planet, dict) :
        raise Exception('planet is not a valid input type; dict')
    
    if not (isinstance(Crr,(np.number,float,int)) and Crr > 0):
        raise Exception('crr is not a valid input type; positive float, positive int')


    # Get values from dicts
    m = get_mass(rover)   

    # Then check scalars / vectors

    omega_is_scalar = np.isscalar(omega)
    omega_is_vector = isinstance(omega, np.ndarray) and omega.ndim == 1

    if not (omega_is_scalar or omega_is_vector):
        raise Exception('omega must be a scalar or a 1D numpy array (vector)')
   
    terrain_is_scalar = np.isscalar(terrain_angle)
    terrain_is_vector = isinstance(terrain_angle, np.ndarray) and terrain_angle.ndim == 1

    if not (terrain_is_scalar or terrain_is_vector):
        raise Exception('terrain angle must be a scalar or a 1D numpy array (vector)')
    # Check to see if shapes are the same
    if np.shape(omega) != np.shape(terrain_angle):
        raise Exception('omega and terrain angle are not the same size')
    
    # Check angles in terrain_angles, .any checks every array value
    terrain_array = np.asarray(terrain_angle)

    # Must adapt dynamically, if out of range return NaN (?)
    if np.any(terrain_array < - 75) or np.any(terrain_array > 75):
        raise Exception('terrain angle is out of range; -75 to 75 degrees')
    
    # execute calculations for rolling resistance
    # Frr must always oppose motion so it must be negative

    gear_ratio = get_gear_ratio(rover['wheel_assembly']['speed_reducer'])
    radius = rover['wheel_assembly']['wheel']['radius']

    magnitude = Crr * m * planet['g'] * np.cos(np.radians(terrain_angle))
    speed = radius * (omega / gear_ratio)

    Frr_simple = magnitude

    # If it's a single number, math.erf works normally
    if omega_is_scalar:
        Frr = -1 * math.erf(40 * speed) * Frr_simple
        
    # If it's an array, we apply math.erf to each element and convert it back to a numpy array
    else:
        erf_values = np.array([-1 * math.erf(40 * s) for s in speed])
        Frr = erf_values * Frr_simple

    return Frr


def F_net(omega, terrain_angle, rover, planet, Crr):
    """Returns the magnitude of net force acting on the rover in the direction of its translational motion."""

    # check parameters
    if not isinstance(rover, dict):
        raise Exception('rover is not a valid input type; dict')
    
    if not isinstance(planet, dict):
        raise Exception('planet is not a valid input type; dict')
    
    if not (isinstance(Crr, (np.number, float, int)) and Crr > 0):
        raise Exception('crr is not a valid input type; positive float, positive int')

    omega_scalar = np.isscalar(omega)
    terrain_angle_scalar = np.isscalar(terrain_angle)

    if omega_scalar != terrain_angle_scalar: # If they aren't the same
        raise Exception('motor shaft speed and terrain angle must be scalars or arrays of the same size')
    
    if not omega_scalar and np.shape(omega) != np.shape(terrain_angle):
        raise Exception('motor shaft speed and terrain angle are not the same size array')
    
    # check the terrain angle, if array or not
    terrain_array = np.asarray(terrain_angle)
    if np.any(terrain_array < -75) or np.any(terrain_array > 75):
        raise Exception('terrain angle is out of range; -75 to 75 degrees')
        
    # call functions only after inputs are checked
    drive = F_drive(omega, rover)
    gravity = F_gravity(terrain_angle, rover, planet)
    rolling = F_rolling(omega, terrain_angle, rover, planet, Crr)
    
    # calculate and return net force
    Fnet = drive + gravity + rolling

    return Fnet

    
