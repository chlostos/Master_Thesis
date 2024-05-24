import pandas as pd
from datetime import datetime
from init_messg import init_sr830
import time

def meas(sens, i,powersupply, time_const, t_sleep, t_avg, u_max, n_meas, n_avg, symetric, measurement_box, box_supply, sensor, mode, frequency, d_minus, d_plus):
    import time
    import numpy as np
    import matplotlib.pylab as plt

    SR830 = init_sr830(sens,i,time_const)
    print('time const were set')
    time.sleep(t_sleep)
    r_vec = np.array([])
    u_vec = np.array([])
    phi_vec = np.array([])
    time_elapsed = []
    u_step_size = u_max / n_meas

    
    
    if symetric:
        u_now = u_max
        powersupply.outputs[1].enabled=False
        powersupply.outputs[0].voltage_level = u_max
        powersupply.outputs[0].enabled=True
        print('start symmetric measurement')
        
        while u_now > 0:
            powersupply.outputs[0].voltage_level = u_now
            print(f'measuring at -{u_now}V...')
            time.sleep(t_sleep)
            r_now = SR830.getR()
            phi_now = SR830.getPhi()
            print(f'{r_now*1E6}uV {phi_now}°')
            # average resistance as the mean of a normal distribution
            if n_avg > 0:
                r_smpl = []
                phi_smpl = []
                print('aquiering mean')
                start_time1 = time.time()
                for i_avg in range(n_avg):
                    r_smpl.append(SR830.getR())
                    time.sleep(t_avg)
                    phi_smpl.append(SR830.getPhi())
                    time.sleep(t_avg)
                end_time1 = time.time()
                r_avg = np.mean(r_smpl)
                phi_avg = np.mean(phi_smpl)
                # calculate real time constant in ms
                elapsed_time1 = end_time1-start_time1
                avg_time = elapsed_time1/n_avg * 1000
                time_elapsed.append(avg_time)
            # no averaging
            else:
                r_avg = r_now
                phi_avg = phi_now


            r_vec=np.append(r_vec, r_avg)
            u_vec=np.append(u_vec, ((-1)*u_now))
            phi_vec=np.append(phi_vec, phi_avg)
            print(u_now,r_now) 

            u_now -= u_step_size    

    u_now = 0
    while u_now <= u_max:
        powersupply.outputs[0].enabled=False
        powersupply.outputs[1].voltage_level = u_now
        powersupply.outputs[1].enabled=True
        print(f'measuring at {u_now}V')
        time.sleep(t_sleep)
        r_now = SR830.getR()
        phi_now = SR830.getPhi()
        print(f'{r_now*1E6}uV {phi_now}°')
        # average resistance as the mean of a normal distribution
        if n_avg > 0:
            r_smpl = []
            phi_smpl = []
            print('aquiering mean')
            start_time2 = time.time()
            for i_avg in range(n_avg):
                r_smpl.append(SR830.getR())
                time.sleep(t_avg)
                phi_smpl.append(SR830.getPhi())
                time.sleep(t_avg)
            end_time2 = time.time()
            elapsed_time2 = end_time2-start_time2
            avg_time = elapsed_time2/n_avg * 1000
            time_elapsed.append(avg_time)
            r_avg = np.mean(r_smpl)
            phi_avg = np.mean(phi_smpl)
        # no averaging
        else:
            r_avg = r_now
            phi_avg = phi_now


        r_vec=np.append(r_vec, r_avg)
        u_vec=np.append(u_vec, u_now)
        phi_vec=np.append(phi_vec, phi_avg)
        print(u_now,r_now) 

        u_now += u_step_size
    elapsed_time_mean = np.mean(time_elapsed)
    elapsed_time_max = np.max(time_elapsed)
    elapsed_time_min = np.min(time_elapsed)
    powersupply.outputs[0].voltage_level = 0
    powersupply.outputs[0].enabled=False
    powersupply.outputs[1].voltage_level = 0
    powersupply.outputs[1].enabled=False
    current_datetime = datetime.now()
    current_date = current_datetime.strftime('%d/%m/%Y')
    date = current_datetime.strftime('%d%m%Y')
    current_time = current_datetime.strftime('%H:%M')
    time = current_datetime.strftime('%Hh%Mmin')
    columns = ["date","time","measurement box","box supply","sensor","mode","frequency","D-","D+","U","R","Phi"]
    df = pd.DataFrame(columns=columns)
    df["U"] = u_vec
    df["R"] = r_vec
    df["Phi"] = phi_vec
    df["time"] = current_time
    df["date"] = current_date
    df["measurement box"] = measurement_box
    df["box supply"] = box_supply
    df["sensor"] = sensor
    df["mode"] = mode
    df["frequency"] = frequency
    df["D-"] = d_minus
    df["D+"] = d_plus
    file_name = f'{sensor}_{date}_{time}.xlsx'
    df.to_excel(file_name, index=False)
    print(f'measurement successfully saved as {file_name}')
    df0 = pd.read_excel('all_measurements.xlsx')
    df0 = pd.concat([df0,df])
    df0.to_excel('all_measurements.xlsx', index=False)
    print(f'measurement data base has been updated')
    print(f'real time constant mean: {elapsed_time_mean}ms\n'
          f'real time constant max:  {elapsed_time_max}ms\n'
          f'real time constant min:  {elapsed_time_min}ms')
    
    return df,date,time