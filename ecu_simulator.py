from PyQt5 import QtCore
import time
import configure as conf
from waveshare_wrapper import Message
import environment as env

class EcuSimulatorThread(QtCore.QThread):
    """
    Background thread to mimic an ECU behavior. 
    Listens on the specified ECU_CH and responds to UDS requests.
    Supports Single Frame and Multi-Frame (ISO-TP) responses.
    """
    def __init__(self, channel_instance):
        super().__init__()
        self._is_running = False
        self.ecu_ch = channel_instance

    def run(self):
        print(f"ECU Simulator active on {self.ecu_ch.channel if hasattr(self.ecu_ch, 'channel') else 'selected channel'}")
        self._is_running = True
        while self._is_running:
            if self.ecu_ch is not None:
                msg = self.ecu_ch.recv(timeout=0.1)
                if msg is not None:
                    self.process_request(msg)
            else:
                time.sleep(0.1)

    def process_request(self, msg):
        """Dispatches the received CAN message to specific UDS service handlers."""
        pci = msg.data[0]
        if (pci & 0xF0) == 0x00: # Single Frame
            dl = pci & 0x0F
            if dl == 0: # CAN FD escape
                dl = msg.data[1]
                sid = msg.data[2]
            else:
                sid = msg.data[1]
            
            if sid == 0x10: # Diagnostic Session Control
                self.handle_service_10(msg)
            elif sid == 0x22: # Read Data By Identifier
                self.handle_service_22(msg)
            else:
                # Handle unsupported services with NRC 0x11 (serviceNotSupported)
                self.send_negative_response(msg, sid, 0x11)
        
        elif (pci & 0xF0) == 0x10: # First Frame (of a multi-frame request, though rare for SIDs like 10/22)
            # Technically should handle multi-frame request too, but 10/22 are usually SF requests.
            pass

    def handle_service_10(self, msg):
        """Respond to Service 10 (DSC)"""
        sub_func = msg.data[2] if (msg.data[0] & 0x0F) != 0 else msg.data[3]
        
        # Positive Response Payload [SID=0x50, Sub, P2, P2*]
        payload = [0x50, sub_func, 0x00, 0x32, 0x01, 0xF4]
        self.send_uds_response(payload, msg.is_extended_id, msg.is_fd)
        print(f"ECU: Sent Response for Service 10 (Sub: {hex(sub_func)})")

    def handle_service_22(self, msg):
        """Respond to Service 22 (RDBI)"""
        # Parsing DID (Assuming it starts after SID)
        # For SF: PCI, SID, DID_H, DID_L
        # For FD SF with PCI 00: PCI, DL, SID, DID_H, DID_L
        pci = msg.data[0]
        if (pci & 0x0F) == 0:
            did = (msg.data[3] << 8) | msg.data[4]
        else:
            did = (msg.data[2] << 8) | msg.data[3]

        if did == 0xD105:
            # 200 bytes of dummy data
            data = [i % 256 for i in range(200)]
            payload = [0x62, 0xD1, 0x05] + data
            self.send_uds_response(payload, msg.is_extended_id, msg.is_fd)
            print(f"ECU: Sent Response for DID 0xD105 (200 bytes)")
        elif did == 0xF120:
            # 17 bytes VIN
            vin = "ABC1234567890VIN1"
            payload = [0x62, 0xF1, 0x20] + [ord(c) for c in vin]
            self.send_uds_response(payload, msg.is_extended_id, msg.is_fd)
            print(f"ECU: Sent Response for DID 0xF120 (VIN)")
        else:
            # Request Out Of Range
            self.send_negative_response(msg, 0x22, 0x31)

    def send_uds_response(self, payload, is_ext, is_fd):
        """Generic method to send UDS response using SF or FF/CF sequence."""
        length = len(payload)
        
        # Define limits for Single Frame
        if is_fd:
            max_sf = 62 
        else:
            max_sf = 7

        if length <= max_sf:
            # Send Single Frame
            if is_fd and length > 7:
                # FD Single Frame with length escape [0x00, length, ...]
                data = [0x00, length] + payload
            else:
                # Normal Single Frame [PCI_DL, ...]
                data = [length] + payload
            
            # Pad
            if is_fd: data += [0x00] * (64 - len(data))
            else: data += [0x00] * (8 - len(data))
            
            resp_msg = Message(conf.diag_resp_msgid, data, is_ext, is_fd)
            self.ecu_ch.send(resp_msg)
        else:
            # Send Multi-Frame Response
            self.send_multiframe(payload, is_ext, is_fd)

    def send_multiframe(self, payload, is_ext, is_fd):
        """Handles ISO-TP Transmit Sequence."""
        length = len(payload)
        
        # 1. Send First Frame
        if length > 4095:
            # FF_DL escape (not usually needed for 200 bytes but good for completeness)
            pci = [0x10, 0x00, (length >> 24) & 0xFF, (length >> 16) & 0xFF, (length >> 8) & 0xFF, length & 0xFF]
            data_bytes = pci + payload[:58 if is_fd else 2] # Simplified padding logic
            payload_pointer = 58 if is_fd else 2
        else:
            pci = [0x10 | ((length >> 8) & 0x0F), length & 0xFF]
            chunk_size = 62 if is_fd else 6
            data_bytes = pci + payload[:chunk_size]
            payload_pointer = chunk_size

        # Pad FF
        if is_fd: data_bytes += [0x00] * (64 - len(data_bytes))
        else: data_bytes += [0x00] * (8 - len(data_bytes))

        self.ecu_ch.send(Message(conf.diag_resp_msgid, data_bytes, is_ext, is_fd))
        
        # 2. Wait for Flow Control
        fc_msg = self.ecu_ch.recv(timeout=1.0)
        if not fc_msg or (fc_msg.data[0] & 0xF0 != 0x30):
            print("ECU: No Flow Control received, aborting transaction.")
            return
        
        # FS check
        fs = fc_msg.data[0] & 0x0F
        if fs != 0: # 0 is CTS
            print(f"ECU: Flow Control Status {fs} (Wait/Overflow), aborting.")
            return

        # 3. Send Consecutive Frames
        bs = fc_msg.data[1]
        st_min = fc_msg.data[2]
        
        seq_num = 1
        pending = length - payload_pointer
        while pending > 0:
            pci = 0x20 | (seq_num & 0x0F)
            chunk_size = 63 if is_fd else 7
            chunk = payload[payload_pointer : payload_pointer + chunk_size]
            data_bytes = [pci] + chunk
            
            # Pad CF
            if is_fd: data_bytes += [0x00] * (64 - len(data_bytes))
            else: data_bytes += [0x00] * (8 - len(data_bytes))
            
            self.ecu_ch.send(Message(conf.diag_resp_msgid, data_bytes, is_ext, is_fd))
            
            payload_pointer += len(chunk)
            pending -= len(chunk)
            seq_num += 1
            
            # ST_min delay (ms to s) - roughly
            if st_min > 0:
                time.sleep(st_min / 1000.0)

    def send_negative_response(self, original_msg, sid, nrc_code):
        """Helper to send a UDS Negative Response (0x7F)."""
        resp_data = [0x03, 0x7F, sid, nrc_code]
        if conf.fdf_type == "CANFD":
            resp_data += [0x00] * (64 - len(resp_data))
        else:
            resp_data += [0x00] * (8 - len(resp_data))

        self.ecu_ch.send(Message(conf.diag_resp_msgid, resp_data, original_msg.is_extended_id, original_msg.is_fd))
        print(f"ECU: Sent Negative Response for {hex(sid)} with NRC {hex(nrc_code)}")

    def stop(self):
        self._is_running = False
        self.wait()
