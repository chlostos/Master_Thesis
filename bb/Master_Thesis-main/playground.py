from setup.initialize import config, logger
import pandas as pd
import numpy as np
import matplotlib.pylab as plt

all_measurements = f'{config.get("DIRECTORIES","results")}/{config.get("DIRECTORIES","all_measurements")}'
df = pd.read_excel(all_measurements)
df = df.iloc[:41]

u_vec = df['U']
r_vec = df['R']
u = np.array(u_vec)
r = np.array(r_vec) * 1000  # in mV
E = np.array(u_vec)/5.6 # in kV/m

# create the first plot
fig, ax1 = plt.subplots()
# plot the voltage data
line, = ax1.plot(r, u, marker='.', linestyle='-', color='b', label='Voltage')
plt.gca().invert_xaxis()
ax1.set_xlabel('U_out in mV')
ax1.set_ylabel('Voltage in V')
ax1.grid(True)
# plot first and last value with different marker
ax1.plot(r[0], u[0], marker='^', linestyle='-', color='b', label='first')
ax1.plot(r[-1], u[-1], marker='d', linestyle='-', color='b', label='last')
# create second y-axis
ax2 = ax1.twinx()
# plot the phase data
ax2.plot(r, E, linestyle='-', color='b', label='E-field')
plt.gca().invert_xaxis()
ax2.set_ylabel('E-field in kV/m')

# add legends
label = line.get_label()
# display the plot
plt.title(f'sensor with measurement_box-box_supply at frequency in mode mode on date daytime')

# save the plot to a file
fig.savefig('sensor_date_daytime.png', dpi=300)  # different output formats like .pdf or .svg available

logger.info('Measurement has been finished successfully')
