import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from setup.initialize import logger

# Define the exponential function
def exponential(x, A, B):
    return A * (1-np.exp(x/B))

# Update the x_data to range from -50 to 50 with a step of 2
x_data = np.arange(0, 51, 2)  # X values from 0 to 50 in steps of 2

y_data = np.array([0,0.000000000005042,0.000000000009899,0.000000000014422,0.000000000018517,0.000000000022136,
                   0.0000000000252686,0.0000000000279746,0.0000000000302501,0.000000000032182,0.0000000000337612,
                   0.0000000000350845,0.0000000000361377,0.0000000000369911,0.0000000000377082,0.0000000000382701,
                   0.0000000000387217,0.0000000000391,0.0000000000394076,0.0000000000396643,0.0000000000398856,
                   0.0000000000400887,0.0000000000402337,0.0000000000403726,0.000000000040471,0.0000000000405782])  # Dependent variable (response)
# Scale y-data to handle small values (optional)
scaling_factor = 1e11
y_data = y_data * scaling_factor

# Fit the data to the exponential function
initial_guess = [4, -13]  # Initial guess for the parameters [A, B, C]
params, covariance = curve_fit(exponential, x_data, y_data, p0=initial_guess)

# Extract the fitted parameters
A, B= params

# Print the fitted function parameters
print(f"Fitted exponential function: y = {A:.4f} * (1 - exp(x/{B:.4f}))")

# Generate values from the fitted model
x_fit = np.linspace(min(x_data), max(x_data), 100)
y_fit = exponential(x_fit, *params)

# Plot the data and the fitted curve
plt.scatter(x_data, y_data, label='Sensing electrodes', color='blue')
plt.plot(x_fit, y_fit, label='Exponential Fit', color='red')
plt.xlabel('Amplitude w in µm')
plt.ylabel(r'Electric displacement field delta $\Delta$D(w) in C/m x E11')
plt.legend()
plt.suptitle(r"Fitted exponential function: $\Delta$D(w) = A $\cdot$ [1 - exp(w/B)]")
plt.title(f"A = {A:.1f}\n"
          f"B = {B:.1f}")
plt.show()