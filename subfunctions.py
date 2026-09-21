#import libraries
import numpy as np
import matplotlib.pyplot as plt

def tau_dcmotor(omega: np.ndarray | int | float, motor: dict) -> np.ndarray | float | int:
    """Returns  the  motor  shaft  torque  when  given  motor  shaft  speed  
    and  a  dictionary  containing important specifications for the motor"""

    # INPUT CHECKS
    # omega
    if not isinstance(omega,(np.ndarray,np.number,int,float)):
        raise Exception('omega is not a valid input type; np.ndarray, float, int')
    # motor
    if not isinstance(motor,dict):
        raise Exception('motor is not a valid input type; dict')

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
            if (omega[w] >= speed_noload):
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
        if (omega >= speed_noload):
            # Return tau = 0 if wheel is being forced faster than possible
            tau = 0
        else: tau = (torque_stall - (((torque_stall - torque_noload) / speed_noload) * omega))

        return float(tau) # Return a scalar, if input is not nparray

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
        raise Exception('Omega is not a valid input type;  np.ndarray, float, int')
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

    m = get_mass(rover)

    #check parameters
    if not isinstance(omega,(np.number,int,float)):
        raise Exception('omega is not a valid input type; float, int')
    
    if not isinstance(terrain_angle,(np.number,int,float)):
        raise Exception('terrain angle is not a valid input type; float, int')
    
    if not np.shape(omega) == np.shape(terrain_angle):
        raise Exception('omega and terrain angle are not the same size')
    
    if not (-75 <= terrain_angle <= 75) :
        raise Exception('terrain angle is out of range; -75 to 75 degrees')
    
    if not isinstance(rover, dict) :
        raise Exception('rover is not a valid input type; dict')
    
    if not isinstance(planet, dict) :
        raise Exception('planet is not a valid input type; dict')
    
    if not (isinstance(Crr,(np.number,float,int)) and Crr > 0):
        raise Exception('crr is not a valid input type; positive float, positive int')
   
    
    # execute calculations for rolling resistance
    # Frr must always oppose motion so it must be negative
    Frr = -1 * abs(Crr * m * planet['g'] * np.cos(np.radians(terrain_angle))) 

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

    
