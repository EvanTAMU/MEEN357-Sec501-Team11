import math
import numpy as np

#set parameters
slope_array_degs = numpy.linspace(-15,35,25)
Crr = .015

#store vmax values
vmax_values = []

for slope_array_deg in slope_array_degs:
    #find omega when net force equals 0
    f = lambda omega: F_net(omega, terrain_angle, rover, planet, Crr)

    #bisect for omega root
    omega_root = bisect(omega, 0, 3.8)
    #convert omega when net force is 0 to translational velocity
    #w_wheel = w_shaft/gear_ratio
    #r = .3m
    #v = w_wheel * r
    v_max = (omega_root/get_gear_ratio(speed_reducer))*(.3)

    #append each vmax throughout the for loop
    vmax_values.append(v_max)


#plot vmax vs slope
import matplotlib.pyplot as plt
plt.plot(vmax_values,slope_array_degs)
plt.xlabel('Incline Angle: degrees')
plt.ylabel('Maximum Velocity: m/s')




#SCRATCH
# #initialize bounds
# def bisec(F_net, xl = 0, xu = 2*math.pi, errTol = 1e-6, iterMax=100, funTol=1e-6)
#     # xl = 0
#     # xu = 2*math.pi

#     iter = 0
#     done = False

#     # err_Tol = 1e-6
#     # iterMax = 100
#     # fun_Tol = 1e-6

#     while not done:
#         iter += 1

#         x_bisect = (xu-xl)/2

#         fu = F_net(xu)
#         fl = F_net(xl)
#         f_bisect = F_net(x_bisect)

#         if fl * f_bisect < 0:
#             fu = f_bisect
#         else:
#         fl = f_bisect

#         error_est = abs((xu-xl)/xr)*100
#         if (error_est < errTol) or iterNum >= iterMax or (abs(f_bisect) < funTol):
#             done = True
        


