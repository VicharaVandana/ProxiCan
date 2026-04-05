from ctypes import *
import time
import threading

# --- Constants & C-Structures ---
VCI_USBCAN2 = 41
INVALID_DEVICE_HANDLE  = 0
TYPE_CANFD = 1

class _ZCAN_CHANNEL_CAN_INIT_CONFIG(Structure):
    _fields_ = [("acc_code", c_uint), ("acc_mask", c_uint), ("reserved", c_uint),
                ("filter", c_ubyte), ("timing0", c_ubyte), ("timing1", c_ubyte), ("mode", c_ubyte)]

class _ZCAN_CHANNEL_CANFD_INIT_CONFIG(Structure):
    _fields_ = [("acc_code", c_uint), ("acc_mask", c_uint), ("abit_timing", c_uint),
                ("dbit_timing", c_uint), ("brp", c_uint), ("filter", c_ubyte),
                ("mode", c_ubyte), ("pad", c_ushort), ("reserved", c_uint)]

class _ZCAN_CHANNEL_INIT_CONFIG(Union):
    _fields_ = [("can", _ZCAN_CHANNEL_CAN_INIT_CONFIG), ("canfd", _ZCAN_CHANNEL_CANFD_INIT_CONFIG)]

class ZCAN_CHANNEL_INIT_CONFIG(Structure):
    _fields_ = [("can_type", c_uint), ("config", _ZCAN_CHANNEL_INIT_CONFIG)]

class ZCAN_CANFD_FRAME(Structure):
    _fields_ = [("can_id", c_uint, 29), ("err", c_uint, 1), ("rtr", c_uint, 1), ("eff", c_uint, 1), 
                ("len", c_ubyte), ("brs", c_ubyte, 1), ("esi", c_ubyte, 1), ("__res", c_ubyte, 6),
                ("__res0", c_ubyte), ("__res1", c_ubyte), ("data", c_ubyte * 64)]

class ZCAN_TransmitFD_Data(Structure):
    _fields_ = [("frame", ZCAN_CANFD_FRAME), ("transmit_type", c_uint)]

class ZCAN_ReceiveFD_Data(Structure):
    _fields_ = [("frame", ZCAN_CANFD_FRAME), ("timestamp", c_ulonglong)]

# --- Load DLL ---
try:
    canDLL = windll.LoadLibrary('./ControlCANFD.dll')
except Exception as e:
    print(f"Failed to load DLL: {e}")
    exit()

canDLL.ZCAN_OpenDevice.restype = c_void_p
canDLL.ZCAN_SetAbitBaud.argtypes = (c_void_p, c_ulong, c_ulong)
canDLL.ZCAN_SetDbitBaud.argtypes = (c_void_p, c_ulong, c_ulong)
canDLL.ZCAN_SetCANFDStandard.argtypes = (c_void_p, c_ulong, c_ulong)
canDLL.ZCAN_InitCAN.argtypes = (c_void_p, c_ulong, c_void_p)
canDLL.ZCAN_InitCAN.restype = c_void_p
canDLL.ZCAN_StartCAN.argtypes = (c_void_p,)
canDLL.ZCAN_TransmitFD.argtypes = (c_void_p, POINTER(ZCAN_TransmitFD_Data), c_ulong)
canDLL.ZCAN_GetReceiveNum.argtypes = (c_void_p, c_ulong)
canDLL.ZCAN_ReceiveFD.argtypes = (c_void_p, POINTER(ZCAN_ReceiveFD_Data), c_ulong, c_long)
canDLL.ZCAN_ResetCAN.argtypes = (c_void_p,)
canDLL.ZCAN_CloseDevice.argtypes = (c_void_p,)

# ==========================================
# 1. Hardware Initialization
# ==========================================
m_dev = canDLL.ZCAN_OpenDevice(VCI_USBCAN2, 0, 0)
if m_dev == INVALID_DEVICE_HANDLE:
    print("FATAL ERROR: Could not access the USB device. Ensure GUI is closed.")
    exit(0)

# Configure CH1 (0) and CH2 (1) - Abit: 500k, Dbit: 1M
for ch in [0, 1]:
    canDLL.ZCAN_SetAbitBaud(m_dev, ch, 500000)
    canDLL.ZCAN_SetDbitBaud(m_dev, ch, 1000000)
    canDLL.ZCAN_SetCANFDStandard(m_dev, ch, 0)

init_config = ZCAN_CHANNEL_INIT_CONFIG()
init_config.can_type = TYPE_CANFD
init_config.config.canfd.mode = 0  

dev_ch1 = canDLL.ZCAN_InitCAN(m_dev, 0, byref(init_config))
canDLL.ZCAN_StartCAN(dev_ch1)

dev_ch2 = canDLL.ZCAN_InitCAN(m_dev, 1, byref(init_config))
canDLL.ZCAN_StartCAN(dev_ch2)

# Global flag to control the background thread
is_running = True 

# ==========================================
# 2. The Background "Listener" Thread for CH2
# ==========================================
def ch2_monitor_thread():
    print("[CH2 Monitor] Started in background. Listening for traffic...\n")
    while is_running:
        rx_count = canDLL.ZCAN_GetReceiveNum(dev_ch2, TYPE_CANFD)
        if rx_count > 0:
            rx_msgs = (ZCAN_ReceiveFD_Data * rx_count)()
            actual_rx = canDLL.ZCAN_ReceiveFD(dev_ch2, rx_msgs, rx_count, -1)
            
            for i in range(actual_rx):
                f = rx_msgs[i].frame
                data_hex = " ".join([f"{f.data[j]:02X}" for j in range(f.len)])
                print(f"\n---> [CH2 Rx] ID: 0x{f.can_id:03X} | Len: {f.len:02d} | Data: {data_hex}")
        
        # Sleep for 1 millisecond so the thread doesn't max out your CPU
        time.sleep(0.001)

# Start the background thread
listener = threading.Thread(target=ch2_monitor_thread, daemon=True)
listener.start()

# ==========================================
# 3. Main Thread: Transmitter on CH1
# ==========================================
print("Bus Initialized. Channel 1 is ready to transmit.")
time.sleep(1) # Give the monitor thread a moment to print its start message

try:
    for i in range(1, 6):
        # Build a frame
        tx_data = (ZCAN_TransmitFD_Data * 1)()
        tx_data[0].transmit_type = 0
        tx_data[0].frame.eff     = 0
        tx_data[0].frame.rtr     = 0
        tx_data[0].frame.brs     = 1
        tx_data[0].frame.can_id  = 0x300 + i
        tx_data[0].frame.len     = 8
        
        for j in range(8):
            tx_data[0].frame.data[j] = j * i
            
        print(f"[CH1 Tx] Sending Message {i}/5...")
        canDLL.ZCAN_TransmitFD(dev_ch1, tx_data, 1)
        
        # Wait 2 seconds between sends
        time.sleep(2)

except KeyboardInterrupt:
    print("\nTransmission interrupted by user.")

# ==========================================
# 4. Clean Up
# ==========================================
print("\nShutting down...")
is_running = False # Tell the background thread to stop
listener.join(timeout=1.0) # Wait for the thread to safely close

canDLL.ZCAN_ResetCAN(dev_ch1)
canDLL.ZCAN_ResetCAN(dev_ch2)
canDLL.ZCAN_CloseDevice(m_dev) 
print("Hardware Released. Script Terminated.")