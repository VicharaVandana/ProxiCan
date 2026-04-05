from ctypes import *
import time
import configure as conf


VCI_USBCAN2 = 41
TYPE_CANFD = 1

# --- C-Structures ---
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

# --- Dummy Message Class to mimic python-can ---
class Message:
    def __init__(self, arbitration_id, data, is_extended_id=False, is_fd=True, timestamp=0.0):
        self.arbitration_id = arbitration_id
        self.data = bytearray(data)  # allows .hex() and list() casting
        self.is_extended_id = is_extended_id
        self.is_fd = is_fd
        self.timestamp = timestamp

    def __str__(self):
        return f"ID: {hex(self.arbitration_id)} Data: {self.data.hex()}"

class WaveshareManager:
    """Manages the Master USB-CAN-FD Device Base"""
    def __init__(self):
        try:
            self.dll = windll.LoadLibrary('./ControlCANFD.dll')
        except Exception as e:
            raise RuntimeError(f"Could not load DLL: {e}")

        # Setup API Signatures
        self.dll.ZCAN_OpenDevice.restype = c_void_p
        self.dll.ZCAN_SetAbitBaud.argtypes = (c_void_p, c_ulong, c_ulong)
        self.dll.ZCAN_SetDbitBaud.argtypes = (c_void_p, c_ulong, c_ulong)
        self.dll.ZCAN_SetCANFDStandard.argtypes = (c_void_p, c_ulong, c_ulong)
        self.dll.ZCAN_InitCAN.argtypes = (c_void_p, c_ulong, c_void_p)
        self.dll.ZCAN_InitCAN.restype = c_void_p
        self.dll.ZCAN_StartCAN.argtypes = (c_void_p,)
        self.dll.ZCAN_TransmitFD.argtypes = (c_void_p, POINTER(ZCAN_TransmitFD_Data), c_ulong)
        self.dll.ZCAN_GetReceiveNum.argtypes = (c_void_p, c_ulong)
        self.dll.ZCAN_ReceiveFD.argtypes = (c_void_p, POINTER(ZCAN_ReceiveFD_Data), c_ulong, c_long)
        self.dll.ZCAN_CloseDevice.argtypes = (c_void_p,)

        # Initialize Hardware
        self.m_dev = self.dll.ZCAN_OpenDevice(VCI_USBCAN2, 0, 0)
        if self.m_dev == 0:
            raise RuntimeError("Failed to open device. Close the GUI!")

    def shutdown(self):
        """Closes the entire underlying USB-CAN-FD device."""
        if self.m_dev != 0:
            self.dll.ZCAN_CloseDevice(self.m_dev)
            self.m_dev = 0


class WaveshareChannel:
    """Represents a Single Channel (e.g., CAN1 or CAN2) mapping to the manager"""
    def __init__(self, manager: WaveshareManager, channel=0, abit=500000, dbit=1000000):
        self.manager = manager
        self.channel = channel
        
        # Setup Baud Rates
        self.manager.dll.ZCAN_SetAbitBaud(self.manager.m_dev, channel, abit)
        self.manager.dll.ZCAN_SetDbitBaud(self.manager.m_dev, channel, dbit)
        self.manager.dll.ZCAN_SetCANFDStandard(self.manager.m_dev, channel, 0) # ISO Standard

        # Start Channel
        init_config = ZCAN_CHANNEL_INIT_CONFIG()
        init_config.can_type = TYPE_CANFD
        init_config.config.canfd.mode = 0  
        self.dev_ch = self.manager.dll.ZCAN_InitCAN(self.manager.m_dev, channel, byref(init_config))
        self.manager.dll.ZCAN_StartCAN(self.dev_ch)

    def send(self, msg: Message):
        """Translates the python-can Message to the C-Structure and sends it."""
        tx_data = (ZCAN_TransmitFD_Data * 1)()
        tx_data[0].transmit_type = 0
        tx_data[0].frame.eff     = 1 if msg.is_extended_id else 0
        tx_data[0].frame.rtr     = 0
        tx_data[0].frame.brs     = 1 if msg.is_fd else 0
        tx_data[0].frame.can_id  = msg.arbitration_id
        tx_data[0].frame.len     = len(msg.data)
        
        for i in range(len(msg.data)):
            tx_data[0].frame.data[i] = msg.data[i]
            
        self.manager.dll.ZCAN_TransmitFD(self.dev_ch, tx_data, 1)

    def recv(self, timeout=None):
        """Polls the hardware buffer until a message arrives or timeout occurs."""
        start_time = time.time()
        
        while True:
            rx_count = self.manager.dll.ZCAN_GetReceiveNum(self.dev_ch, TYPE_CANFD)
            if rx_count > 0:
                rx_msgs = (ZCAN_ReceiveFD_Data * 1)() # Read 1 frame at a time
                self.manager.dll.ZCAN_ReceiveFD(self.dev_ch, rx_msgs, 1, -1)
                
                f = rx_msgs[0].frame
                data_bytes = [f.data[j] for j in range(f.len)]
                print(f"Received: {data_bytes}")
                
                # Return the dummy Message object
                return Message(
                    arbitration_id=f.can_id,
                    data=data_bytes,
                    is_extended_id=(f.eff == 1),
                    is_fd=(conf.fdf_type == "CANFD"),
                    timestamp=time.time()
                )
            
            # Timeout Check
            if timeout is not None:
                if (time.time() - start_time) >= timeout:
                    return None
            
            time.sleep(0.001) # 1ms poll delay to save CPU