#import libraries
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from scipy.integrate import solve_ivp
from scipy.integrate import simpson 
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
        raise Exception('omega must be a scalar or a 1D numpy array (vector)')

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
        raise Exception('Crr must be a positive scalar')

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

# ===================--------===================
# ===================-PART 2-===================
# ===================--------===================

def motorW(v, rover):
    """Computes the rotational speed of the motor shaft [rad/s] given the translational
    velocity of the rover and the rover dictionary"""
    # v is scalar/float or 1D array
    # rover is dict

    # Should call get_gear_ratio

    # w = (v / r)

    # Used rewritten code for dcmotor with key checker
    if not isinstance(rover,dict):
        raise Exception('rover is not a valid input type; dict')
    
    required_keys = ["wheel_assembly"]
    if not all(key in rover for key in required_keys):
        raise Exception('rover dictionary is missing required specifications')
    
    is_scalar = np.isscalar(v)
    is_vector = isinstance(v, np.ndarray) and v.ndim == 1

    if not (is_scalar or is_vector):
        raise Exception('v must be a scalar or a 1D numpy array (vector)')

    # Get motor/wheel propertires
    gear_ratio = get_gear_ratio(rover["wheel_assembly"]["speed_reducer"])
    radius = rover["wheel_assembly"]["wheel"]["radius"]

    w = (v / radius) * gear_ratio

    if is_scalar:
        return float(w)
    else:
        return np.asarray(w)

def rover_dynamics(t,y,rover,planet,experiment):
    """This function computes the derivative of the state vector (state vector is:[velocity, position]) for the
    rover given its current state. It requires rover and experiment dictionary input parameters. It is
    intended to be passed to an ODE solver."""
    # t is scalar
    # y is a 1D array
    # rover, planet, experiment are dict

    # check rover
    if not isinstance(rover, dict):
        raise Exception('rover is not a valid input type; dict')
    
    # check planet
    if not isinstance(planet, dict):
        raise Exception('planet is not a valid input type; dict')
    
    # check experiment
    if not isinstance(experiment, dict):
        raise Exception('experiment is not a valid input type; dict')
    
    #check t is scalar
    if not np.isscalar(t):
        raise Exception('t must be a scalar')
    
    # check y is a 1D array
    if not (isinstance(y, np.ndarray) and y.ndim == 1):
        raise Exception('y must be a 1D numpy array')

    # y = [velocity, position]
    # dydt = [acceleration, velocity]

    # state variables
    v = y[0]
    p = y[1]

    # calculate F_net.
        # gravitational and rolling resistance froces are funtions of alpha but otherwise independent of vehicle dynamics
        # drive Force is a function of rover dynamical behavior

    # define angular velocity
    omega = motorW(v,rover)

    # define terrain angle as interpolated value from dictionary containing arrays of position and angle
    # may need to define alpha fun in experiment to optimize 
    alpha_dist = experiment['alpha_dist']
    alpha_deg = experiment['alpha_deg']
    alpha_fun = interp1d(alpha_dist, alpha_deg, kind = "cubic", fill_value = 'extrapolate') # fit the cubic spline
    terrain_angle = alpha_fun(p)

    # define Crr
    Crr = experiment['Crr']

    # define F_net by calling the sub function F_net
    F_net = F_net(omega, terrain_angle, rover, planet, Crr) 


    # call get_mass to get the total mass of the rover. non dynamic 
    rover_mass = get_mass(rover)

    # define acceleration
    acceleration = F_net/rover_mass

    # define dydt with acceleration and velocity 
    dydt = np.array([acceleration, y[0]])
    return dydt

def mechpower(v, rover):
    """This function computes the instantaneous mechanical power output by a 
    single DC motor at each point in a given velocity profile."""
    # v is scalar/float or arrary
    # rover is dict

    # Used rewritten code for dcmotor with key checker
    if not isinstance(rover,dict):
        raise Exception('rover is not a valid input type; dict')
    
    required_keys = ["wheel_assembly"]
    if not all(key in rover for key in required_keys):
        raise Exception('rover dictionary is missing required specifications')
    
    is_scalar = np.isscalar(v)
    is_vector = isinstance(v, np.ndarray) and v.ndim == 1

    if not (is_scalar or is_vector):
        raise Exception('v must be a scalar or a 1D numpy array (vector)')

    # Get motor/wheel propertires
    motor_speed = motorW(v,rover) # comes back as scalar or an array
    motor_torque = tau_dcmotor(motor_speed, rover["wheel_assembly"]["motor"]) # returns with a scalar or an arrary

    P = motor_speed*motor_torque

    if is_scalar:
        return float(P)
    else:
        return np.asarray(P)

def battenergy(t,v,rover):
    # computes the total energy consumed, in Joules, from the rover batteries over the course of a simulation run
    # t is 1D numpy array is the time vector from the simulation
    # v is 1D numpy array is the velocity vector from the simulation
    #This function accounts for the inefficiencies of transforming electrical energy to mechanical energy using a DCmotor
    # rover is a dict

    # Data input checks
    if not isinstance(rover,dict):
            raise Exception('rover is not a valid input type; dict')

    if not isinstance(t,np.ndarray) or t.ndim != 1:
        raise Exception('t is not a valid input type; 1D array')

    if not isinstance(v,np.ndarray) or v.ndim != 1:
        raise Exception('v is not a valid input type; 1D array')

    if len(v) != len(t) : 
        raise Exception('v and t are not the same length')

    # process: 1. find power_batt, 2. integrate power_batt

    #define parameters for p_mech and tau_dcmotor
    motor = rover['wheel_assembly']['motor']
    omega = motorW(v,rover)

    # power from motor
    p_mech = mechpower(v,rover)
    tau = tau_dcmotor(omega, motor) 

    # cubic spline interp1d(x, y, kind='linear', axis=-1, copy=True, bounds_error=None, fill_value=nan, assume_sorted=False)
    effcy_tau = rover["wheel_assembly"]["motor"]["effcy_tau"]
    effcy = rover["wheel_assembly"]["motor"]["effcy"]
    effcy_fun = interp1d(effcy_tau, effcy, kind = 'cubic')

    # find effcy_fun for tau
    n = effcy_fun(tau)

    # define battery power as function of motor power and efficiency at tau. *6 because 6 wheels
    power_batt = 6 * p_mech/(n) #this is the power demand 

    # potential divide by zero bug that will need fixing

    # integrate p_batt over time using simppsons rule
    E = simpson(power_batt, x=t) 

    return E


# The BIG subfunction, runs the simulation!
def simulate_rover(rover,planet,experiment,end_event):
    # uses an ODE to integrate. 

    # what does it do
        # integrates trajectory rover according to terrain and initial conditions
        # defines necessary and sifficient conditions to terminate simulation
    rover 
    planet
    experiment 
    end_event

    # update rover['telemetry']
    time = N_element array 
    completion_time = time to complete mission 
    velocity = N element array containing velocity of rover 
    position = N-element array containing the position of the rover
    distance_traveled = total distance traveled by the rover
    max_velocity = maxium velocity 
    avergae_velocity = avergage velocity along given trajectory 
    power = N-element array of instantaneous power outputted by the motor along the trajectory 
    battery_energy = total energy extracted from the battery to complete trajectory
    energy_per_distance = total energy spent

    return rover # dict, fill with telemetry data!

def end_of_mission_event(end_event):
    """
    Defines an event that terminates the mission simulation. Mission is over
    when rover reaches a certain distance, has moved for a maximum simulation 
    time or has reached a minimum velocity.            
    """
    
    mission_distance = end_event['max_distance']
    mission_max_time = end_event['max_time']
    mission_min_velocity = end_event['min_velocity']
    
    # Assume that y[1] is the distance traveled
    distance_left = lambda t,y: mission_distance - y[1]
    distance_left.terminal = True
    
    time_left = lambda t,y: mission_max_time - t
    time_left.terminal = True
    
    velocity_threshold = lambda t,y: y[0] - mission_min_velocity;
    velocity_threshold.terminal = True
    velocity_threshold.direction = -1
    
    # terminal indicates whether any of the conditions can lead to the
    # termination of the ODE solver. In this case all conditions can terminate
    # the simulation independently.
    
    # direction indicates whether the direction along which the different
    # conditions is reached matters or does not matter. In this case, only
    # the direction in which the velocity treshold is arrived at matters
    # (negative)
    
    events = [distance_left, time_left, velocity_threshold]
    
    return events