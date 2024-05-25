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
    sensitivity = int(config.get("SR830", "sensitivity"))   # 23...100mV, 22...50mV, 21...20mV, 20...10mV, 19...5mV
    i = int(config.get("SR830", "signal_input"))             # signal input: 0...A, 1...A-B
    time_const = int(config.get("SR830", "signal_input"))     # 4...1ms, 5...3ms, 6...10ms, 7...30ms, 8...100ms, 9...300ms
    SR830 = init_sr830(sensitivity, i, time_const)
    reset = input('would you like to reset the function generator? press (y/n): ')
    fgen = init_fgen(reset)
    supply = int(config.get("hameg", "supply"))
    powersupply = init_hameg(supply)  # 1...5V, 2...12V
    auto_cal = config.get("fgen", "auto_calibration")
    frequency = float(config.get("fgen", "frequency"))
    # define measurement setup
    measurement_box = config.get("SETUP", "measurement_box")
    box_supply = f'{config.get("SETUP", "box_supply")} V'  # supply voltage from powersupply
    sensor = config.get("SETUP", "sensor")
    mode = config.get("SETUP", "mode")
    frequency = f'{frequency:.3f} Hz'
    d_minus = f'{float(config.get("SETUP", "d_minus")):.3f} V'  # f"{u0}V"  # drive voltage ch1 from function generator
    d_plus = f'{float(config.get("SETUP", "d_plus")):.3f} V'  # f"{u_min}V"   # drive voltage ch2 from function generator
    if 'y' in auto_cal:
        amplitude = float(config.get("fgen", "amplitude"))
        u, ph = start_calibration(SR830, fgen, frequency, amplitude)
        d_minus = f'{amplitude:.3f} V'
        d_plus = f'{u:.3f} V'
    t_sleep = float(config.get("MEASUREMENT", "t_steep"))
    u_max = float(config.get("MEASUREMENT", "u_max"))
    n_meas = float(config.get("MEASUREMENT", "u_meas"))
    n_avg = float(config.get("MEASUREMENT", "n_avg"))
    t_avg = float(config.get("MEASUREMENT", "t_avg"))
    symmetric = config.get("MEASUREMENT", "symmetric")
    df, date, daytime = mess_func.meas(sensitivity, i, powersupply, time_const, t_sleep, t_avg, u_max, n_meas, n_avg,
                                       symmetric, measurement_box, box_supply, sensor, mode, frequency, d_minus, d_plus)
    u_vec = df['U']
    r_vec = df['R']
    phi_vec = df['Phi']

    u = np.array(np.array(u_vec))  # np.array((np.array(u_vec))/(distance*1000)) # in kV/m
    r = np.array(r_vec) * 1000  # in mV
    phi = np.array(phi_vec)

    # create the first plot
    fig, ax1 = plt.subplots()
    # plot the voltage data
    line1, = ax1.plot(u, r, 'b-', label='U_out')
    ax1.set_xlabel('Voltage [V]')
    ax1.set_ylabel('U_out [mV]', color='b')
    ax1.tick_params(axis='y', labelcolor='b')
    ax1.grid(True)
    # create second y-axis
    ax2 = ax1.twinx()
    # plot the phase data
    line2, = ax2.plot(u, phi, 'r-', label='Phi_out')
    ax2.set_ylabel('Phi_out [°]', color='r')
    ax2.tick_params(axis='y', labelcolor='r')
    # add legends
    lines = [line1, line2]
    labels = [line.get_label() for line in lines]
    ax1.legend(lines, labels, loc='lower left')

    # display the plot
    plt.title(f'{sensor} with {measurement_box}-{box_supply} at {frequency} in mode {mode} on {date} {daytime}')
    plt.show()
    # save the plot to a file
    fig.savefig(f"{sensor}_{date}_{daytime}.png", dpi=300)  # different output formats like .pdf or .svg available
    logger.info('Measurement has been finished successfully')
    return


if __name__ == "__main__":
    main()