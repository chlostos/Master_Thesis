import ivi
import time
import sys

def init_sr830(sens,input_config,time_const):
    # initialize lock-in amplifier
    SR830 = ivi.stanford.stanfordSR830()
    SR830.Reset()
    SR830.SetRefPhas(0)
    #SR830.SetRefFreq(f_mech)
    SR830.SetRefMode(0) # internal 1; external 0
    SR830.SetRefHarm(1)
    SR830.SetInputConfig(input_config)  # i selects A (i=0), A-B (i=1), I (1 MΩ) (i=2) or I (100 MΩ) (i=3)
    SR830.SetGNDConfig(0)  # Float (gndconf=0) or Ground (gndconf=1)
    SR830.SetInputCoupling(0)  # i selects AC (i=0) or DC (i=1)[1]
    SR830.SetTimeConst(time_const)  # 8..100ms; 10...1s; 11...3s
    SR830.SetReserve(1)  # Normal
    SR830.SetTriggerSlope(0)  # 0..sine
    SR830.SetSens(sens)  # 22..50mV
    SR830.SetDisplay(1, 1) # setting display to r and phi
    SR830.SetDisplay(2, 1)
    print('lock-in ready')
    return SR830

def init_fgen(reset=True):
    # initialize function generator
    fgen = ivi.keysight.keysight33510B()
    if reset:
        fgen.utility.reset()
        fgen._identity_description
        fgen._output_name
        fgen.outputs[0].standard_waveform.waveform = 'sine'
        fgen.outputs[1].standard_waveform.waveform = 'sine'
        fgen.outputs[0].impedance = 'INF'
        fgen.outputs[1].impedance = 'INF'
        fgen.outputs.phase_sync = True
        fgen.outputs[0].phase_sync = True
        fgen.outputs[1].phase_sync = True
        fgen.outputs[0].frequency_coupling = True
        fgen.outputs[1].frequency_coupling = True
        fgen._write("OUTPut:SYNC:SOURce CH2")
        fgen._write("TRIGger1:SOURce EXTernal")
        fgen._write("TRIGger2:SOURce EXTernal")
        fgen._write("SOURce1:PHASe:SYNChronize")
        fgen.outputs[0].standard_waveform.start_phase = 0
        fgen.outputs[1].standard_waveform.start_phase = 180
        fgen.outputs[0].standard_waveform.dc_offset = 0
        fgen.outputs[1].standard_waveform.dc_offset = 0
    print('function generator ready')
    return fgen

def init_hameg(mode):
    # initialize power supply
    # mode 1...5v
    # mode 2...12V
    powersupply = ivi.hameg.hamegHMP2030()
    if mode ==1:
        powersupply.outputs[0].current_limit = 20E-3
        powersupply.outputs[1].current_limit = 20E-3
        powersupply.outputs[2].current_limit = 800E-3
        powersupply.outputs[0].voltage_level = 0
        powersupply.outputs[1].voltage_level = 0
        powersupply.outputs[2].voltage_level = 5
        powersupply.outputs[0].enabled=False
        powersupply.outputs[1].enabled=False
        powersupply.outputs[2].enabled=True
        print('power supply ready')
    elif mode ==2:
        powersupply.outputs[0].current_limit = 20E-3
        powersupply.outputs[1].current_limit = 200E-3
        powersupply.outputs[2].current_limit = 200E-3
        powersupply.outputs[0].voltage_level = 10
        powersupply.outputs[1].voltage_level = 12
        powersupply.outputs[2].voltage_level = 12
        powersupply.outputs[0].enabled=False
        powersupply.outputs[1].enabled=True
        powersupply.outputs[2].enabled=True
        print('power supply ready')
    else:
        print('No mode selected. Pleas select mode 1 for 5V and mode 2 for 12V supply.')
        print('power supply not ready')
    
    return powersupply