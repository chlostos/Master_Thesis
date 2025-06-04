import pandas as pd
from datetime import datetime
from help_functions.init_messg import init_sr830
from setup.initialize import logger
from setup.initialize import config
import numpy as np

def meas(SR830, powersupply, t_sleep, t_avg, u_max, n_meas, n_avg, symmetric):
    from setup import log_func
    import matplotlib.pylab as plt
    import time
    
    logger.info('start measurement')
    r_vec = np.array([])
    u_vec = np.array([])
    phi_vec = np.array([])
    t_vec = np.array([])
    i_vec = np.array([])
    u_step_size = u_max / n_meas
    repeat = int(config.get("MEASUREMENT","repeat"))
    i_repeat=0
    t_start = time.time()
    while i_repeat <= repeat:
        if 'y' in symmetric.lower():
            u_now = u_max
            powersupply.outputs[1].enabled=False
            powersupply.outputs[0].voltage_level = u_max
            powersupply.outputs[0].enabled=True
            while u_now > 0:
                powersupply.outputs[0].voltage_level = u_now
                logger.info(f'{i_repeat}. measuring at -{u_now}V...')
                time.sleep(t_sleep)
                r_now = SR830.getR()
                phi_now = SR830.getPhi()
                t_end = time.time()
                # average resistance as the mean of a normal distribution
                if n_avg > 1:
                    r_smpl = []
                    phi_smpl = []
                    for i_avg in range(n_avg):
                        r_smpl.append(SR830.getR())
                        phi_smpl.append(SR830.getPhi())
                        time.sleep(t_avg)
                    t_end = time.time()
                    r_avg = np.mean(r_smpl)
                    phi_avg = np.mean(phi_smpl)
                # no averaging
                else:
                    r_avg = r_now
                    phi_avg = phi_now


                t_total = int(t_end - t_start)
                t_vec=np.append(t_vec, t_total)
                r_vec=np.append(r_vec, r_avg)
                u_vec=np.append(u_vec, ((-1)*u_now))
                phi_vec=np.append(phi_vec, phi_avg)
                i_vec=np.append(i_vec, i_repeat)

                u_now -= u_step_size    

        u_now = 0
        while u_now <= u_max:
            powersupply.outputs[0].enabled=False
            powersupply.outputs[1].voltage_level = u_now
            powersupply.outputs[1].enabled=True
            logger.info(f'{i_repeat}. measuring at {u_now}V')
            time.sleep(t_sleep)
            r_now = SR830.getR()
            phi_now = SR830.getPhi()
            t_end = time.time()
            # average resistance as the mean of a normal distribution
            if n_avg > 1:
                r_smpl = []
                phi_smpl = []
                for i_avg in range(n_avg):
                    r_smpl.append(SR830.getR())
                    phi_smpl.append(SR830.getPhi())
                    time.sleep(t_avg)
                t_end = time.time()
                r_avg = np.mean(r_smpl)
                phi_avg = np.mean(phi_smpl)
            # no averaging
            else:
                r_avg = r_now
                phi_avg = phi_now


            t_total = int(t_end - t_start)
            t_vec=np.append(t_vec, t_total)
            r_vec=np.append(r_vec, r_avg)
            u_vec=np.append(u_vec, u_now)
            phi_vec=np.append(phi_vec, phi_avg)
            i_vec=np.append(i_vec, i_repeat)

            u_now += u_step_size
        
        i_repeat += 1


    return r_vec, u_vec, phi_vec, t_vec, i_vec

def long(SR830,powersupply,t_sleep,t_avg,measurement_box,box_supply,sensor,mode,frequency,d_minus,d_plus):
    from setup import log_func
    import matplotlib.pylab as plt
    import time
    
    logger.info('start long measurement')
    r_vec = np.array([])
    u_vec = np.array([])
    phi_vec = np.array([])
    t_vec  = np.array([])
    n = 0
    time_total=float(config.get("MEASUREMENT","time_total"))
    time_intervall=float(config.get("MEASUREMENT","time_intervall"))
    start_time = time.time()
    while (time.time() - start_time - t_sleep + (time_intervall*60))<= (time_total*60):
        u_now = n % 2
        powersupply.outputs[0].enabled=False
        powersupply.outputs[1].voltage_level = u_now
        powersupply.outputs[1].enabled=True
        logger.info(f'measuring at {u_now}V')
        time.sleep(t_sleep)
        # average resistance as the mean of a normal distribution
        start_time2 = time.time()
        while time.time() - start_time2 - t_avg <= (time_intervall*60):
            r_vec=np.append(r_vec,SR830.getR())
            phi_vec=np.append(phi_vec,SR830.getPhi())
            t_vec=np.append(t_vec,int(time.time()-start_time))
            u_vec=np.append(u_vec, u_now)
            time.sleep(t_avg)

        n += 1
    
    powersupply.outputs[0].voltage_level = 0
    powersupply.outputs[0].enabled=False
    powersupply.outputs[1].voltage_level = 0
    powersupply.outputs[1].enabled=False
    current_datetime = datetime.now()
    current_date = current_datetime.strftime('%d/%m/%Y')
    date = current_datetime.strftime('%d%m%Y')
    current_time = current_datetime.strftime('%H:%M')
    daytime = current_datetime.strftime('%Hh%Mmin')
    distance = float(config.get("MEASUREMENT", "distance"))
    columns = ["date","end time","measurement box","box supply","sensor","mode","frequency","D-","D+","iteration","t","E","U","Phi","R"]
    df = pd.DataFrame(columns=columns)
    df["U"] = u_vec
    df["R"] = r_vec
    df["Phi"] = phi_vec
    df["E"] = list(np.array(u_vec/distance))
    df["t"] = t_vec
    df["end time"] = current_time
    df["date"] = current_date
    df["measurement box"] = measurement_box
    df["box supply"] = box_supply
    df["sensor"] = sensor
    df["mode"] = mode
    df["frequency"] = frequency
    df["D-"] = d_minus
    df["D+"] = d_plus
    file_name = f'{config.get("DIRECTORIES","results")}/{sensor}_{date}_{daytime}.xlsx'
    df.to_excel(file_name, index=False)
    logger.info(f'measurement successfully saved as {file_name}')
    '''all_measurements = f'{config.get("DIRECTORIES","results")}/{config.get("DIRECTORIES","all_measurements")}'
    df0 = pd.read_excel(all_measurements)
    df0 = pd.concat([df0,df])
    df0.to_excel(all_measurements, index=False)'''
    logger.info(f'measurement data base has been updated')
    
    return df,date,daytime

def create_df(SR830,powersupply,t_sleep,t_avg,u_max,n_meas,n_avg,symmetric,measurement_box,box_supply,sensor,mode,frequency,d_minus,d_plus):
    
    r_vec, u_vec, phi_vec, t_vec, i_vec = meas(SR830, powersupply, t_sleep, t_avg, u_max, n_meas, n_avg, symmetric)
    
    powersupply.outputs[0].voltage_level = 0
    powersupply.outputs[0].enabled=False
    powersupply.outputs[1].voltage_level = 0
    powersupply.outputs[1].enabled=False
    current_datetime = datetime.now()
    current_date = current_datetime.strftime('%d/%m/%Y')
    date = current_datetime.strftime('%d%m%Y')
    current_time = current_datetime.strftime('%H:%M')
    daytime = current_datetime.strftime('%Hh%Mmin')
    distance = float(config.get("MEASUREMENT", "distance"))
    columns = ["date","end time","measurement box","box supply","sensor","mode","frequency","D-","D+","iteration","t","E","U","R","Phi"]
    df = pd.DataFrame(columns=columns)
    df["U"] = u_vec
    df["R"] = r_vec
    df["Phi"] = phi_vec
    df["E"] = list(np.array(u_vec/distance))
    df["t"] = t_vec
    df["iteration"] = i_vec
    df["end time"] = current_time
    df["date"] = current_date
    df["measurement box"] = measurement_box
    df["box supply"] = box_supply
    df["sensor"] = sensor
    df["mode"] = mode
    df["frequency"] = frequency
    df["D-"] = d_minus
    df["D+"] = d_plus
    file_name = f'{config.get("DIRECTORIES","results")}/{sensor}_{date}_{daytime}.xlsx'
    df.to_excel(file_name, index=False)
    logger.info(f'measurement successfully saved as {file_name}')
    all_measurements = f'{config.get("DIRECTORIES","results")}/{config.get("DIRECTORIES","all_measurements")}'
    df0 = pd.read_excel(all_measurements)
    df0 = pd.concat([df0,df])
    df0.to_excel(all_measurements, index=False)
    logger.info(f'measurement data base has been updated')
    
    return df,date,daytime