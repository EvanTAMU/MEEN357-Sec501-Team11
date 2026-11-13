# Added graph for data visualization

import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate as interp

# Experimental data from PDF table
mach = np.array([
    0.25, 0.5, 0.65, 0.7, 0.8, 0.9, 0.95, 1.0, 1.1, 1.2,
    1.3, 1.4, 1.5, 1.6, 1.8, 1.9, 2.0, 2.2, 2.5, 2.6
])

mef = np.array([
    1.0, 1.0, 1.0, 0.97, 0.91, 0.72, 0.66, 0.75, 0.90, 0.96,
    0.990, 0.999, 0.992, 0.98, 0.91, 0.85, 0.82, 0.75, 0.64, 0.62
])

# Piecewise linear interpolation model with clamped boundary fill values
mef_interp = interp.interp1d(mach, mef, kind='linear', bounds_error=False, fill_value=(1.0, 0.62))

# Generate continuous Mach domain (including regions < 0.25 and > 2.6 to show clamping)
mach_continuous = np.linspace(0.0, 3.0, 500)
mef_continuous = mef_interp(mach_continuous)

plt.figure(figsize=(8, 4.5))
plt.plot(mach_continuous, mef_continuous, 'b-', linewidth=1.8, label='Continuous Linear Interpolation (mef_interp)')
plt.scatter(mach, mef, color='red', zorder=5, label='Experimental Test Data')
plt.title('Continuous Mach Efficiency Factor (MEF) Model vs. Mach Number')
plt.xlabel('Mach Number, M [-]')
plt.ylabel('Mach Efficiency Factor, MEF [-]')
plt.ylim([0.55, 1.05])
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()