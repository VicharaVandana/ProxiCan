from environment import *

if RUNNING_ON_RASPBERRYPI == True:
    import can
import os


diag_req_msgid = 0x18DA6CF2  # General broadcast address for diagnostic tools 18DA6CF2
diag_resp_msgid = 0x18DAF26C  # ECU response address (this may need to be adjusted based on your ECU) 18DAF26C
can_channel = 'can0'
id_type = "EXTENDED"    #CAN ID is extended or standard
fdf_type = "CANFD"      #CAN or CANFD
baudrate = 500000
datarate = 2000000
sample_point = 0.8
flowcontrolframe_maxwaittime = 5 #2seconds

tx = None
rx = None


#The function to initialise and configure the CAN channel
def connectCAN(canconfig):
    #Declare which all global variables will be  used and updated in the function
    global diag_req_msgid, diag_resp_msgid, can_channel, id_type, fdf_type, baudrate, datarate, sample_point, rx, tx

    #Update the Request and Response can ids and other configurations needed for diagnostic from the userform
    diag_req_msgid = canconfig.ReqCanId  
    diag_resp_msgid = canconfig.RespCanId 
    can_channel = canconfig.channel
    id_type = canconfig.idtype
    baudrate = canconfig.bitrate
    fdf_type = canconfig.fdftype
    datarate = canconfig.brsrate
    sample_point = canconfig.samplepoint
    flowcontrolframe_maxwaittime = canconfig.FlowCtrlTimeout

    try:
        #initialise the can
        # Set up the CAN interface
        if RUNNING_ON_RASPBERRYPI == True:
            #os.system(f'sudo ip link set {can_channel} up type can bitrate {baudrate} dbitrate {datarate} restart-ms 1000 berr-reporting on fd on')
            os.system(f'sudo ip link set {can_channel} up type can bitrate {baudrate} sample-point {sample_point} dbitrate {datarate} dsample-point {sample_point} fd on')
            tx = can.interface.Bus(channel=can_channel, bustype='socketcan', fd=True)
            rx = can.interface.Bus(channel=can_channel, bustype='socketcan', fd=True)
        return True
    except ValueError as e:
        return e

def disconnectCAN():
    global rx, tx
    if RUNNING_ON_RASPBERRYPI == True:
        os.system(f'sudo ip link set {can_channel} down')
        rx = None
        tx = None

        
    

