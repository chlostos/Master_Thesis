import ivi
import time
import sys
from setup.initialize import logger
from setup.initialize import config

def init_sr830():
    # initialize lock-in amplifier
    logger.info('initializing lock-in...')

    sens = int(config.get("SR830", "sensitivity"))                  # 23...100mV, 22...50mV, 21...20mV, 20...10mV, 19...5mV
    input_config = int(config.get("SR830", "signal_input"))             # signal input: 0...A, 1...A-B
    time_const = int(config.get("SR830", "time_const"))           # 4...1ms, 5...3ms, 6...10ms, 7...30ms, 8...100ms, 9...300ms
    
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
    logger.info('lock-in ready')
    return SR830

def init_fgen():
    # initialize function generator
    logger.info('initializing function generator...')
    fgen = ivi.keysight.keysight33510B()
    reset = input('would you like to reset the function generator? press (y/n): ')
    if 'y' in reset.lower():
        fgen.utility.reset()
        fgen._identity_description
        fgen._output_name
        fgen.outputs[0].standard_waveform.waveform = 'sine'
        fgen.outputs[1].standard_waveform.waveform = 'sine'
        fgen.outputs[0].impedance = 'INF'
        fgen.outputs[1].impedance = 'INF'
        fgen.outputs[0].frequency_coupling = True
        fgen.outputs[1].frequency_coupling = True
        fgen.outputs[0].standard_waveform.start_phase = 0
        fgen.outputs[1].standard_waveform.start_phase = 180
        fgen.outputs[0].standard_waveform.dc_offset = 0
        fgen.outputs[1].standard_waveform.dc_offset = 0
        fgen.outputs[0].standard_waveform.frequency = float(config.get("fgen","frequency"))
        fgen.outputs[0].standard_waveform.amplitude = float(config.get("fgen","u1"))
        fgen.outputs[1].standard_waveform.amplitude = float(config.get("fgen","u2"))
        fgen.outputs.phase_sync = True
        fgen.outputs[0].phase_sync = True
        fgen.outputs[1].phase_sync = True
        fgen.outputs[0].enabled = True
        fgen.outputs[1].enabled = True
    logger.info('function generator ready')
    return fgen

def init_hameg():
    # initialize power supply
    # mode 1...5v
    # mode 2...12V
    logger.info('initializing power supply...')
    powersupply = ivi.hameg.hamegHMP2030()
    mode = int(config.get("hameg","supply"))
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
        logger.info('power supply ready')
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
        logger.info('power supply ready')
    else:
        logger.info('No supply selected. Pleas select mode 1 for 5V and mode 2 for 12V supply.')
        logger.info('power supply not ready')
    
    return powersupply