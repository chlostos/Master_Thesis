#!/usr/bin/env python3

from help_functions.init_messg import init_sr830, init_fgen, init_hameg
from help_functions.calibration import start_calibration
from help_functions import mess_func
from setup.initialize import config
from setup.initialize import logger
from setup.log_func import log_func
import numpy as np
import matplotlib.pylab as plt

@log_func
def main():
    logger.info('measurement script started')
    
    # initializing lock-in
    SR830 = init_sr830()

    # initializing finction generator  
    fgen = init_fgen()
    
    # initializing power supply
    powersupply = init_hameg()  # 1...5V, 2...12V
    
    # automatic calibration
    auto_cal = config.get("fgen", "auto_calibration")
    
    
    # define measurement setup
    f_mech = float(config.get("fgen", "frequency"))
    measurement_box = config.get("SETUP", "measurement_box")
    x='Test'
    y=f'x'
    
    box_supply = f'{config.get("SETUP", "box_supply")} V'  # supply voltage from powersupply
    sensor = config.get("SETUP", "sensor")
    mode = config.get("SETUP", "mode")
    frequency = f'{f_mech:.3f} Hz'
    d_minus = f'{float(config.get("fgen", "u1")):.3f} V'  # f"{u0}V"  # drive voltage ch1 from function generator
    d_plus = f'{float(config.get("fgen", "u2")):.3f} V'  # f"{u_min}V"   # drive voltage ch2 from function generator
    u1 = float(config.get("fgen", "u1"))
    u2 = float(config.get("fgen", "u2"))
    ph1 = 0
    ph2 = 180
    fgen.outputs[0].standard_waveform.frequency = f_mech
    fgen.outputs[0].standard_waveform.start_phase = ph1
    fgen.outputs[1].standard_waveform.start_phase = ph2
    fgen.outputs[0].standard_waveform.amplitude = u1
    fgen.outputs[1].standard_waveform.amplitude = u2
    fgen.outputs[0].enabled = True
    fgen.outputs[1].enabled = True

    if 'y' in auto_cal:
        u, ph = start_calibration(SR830, fgen)
        d_minus = f'{amplitude:.3f} V'
        d_plus = f'{u:.3f} V'
    t_sleep = float(config.get("MEASUREMENT", "t_sleep"))
    u_max = float(config.get("MEASUREMENT", "u_max"))
    n_meas = int(config.get("MEASUREMENT", "n_meas"))
    n_avg = int(config.get("MEASUREMENT", "n_avg"))
    t_avg = float(config.get("MEASUREMENT", "t_avg"))
    symmetric = config.get("MEASUREMENT", "symmetric")
    measurement_type = input('wolud you like to do a long measurement? (y/n):')
    # start measurement
    if 'y' in measurement_type.lower():
        df, date, daytime = mess_func.long(SR830,powersupply,t_sleep,t_avg,measurement_box,box_supply,sensor,mode,frequency,d_minus,d_plus)
        
    else:
        df, date, daytime = mess_func.create_df(SR830, powersupply, t_sleep, t_avg, u_max, n_meas, n_avg,
                                       symmetric, measurement_box, box_supply, sensor, mode, frequency, d_minus, d_plus)
        
    fgen.outputs[0].enabled = False
    fgen.outputs[1].enabled = False
    powersupply.outputs[0].enabled=False
    powersupply.outputs[1].enabled=False
    powersupply.outputs[2].enabled=False
    u_vec = df['U']
    r_vec = df['R']
    e_vec = df['E']
    t_vec = df['t']
    u = np.array(np.array(u_vec)) # in V
    r = np.array(r_vec) * 1000  # in mV
    E = np.array(e_vec) # in kV/m
    t = np.array(t_vec) # in s
    
    # create the first plot
    fig, ax1 = plt.subplots()
    # plot the voltage data
    line, = ax1.plot(r, u, marker='.', linestyle='-', linewidth=0.5, color='b', label='Voltage')
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
    ax2.plot(r, E, linestyle='-', linewidth=0.1, color='b', label='E-field')
    plt.gca().invert_xaxis()
    ax2.set_ylabel('E-field in kV/m')

    # display the plot
    plt.title(f'{sensor} with {measurement_box}-{box_supply} at {frequency} in mode {mode} on {date} {daytime}')

    # save the plot to a file
    fig.savefig(f'{config.get("DIRECTORIES","results")}/{sensor}_{date}_{daytime}.png', dpi=600)  # different output formats like .pdf or .svg available
    
    logger.info('Measurement has been finished successfully')
    return


if __name__ == "__main__":
    main()
