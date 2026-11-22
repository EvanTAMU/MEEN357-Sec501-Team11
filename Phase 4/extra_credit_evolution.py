"""
Evolutionary Optimizer using SciPy's mixed-integer differential_evolution package
"""

from scipy.optimize import differential_evolution, minimize # Bread and butter optimizer and minimizer for data
import numpy as np
import copy
import pickle
import csv
import os

from subfunctions_Phase4 import (
    define_batt_pack, define_chassis, define_edl_system,
      define_mission_events, define_motor, define_planet, define_rover, 
      get_cost_edl, get_cost_rover, F_rollingCorr , simulate_edl, simulate_rover, 
      end_of_mission_event, update_edl_state, redefine_edl_system)

from define_experiment import experiment1

# differential_evolution needs multiple parameters for this setup
# Define the function, bounds, arguments, integrality, constraints, seed etc...
# Start by gathering these values

MOTORS = ['base','base_he','torque','torque_he','speed','speed_he']
CHASSIS = ['steel','magnesium'] # DROP CARBON, STUPID EXPENSIVE
BATTERIES = ['LiFePO4','NiMH','NiCD','PbAcid-1','PbAcid-2','PbAcid-3']

BOUNDS = [
    (14.0, 19.0), # parachute diameter (m)
    (0.2, 0.7), # wheel radius (m)
    (250.0, 800.0), # chassis mass (kg)
    (0.05, 0.12), # gear diameter d2 (m)
    (100.0, 290.0), # fuel mass (kg)
    (0, len(CHASSIS) - 1), # Chasis materials
    (0, len(MOTORS) - 1), # Motor types
    (0, len(BATTERIES) - 1), # Battery types
    (1,45), # number of battery packs
]

INTEGRALITY = [0,0,0,0,0,1,1,1,1] # 1 for discrete, 0 for continuous

INITAL_CONDITIONS = [

]

HARD_CONSTRAINTS = [
    40_000, # Min Chassis strength (mpa)
    7.2e6,  # Max Cost ($)
    1,      # Max touchdown speed (m/s)
    1000,   # Distance traveled
]

 # define random terrain
def make_terrain(n_random = 5, seed=42):
    """Returns modified environments for training. 
    Random angle spikes at random locations along environment"""
    rng = np.random.default_rng(seed)
    base_exp, end_event = experiment1()
    exp_final = [copy.deepcopy(base_exp)]

    n_pts = len(base_exp['alpha_dist'])

    for _ in range(n_random):
        exp = copy.deepcopy(base_exp) # Copy the exp dict
        angles = rng.normal(loc=5.5, scale=5.5, size=n_pts) # choose random angels
        spikes = rng.choice(n_pts, size=rng.integers(1,3), replace=False) # choose random angle locations
        angles[spikes] += rng.uniform(4.0, 10.0, size=len(spikes))
        exp['alpha_deg'] = np.clip(angles, -10.0, 24.0)
        exp_final.append(exp)
    return exp_final, end_event # returns modified environment, random angle spikes at random locations


# Build edl dict with chosen bounds
# x = [chute_d, wheel_r, chassis_m, d2, fuel_m, chassis_i, motor_i, batt_i, batt_n]
def build_edl(x):
    """Build EDL with selected values"""
    edl = define_edl_system()                                           # Baseline
    edl['parachute']['diameter'] = x[0]                                 # chute_d
    edl['rover']['wheel_assembly']['wheel']['radius'] = x[1]            # wheel_r
    edl['rover']['chassis']['mass'] = x[2]                              # chassis_m
    edl['rover']['wheel_assembly']['speed_reducer']['diam_gear'] = x[3] # d2
    edl["rocket"]["initial_fuel_mass"] = x[4]                           # fuel_m (inital mass)
    edl["rocket"]["fuel_mass"] = x[4]                                   # fuel_m
    edl = define_chassis(edl, CHASSIS[int(round(x[5]))])                # chassis_i
    edl = define_motor(edl, MOTORS[int(round(x[6]))])                   # motor_i
    edl = define_batt_pack(edl, BATTERIES[int(round(x[7]))], int(round(x[8]))) # batt_i, batt_n

    return redefine_edl_system(edl)

def objective(x, terrain, end_event):
    edl = build_edl(x)

    # Check constraints, capacity, speed, etc...
    strength = edl['rover']['chassis']['strength']
    cost = get_cost_edl(edl)
    # Check required stat values for early return
    if strength < HARD_CONSTRAINTS[0] or cost > HARD_CONSTRAINTS[1]:
        # Return poor score 
        # Too little strength? return value based on amount under
        # same with cost but reverse
        return 1e5 + max(0, HARD_CONSTRAINTS[0] - strength) + max(0, (cost - HARD_CONSTRAINTS[1])/ 100.0) 

    # EDL simulation
    planet = define_planet()
    events = define_mission_events()
    try:
        t_edl_arr, _, edl_post = simulate_edl(edl,planet,events, 5000, False)
    except:
        # if there is an error with simualtion, return poor score
        return 5e5

    # Rover touchdown failure
    td_speed = edl_post.get('rover_touchdown_speed', 999.0)
    if (
        not edl_post['rover']['on_ground'] # if its not on the ground
        or abs(td_speed) > HARD_CONSTRAINTS[2] # is too fast on touchdown
        or abs(edl_post['velocity']) > HARD_CONSTRAINTS[2] # is too fast after touchdown
        or edl_post['altitude'] < edl_post['sky_crane']['danger_altitude'] # triggered sky crane too late
    ): 
        return 5e4 + 5e3 * abs(td_speed) # score based on touchdown speed

    # Terrain simulation
    # battery max charge
    max_e_per_m = (edl_post['rover']['power_subsys']['battery']['capacity'] * 0.95) / end_event['max_distance']
    times = []
    penalty = 0.0

    for exp in terrain:
        try:
            rov = simulate_rover(copy.deepcopy(edl_post['rover']), planet, exp, end_event)
        except Exception:
            return 5e4 # if error return poor score
        
        # check rover output data
        tel = rov['telemetry'] # rov telemetry
        # check is distance traveled is under max distance (min maxing)
        # if the rover goes over max distance, it is TOO MUCH, can use less
        if tel['distance_traveled'] < end_event['max_distance'] - 1.0:
            # flat value times the distance over
            penalty += 2e4 * (1.0 + (end_event["max_distance"] - tel["distance_traveled"]) / 1000.0)
        if tel['energy_per_distance'] > max_e_per_m:
            penalty += 1e4 * (1.0 + (tel["energy_per_distance"] - max_e_per_m) / max_e_per_m)
        # append completion time of rover
        times.append(tel['completion_time'])

    # if there is a penalty, punish harder
    if penalty > 0:
        return float(t_edl_arr[-1] + np.mean(times) + penalty)

    # return normally without penalty
    return float(t_edl_arr[-1] + 0.75 * np.mean(times) + 0.25 * np.max(times))

# Run the functions!
if __name__ == '__main__':

    SEED_T = 42 # terrain seed
    SEED_E = 42 # evolution seed

    terrains, end_event = make_terrain(n_random=5, seed=SEED_T)

    # time to apply all the values
    res = differential_evolution(
        func= objective,            # main function
        bounds=BOUNDS,              # bounds of function
        integrality=INTEGRALITY,    # what values are continious/discrete
        args=(terrains, end_event), # arguments for function
        popsize=10,                 # total population = popsize * len(BOUNDS)
        maxiter=25,                 # maximum number of generations over which the entire population is evolved
        workers=-1,                 # CPU cores
        updating='deferred',        # needed for workers = -1
        polish = False,             # polish final choice
        disp = True,                # prints out function every iteration
        seed = SEED_E,              # Seed, changes random values
    )

    # get values from output
    # display to console and CSV to run multiple trials
    best_edl = build_edl(res.x)
    

    
    print(f"\nBest Score: {res.fun:.2f}s | Cost: ${get_cost_edl(best_edl):,.0f}")
    print(
        f"Discrete: {CHASSIS[int(round(res.x[5]))]}, "
        f"{MOTORS[int(round(res.x[6]))]}, "
        f"{BATTERIES[int(round(res.x[7]))]} x {int(round(res.x[8]))}"
    )
    print(
        f"Continuous: chute={res.x[0]:.3f}m, r={res.x[1]:.3f}m, "
        f"chassis_m={res.x[2]:.1f}kg, d2={res.x[3]:.4f}m, fuel={res.x[4]:.1f}kg"
    )

    best_edl["team_name"] = "EvoRover"
    best_edl["team_number"] = 11
    with open("evo_best_rover.pickle", "wb") as f:
        pickle.dump(best_edl, f, protocol=pickle.HIGHEST_PROTOCOL)
