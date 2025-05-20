import general as gen
import json



class CanConfig:
    def __init__(self):
        self.ReqCanId = None
        self.RespCanId = None
        self.channel = None
        self.idtype = None
        self.bitrate = None
        self.fdftype = None
        self.brsrate = None
        self.samplepoint = None
        self.FlowCtrlTimeout = 2 #2 seconds

    # Convert the object to a dictionary
    def to_dict(self):
        return {
            'ReqCanId': self.ReqCanId,
            'RespCanId': self.RespCanId,
            'channel': self.channel,
            'idtype': self.idtype,
            'bitrate': self.bitrate,
            'fdftype': self.fdftype,
            'brsrate': self.brsrate,
            'samplepoint': self.samplepoint,
            'FlowCtrlTimeout': self.FlowCtrlTimeout
        }

    # Convert object to JSON string
    def to_json(self):
        return json.dumps(self.to_dict(), indent=4)
    
    # Optional: Add methods to set individual values (if you want setters)
    def set_req_can_id(self, req_can_id):
        self.ReqCanId = req_can_id
    
    def set_resp_can_id(self, resp_can_id):
        self.RespCanId = resp_can_id

    def set_channel(self, channel):
        self.channel = channel

    def set_id_type(self, id_type):
        self.idtype = id_type

    def set_bitrate(self, bitrate):
        self.bitrate = bitrate

    def set_fd_type(self, fd_type):
        self.fdftype = fd_type

    def set_brs_rate(self, brs_rate):
        self.brsrate = brs_rate

    def set_sample_point(self, sample_point):
        self.samplepoint = sample_point

    def set_flow_ctrl_timeout(self, timeout):
        self.FlowCtrlTimeout = timeout


def verifyandPopulateConfigFields(ui):
    canconfig = CanConfig()
    status = "Success"  #Initially assume it will be a success
    #Get Can channel is selected
    canchannel = ui.cmb_CanChannel.currentText()
    canconfig.set_channel(canchannel)     # Set the CAN channel

    #Check if proper Can Type is selected
    if ui.radiobtn_fdftype_can.isChecked():
        canconfig.set_fd_type('CAN')           # Set CAN type (CAN)
    elif ui.radiobtn_fdftype_canfd.isChecked():
        canconfig.set_fd_type('CANFD')           # Set CAN type (CANFD)
    else:
        status = f"No CAN Type selected. Select if CAN or CAN FD is used"

    #Check if proper Can ID Type is selected
    if ui.radiobtn_idtype_standard.isChecked():
        canconfig.set_id_type('STANDARD')        # Set CAN ID type
    elif ui.radiobtn_idtype_extended.isChecked():
        canconfig.set_id_type('EXTENDED')        # Set CAN ID type
    else:
        status = f"No CAN ID Type selected. Select if STANDARD or EXTENDED is used"
    
    #Check if Request and Response CAN ID is a proper Can ID
    reqidstr = ui.lineEdit_reqmsgid.text()
    residstr = ui.lineEdit_resmsgid.text()

    if(canconfig.idtype == 'STANDARD'): #standard 11 bits
        reqid = gen.is_valid_hex(reqidstr, 0b00, 0b11111111111)
        resid = gen.is_valid_hex(residstr, 0b00, 0b11111111111)
    else:   #Extended - 29 bits
        reqid = gen.is_valid_hex(reqidstr, 0b00, 0b11111111111111111111111111111)
        resid = gen.is_valid_hex(residstr, 0b00, 0b11111111111111111111111111111)


    if (reqid != False):
        canconfig.set_req_can_id(reqid)          # Set request CAN ID
    else:
        status = f"Invalid Request CAN ID {reqidstr}. It must be hexadecimal value of length corresponding to ID type"

    if (resid != False):
        canconfig.set_resp_can_id(resid)         # Set response CAN ID
    else:
        status = f"Invalid Response CAN ID {residstr}. It must be hexadecimal value of length corresponding to ID type"

    #Get Baudrate selected
    baudrate = ui.cmb_baudrate.currentText()
    if ("125" in baudrate):
        canconfig.set_bitrate(125000)            # Set CAN bitrate
    elif ("250" in baudrate):
        canconfig.set_bitrate(250000)            # Set CAN bitrate
    elif ("500" in baudrate):
        canconfig.set_bitrate(500000)            # Set CAN bitrate
    elif ("mbps" in baudrate):
        canconfig.set_bitrate(1000000)            # Set CAN bitrate
    else:
        status = f"Invalid Baudrate. Please select an option from dropdown"
    
    #Get DataRate selected
    datarate = ui.cmb_datarate.currentText()
    if ("125" in datarate):
        canconfig.set_brs_rate(125000)            # Set CAN datarate
    elif ("250" in datarate):
        canconfig.set_brs_rate(250000)            # Set CAN datarate
    elif ("500" in datarate):
        canconfig.set_brs_rate(500000)            # Set CAN datarate
    elif ("1mbps" in datarate):
        canconfig.set_brs_rate(1000000)            # Set CAN datarate
    elif ("2mbps" in datarate):
        canconfig.set_brs_rate(2000000)            # Set CAN datarate
    elif ("5mbps" in datarate):
        canconfig.set_brs_rate(5000000)            # Set CAN datarate
    else:
        status = f"Invalid FD Baudrate. Please select an option from dropdown"

    #Check if the sample point is valid
    samplepointstr = ui.lineEdit_samplepoint.text()
    samplepoint = gen.is_validfloat(samplepointstr, 0.0, 1.0)
    if (samplepoint != False):
        canconfig.set_sample_point(samplepoint)           # Set sample point
    else:
        status = f"Invalid Sample point {samplepointstr}. It must be floating point decimal value between 0.0 to 1.0"


    return (canconfig, status)

