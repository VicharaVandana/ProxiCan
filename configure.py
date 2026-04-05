from environment import *
import os

if RUNNING_ON_RASPBERRYPI == True:
    import can
elif RUNNING_ON_WINDOWS_WAVESHARE == True:
    from waveshare_wrapper import Message as can_Message
    # NEW: Import our wrapper
    from waveshare_wrapper import WaveshareManager, WaveshareChannel
else:
    pass



diag_req_msgid = 0x18DA6CF2  
diag_resp_msgid = 0x18DAF26C  
can_channel = 0 # CHANGED: Waveshare uses integer 0 for CAN1, 1 for CAN2
id_type = "EXTENDED"    
fdf_type = "CANFD"      
baudrate = 500000
datarate = 2000000
sample_point = 0.8
flowcontrolframe_maxwaittime = 2 

tx = None
rx = None
manager = None
ecu_ch = None

def connectCAN(canconfig):
    global diag_req_msgid, diag_resp_msgid, can_channel, id_type, fdf_type, baudrate, datarate, sample_point, rx, tx, manager, ecu_ch

    diag_req_msgid = canconfig.ReqCanId  
    diag_resp_msgid = canconfig.RespCanId 
    # can_channel = 0 # Hardcoded to integer 0 for Waveshare CAN 1
    # NEW: Determine channel index from string: "CAN 1" -> 0, "CAN 2" -> 1
    if "CAN 1" in canconfig.channel:
        can_channel = 0
    elif "CAN 2" in canconfig.channel:
        can_channel = 1
    else:
        can_channel = 0 # Default fallback
    
    id_type = canconfig.idtype
    baudrate = canconfig.bitrate
    fdf_type = canconfig.fdftype
    datarate = canconfig.brsrate
    sample_point = canconfig.samplepoint
    flowcontrolframe_maxwaittime = canconfig.FlowCtrlTimeout

    try:
        if RUNNING_ON_RASPBERRYPI == True:
            os.system(f'sudo ip link set {can_channel} up type can bitrate {baudrate} sample-point {sample_point} dbitrate {datarate} dsample-point {sample_point} restart-ms 1000 berr-reporting on fd on')
            tx = can.interface.Bus(channel=can_channel, bustype='socketcan', fd=True)
            rx = can.interface.Bus(channel=can_channel, bustype='socketcan', fd=True)
        elif RUNNING_ON_WINDOWS_WAVESHARE == True:
            # NEW: Initialize the Waveshare Windows Hardware
            manager = WaveshareManager()
            
            # Map both rx and tx to the SAME physical channel selected in GUI
            tx = WaveshareChannel(manager, channel=can_channel, abit=baudrate, dbit=datarate)
            rx = tx

            # ECU simulator channel - only if enabled and different from tester channel
            if ECU_SIMULATOR_ENABLE:
                ecu_ch = WaveshareChannel(manager, channel=ECU_SIMULATOR_CHANNEL, abit=baudrate, dbit=datarate)
        else:
            pass
            
        return True
    except Exception as e:
        return str(e)

def disconnectCAN():
    global rx, tx, manager, ecu_ch
    if RUNNING_ON_RASPBERRYPI == True:
        os.system(f'sudo ip link set {can_channel} down')
    elif RUNNING_ON_WINDOWS_WAVESHARE == True:
        # NEW: Gracefully close the DLL
        if manager is not None:
            manager.shutdown()
            manager = None
    else:        
        pass

            
    rx = None
    tx = None
    ecu_ch = None