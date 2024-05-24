import time
import sys

def amplitude_cal(fgen,SR830,u,r_min,sens):  
    u_min = u
    for i in range(11):
        u_now = u - (i-1)*sens
        if u_now < 1:
            break        
        fgen.outputs[1].standard_waveform.amplitude = u_now
        print(f'Nr:{i} {u_now}V')
        time.sleep(1.5)
        r_now = SR830.getR()
        if r_now < r_min:
            r_min = r_now
            u_min = u_now
        elif r_now > (r_min*1.2):
            break
    for i in range(11):
        u_now = u + (i+1)*sens
        if u_now >= 10:
            break
        fgen.outputs[1].standard_waveform.amplitude = u_now
        print(f'Nr:{i} {u_now}V')
        time.sleep(1.5)
        r_now = SR830.getR()
        if r_now < r_min:
            r_min = r_now
            u_min = u_now
        elif r_now > (r_min*1.2):
            break
    print(f'u_min={u_min}V | r_min={r_min*1000}mV')
    return u_min,r_min

def phase_cal(fgen,SR830,ph,r_min,sens):  
    ph_min = ph
    for i in range(11):
        ph_now = ph - (i-1)*sens
        fgen.outputs[1].standard_waveform.start_phase = ph_now
        time.sleep(1.5)
        r_now=SR830.getR()
        print(f'Nr:{i} {ph_now}°') 
        if(r_now<r_min):
            r_min=r_now
            ph_min=ph_now
        elif r_now > (r_min*1.2):
            break
    for i in range(11):
        ph_now = ph + (i+1)*sens
        fgen.outputs[1].standard_waveform.start_phase = ph_now
        time.sleep(1.5)
        r_now=SR830.getR()
        print(f'Nr:{i} {ph_now}°') 
        if(r_now<r_min):
            r_min=r_now
            ph_min=ph_now
        elif r_now > (r_min*1.2):
            break
    print(f'ph_min={ph_min}° | r_min={r_min*1000}mV')
    return ph_min,r_min

def start_calibration(SR830, fgen, f_mech, u0, ph1, ph2):

    fgen.outputs[0].standard_waveform.frequency = f_mech
    fgen.outputs[0].standard_waveform.start_phase = ph1
    fgen.outputs[1].standard_waveform.start_phase = ph2
    fgen.outputs[0].enabled = True
    fgen.outputs[1].enabled = True
    fgen.outputs[0].standard_waveform.amplitude = u0

    SR830.SetRefFreq(f_mech)

    print('start amplitude calibration')
    r_min = 10e9

    # 1 V amplitude calibration        
    u_min_1, r_min_1 = amplitude_cal(fgen,SR830,u0,r_min,1)
    # 100 mV amplitude calibration
    u_min_2, r_min_2 = amplitude_cal(fgen,SR830,u_min_1,r_min_1,0.1)
    # 10° phase calibration
    ph_min_1, r_min_3 = phase_cal(fgen,SR830,ph2,r_min_2,10)
    # 1° phase calibration
    ph_min_2, r_min_4 = phase_cal(fgen,SR830,ph_min_1,r_min_3,1)
    
    
    # 1 V amplitude calibration        
    u_min_3, r_min_5 = amplitude_cal(fgen,SR830,u_min_2,r_min_4,1)
    # 100 mV amplitude calibration
    u_min_4, r_min_6 = amplitude_cal(fgen,SR830,u_min_3,r_min_5,0.1)
    # 10° phase calibration
    ph_min_3, r_min_7 = phase_cal(fgen,SR830,ph_min_2,r_min_6,10)
    # 1° phase calibration
    ph_min_4, r_min_8 = phase_cal(fgen,SR830,ph_min_3,r_min_7,1)
    # 0.1° phase calibration
    ph_min_5, r_min_9 = phase_cal(fgen,SR830,ph_min_4,r_min_8,0.1)
    
    
    # 1 V amplitude calibration        
    u_min_5, r_min_10 = amplitude_cal(fgen,SR830,u_min_4,r_min_9,1)
    # 100 mV amplitude calibration
    u_min_6, r_min_11 = amplitude_cal(fgen,SR830,u_min_5,r_min_10,0.1)
    # 10 mV amplitude calibration
    u_min_7, r_min_12 = amplitude_cal(fgen,SR830,u_min_6,r_min_11,0.01)
    # 1 mV amplitude calibration
    u_min_8, r_min_13 = amplitude_cal(fgen,SR830,u_min_7,r_min_12,0.001)
    # # 10° phase calibration
    ph_min_6, r_min_14 = phase_cal(fgen,SR830,ph_min_5,r_min_13,10)
    # # 1° phase calibration
    ph_min_7, r_min_15 = phase_cal(fgen,SR830,ph_min_6,r_min_14,1)
    # # 0.1° phase calibration
    ph_min_8, r_min_16 = phase_cal(fgen,SR830,ph_min_7,r_min_15,0.1)
    # # 0.01° phase calibration
    ph_min_9, r_min_17 = phase_cal(fgen,SR830,ph_min_8,r_min_16,0.01)
    # # 0.001° phase calibration
    ph_min_10, r_min_18 = phase_cal(fgen,SR830,ph_min_9,r_min_17,0.001)
    
    # 1 mV amplitude calibration
    u_min_9, r_min_19 = amplitude_cal(fgen,SR830,u_min_8,r_min_18,0.001)
    fgen.outputs[1].standard_waveform.amplitude = u_min_9
    fgen.outputs[1].standard_waveform.start_phase = ph_min_10
    print(f'amplitude were set to {u_min_9}V')
    print(f'phase were set to {ph_min_10}°')
    print(f'amplitude: {u_min_9}V @ phase: {ph_min_10}°')
    return u_min_9,ph_min_10
