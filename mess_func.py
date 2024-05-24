import pandas as pd
from datetime import datetime

def meas(SR830, powersupply, time_const, t_sleep, t_avg, u_max, n_meas, n_avg, symetric, measurement_box, box_supply, sensor, mode, frequency, d_minus, d_plus):
    import time
    import numpy as np
    import matplotlib.pylab as plt

    SR830.SetTimeConst(time_const)  # 8..100ms; 9..300ms; 10...1s; 11...3s
    time.sleep(t_sleep)
    r_vec = np.array([])
    u_vec = np.array([])
    phi_vec = np.array([])

    u_step_size = u_max / n_meas

    
    
    if symetric:
        u_now = u_max
        powersupply.outputs[1].enabled=False
        powersupply.outputs[0].voltage_level = u_max
        powersupply.outputs[0].enabled=True
        time.sleep(t_sleep)
        
        while u_now > 0:
            powersupply.outputs[0].voltage_level = u_now
            
            #if ((n%40)==0):
            #    SR830.SetSensitivityLIA()
            time.sleep(t_sleep)
            r_now = SR830.getR()
            phi_now = SR830.getPhi()
            
            # average resistance as the mean of a normal distribution
            if n_avg > 0:
                r_smpl = []
                phi_smpl = []
                for i_avg in range(n_avg-1):
                    time.sleep(t_avg)
                    r_smpl.append(SR830.getR())
                    phi_smpl.append(SR830.getPhi())
                r_avg = np.mean(r_smpl)
                phi_avg = np.mean(phi_smpl)
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
        
        #if ((n%40)==0):
        #    SR830.SetSensitivityLIA()

        time.sleep(t_sleep)
        r_now = SR830.getR()
        phi_now = SR830.getPhi()
        
        # average resistance as the mean of a normal distribution
        if n_avg > 0:
            r_smpl = []
            phi_smpl = []
            for i_avg in range(n_avg-1):
                time.sleep(t_avg)
                r_smpl.append(SR830.getR())
                phi_smpl.append(SR830.getPhi())
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
    
    return df,date,time