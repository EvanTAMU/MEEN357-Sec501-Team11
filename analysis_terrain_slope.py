#call force drive, force gravity, force rolling
#input inclination angle, rover properties, rolling coefficient(.15)
#call defined function net force

import math
import numpy as np
#initialize bounds
def bisec(F_net, xl = 0, xu = 2*math.pi, errTol = 1e-6, iterMax=100, funTol=1e-6)
    # xl = 0
    # xu = 2*math.pi

    iter = 0
    done = False

    # err_Tol = 1e-6
    # iterMax = 100
    # fun_Tol = 1e-6

    while not done:
        iter += 1

        x_bisect = (xu-xl)/2

        fu = F_net(xu)
        fl = F_net(xl)
        f_bisect = F_net(x_bisect)

        if fl * f_bisect < 0:
            fu = f_bisect
        else:
        fl = f_bisect

        error_est = abs((xu-xl)/xr)*100
        if (error_est < errTol) or iterNum >= iterMax or (abs(f_bisect) < funTol):
            done = True
        
