import copy

NRC_DATA = {
    0x00: ["PositiveResponse", "This response code indicates that the requested action has been fulfilled by the server. The response is positive as well."],
    0x10: ["generalReject", "This response code indicates that the requested action has been rejected by the server. The generalReject response code shall only be implemented in the server if none of the negative response codes defined in this document meet the needs of the implementation. At no means shall this response code be a general replacement for other response codes defined."],
    0x11: ["serviceNotSupported", "This response code indicates that the requested action will not be taken because the server does not support the requested service. The server shall send this response code in case the client has sent a request message with a service identifier, which is either unknown or not supported by the server. Therefore this negative response code is not shown in the list of negative response codes to be supported for a diagnostic service, because this negative response code is not applicable for supported services."],
    0x12: ["subFunctionNotSupported", "This response code indicates that the requested action will not be taken because the server does not support the service specific parameters of the request message. The server shall send this response code in case the client has sent a request message with a known and supported service identifier but with 'sub function' which is either unknown or not supported."],
    0x13: ["incorrectMessageLengthOrInvalidFormat", "This response code indicates that the requested action will not be taken because the length of the received request message does not match the prescribed length for the specified service or the format of the parameters do not match the prescribed format for the specified service."],
    0x14: ["responseTooLong", "This response code shall be reported by the server if the response to be generated exceeds the maximum number of bytes available by the underlying network layer."],
    0x21: ["busyRepeatRequest", "This response code indicates that the server is temporarily too busy to perform the requested operation. In this circumstance the client shall perform repetition of the 'identical request message' or 'another request message'. The repetition of the request shall be delayed by a time specified in the respective implementation documents. Example: In a multi-client environment the diagnostic request of one client might be blocked temporarily by a NRC 0x21 while a different client finishes a diagnostic task. NOTE If the server is able to perform the diagnostic task but needs additional time to finish the task and prepare the response, the NRC 0x78 shall be used instead of NRC 0x21. This response code is in general supported by each diagnostic service, as not otherwise stated in the data link specific implementation document, therefore it is not listed in the list of applicable response codes of the diagnostic services."],
    0x22: ["conditionsNotCorrect", "This response code indicates that the requested action will not be taken because the server prerequisite conditions are not met."],
    0x24: ["requestSequenceError", "This response code indicates that the requested action will not be taken because the server expects a different sequence of request messages or message as sent by the client. This may occur when sequence sensitive requests are issued in the wrong order. Example: A successful SecurityAccess service specifies a sequence of requestSeed and sendKey as sub-functions in the request messages. If the sequence is sent different by the client the server shall send a negative response message with the negative response code 0x24 (requestSequenceError)."],
    0x31: ["requestOutOfRange", "This response code indicates that the requested action will not be taken because the server has detected that the request message contains a parameter which attempts to substitute a value beyond its range of authority (e.g. attempting to substitute a data byte of 111 when the data is only defined to 100), or which attempts to access a dataIdentifier/routineIdentifer that is not supported or not supported in active session. This response code shall be implemented for all services, which allow the client to read data, write data or adjust functions by data in the server."],
    0x33: ["securityAccessDenied", "This response code indicates that the requested action will not be taken because the server's security strategy has not been satisfied by the client. The server shall send this response code if one of the following cases occur: the test conditions of the server are not met, the required message sequence e.g. DiagnosticSessionControl, securityAccess is not met, the client has sent a request message which requires an unlocked server. Beside the mandatory use of this negative response code as specified in the applicable services within this standard, this negative response code can also be used for any case where security is required and is not yet granted to perform the required service."],
    0x35: ["invalidKey", "This response code indicates that the server has not given security access because the key sent by the client did not match with the key in the server's memory. This counts as an attempt to gain security. The server shall remain locked and increment its internal securityAccessFailed counter."],
    0x36: ["exceedNumberOfAttempts", "This response code indicates that the requested action will not be taken because the client has unsuccessfully attempted to gain security access more times than the server's security strategy will allow."],
    0x37: ["requiredTimeDelayNotExpired", "This response code indicates that the requested action will not be taken because the client's latest attempt to gain security access was initiated before the server's required timeout period had elapsed."],
    0x70: ["uploadDownloadNotAccepted", "This response code indicates that an attempt to upload/download to a server's memory cannot be accomplished due to some fault conditions."],
    0x71: ["transferDataSuspended", "This response code indicates that a data transfer operation was halted due to some fault. The active transferData sequence shall be aborted."],
    0x72: ["generalProgrammingFailure", "This response code indicates that the server detected an error when erasing or programming a memory location in the permanent memory device (e.g. Flash Memory)."],
    0x73: ["wrongBlockSequenceCounter", "This response code indicates that the server detected an error in the sequence of blockSequenceCounter values. Note that the repetition of a TransferData request message with a blockSequenceCounter equal to the one included in the previous TransferData request message shall be accepted by the server."],
    0x78: ["requestCorrectlyReceived-ResponsePending", "This response code indicates that the request message was received correctly, and that all parameters in the request message were valid, but the action to be performed is not yet completed and the server is not yet ready to receive another request. As soon as the requested service has been completed, the server shall send a positive response message or negative response message with a response code different from this. The negative response message with this response code may be repeated by the server until the requested service is completed and the final response message is sent. This response code might impact the application layer timing parameter values. The detailed specification shall be included in the data link specific implementation document. This response code shall only be used in a negative response message if the server will not be able to receive further request messages from the client while completing the requested diagnostic service. When this response code is used, the server shall always send a final response (positive or negative) independent of the suppressPosRspMsgIndicationBit value. A typical example where this response code may be used is when the client has sent a request message, which includes data to be programmed or erased in flash memory of the server. If the programming/erasing routine (usually executed out of RAM) is not able to support serial communication while writing to the flash memory the server shall send a negative response message with this response code. This response code is in general supported by each diagnostic service, as not otherwise stated in the data link specific implementation document, therefore it is not listed in the list of applicable response codes of the diagnostic services."],
    0x7F: ["serviceNotSupportedInActiveSession", "This response code indicates that the requested action will not be taken because the server does not support the requested service in the session currently active. This response code shall only be used when the requested service is known to be supported in another session, otherwise response code 0x11 (serviceNotSupported) shall be used. This response code is in general supported by each diagnostic service, as not otherwise stated in the data link specific implementation document, therefore it is not listed in the list of applicable response codes of the diagnostic services."],
    0x81: ["rpmTooHigh", "This response code indicates that the requested action will not be taken because the server prerequisite condition for RPM is not met (current RPM is above a pre-programmed maximum threshold)."],
    0x82: ["rpmTooLow", "This response code indicates that the requested action will not be taken because the server prerequisite condition for RPM is not met (current RPM is below a pre-programmed minimum threshold)."],
    0x83: ["engineIsRunning", "This is required for those actuator tests which cannot be actuated while the Engine is running. This is different from RPM too high negative response and needs to be allowed."],
    0x84: ["engineIsNotRunning", "This is required for those actuator tests which cannot be actuated unless the Engine is running. This is different from RPM too low negative response, and needs to be allowed."],
    0x85: ["engineRunTimeTooLow", "This response code indicates that the requested action will not be taken because the server prerequisite condition for engine run time is not met (current engine run time is below a preprogrammed limit)."],
    0x86: ["temperatureTooHigh", "This response code indicates that the requested action will not be taken because the server prerequisite condition for temperature is not met (current temperature is above a pre-programmed maximum threshold)."],
    0x87: ["temperatureTooLow", "This response code indicates that the requested action will not be taken because the server prerequisite condition for temperature is not met (current temperature is below a pre-programmed minimum threshold)."],
    0x88: ["vehicleSpeedTooHigh", "This response code indicates that the requested action will not be taken because the server prerequisite condition for vehicle speed is not met (current vehicle speed is above a pre-programmed maximum threshold)."],
    0x89: ["vehicleSpeedTooLow", "This response code indicates that the requested action will not be taken because the server prerequisite condition for vehicle speed is not met (current vehicle speed is below a pre-programmed minimum threshold)."],
    0x8A: ["throttlePositionTooHigh", "This response code indicates that the requested action will not be taken because the server prerequisite condition for throttle position is not met (current throttle position is above a pre-programmed maximum threshold)."],
    0x8B: ["throttlePositionTooLow", "This response code indicates that the requested action will not be taken because the server prerequisite condition for throttle position is not met (current throttle position is below a pre-programmed minimum threshold)."],
    0x8C: ["transmissionRangeNotInNeutral", "This response code indicates that the requested action will not be taken because the server prerequisite condition for being in neutral is not met (current transmission range is not in neutral)."],
    0x8D: ["transmissionRangeNotInGear", "This response code indicates that the requested action will not be taken because the server prerequisite condition for being in gear is not met (current transmission range is not in gear)."],
    0x8F: ["brakeSwitchesNotClosed", "For safety reasons, this is required for certain tests before it begins, and must be maintained for the entire duration of the test."],
    0x90: ["shifterLeverNotInPark", "For safety reasons, this is required for certain tests before it begins, and must be maintained for the entire duration of the test."],
    0x91: ["torqueConverterClutchLocked", "This response code indicates that the requested action will not be taken because the server prerequisite condition for torque converter clutch is not met (current TCC status above a preprogrammed limit or locked)."],
    0x92: ["voltageTooHigh", "This response code indicates that the requested action will not be taken because the server prerequisite condition for voltage at the primary pin of the server (ECU) is not met (current voltage is above a pre-programmed maximum threshold)."],
    0x93: ["voltageTooLow", "This response code indicates that the requested action will not be taken because the server prerequisite condition for voltage at the primary pin of the server (ECU) is not met (current voltage is below a pre-programmed minimum threshold)."]
}


class cls_response:
    def __init__(self):
        self.type = "No Response"   #Types can be "No Response", "Positive Response" or "Negative Response"
        self.nrc = 0x00
        self.nrcname = "No NRC"
        self.nrcdesc = "There is no Negative Response Code"
        self.resp = []
        self.positiveResponsePending_count = 0

response = cls_response()

def get_response():
    global response
    return(response)

def sendRequest(request, IsPosResExpected = True):
    global response
    response.req = request.copy()
    if(request[0] == 0x22): #dummy implementation for service 22
        if(request[1:] == [0xF1, 0x28]):
            res = [0x7F, 0x22, 0x10]
            response.resp = res.copy()
            response.type = "Negative Response"
            response.nrc = 0x10
            response.nrcname = NRC_DATA.get(response.nrc, "Unknown NRC")[0]
            response.nrcdesc = NRC_DATA.get(response.nrc, "Unknown NRC Recieved. There is no record of this NRC in UDS ISO 14229 Document")[1]
        
        elif(request[1:] == [0xF1, 0x22]):
            res = [0x62, 0xF1, 0x22, 0x88, 0x6C, 0x5E, 0x3B]
            response.resp = res.copy()
            response.type = "Positive Response"
            response.nrc = 0x00
            response.nrcname = NRC_DATA.get(response.nrc, "Unknown NRC")[0]
            response.nrcdesc = NRC_DATA.get(response.nrc, "Unknown NRC Recieved. There is no record of this NRC in UDS ISO 14229 Document")[1]

        else:
            res = [0x7F, 0x22, 0x31]
            response.resp = res.copy()
            response.type = "Negative Response"
            response.nrc = 0x31
            response.nrcname = NRC_DATA.get(response.nrc, "Unknown NRC")[0]
            response.nrcdesc = NRC_DATA.get(response.nrc, "Unknown NRC Recieved. There is no record of this NRC in UDS ISO 14229 Document")[1]

    elif(request[0] == 0x10): #dummy implementation for service 10
        if(request[1] == 0x03):
            res = [0x50, 0x03, 0x50, 0x00, 0x13, 0x32]
            response.resp = res.copy()
            response.type = "Positive Response"
            response.nrc = 0x00
            response.nrcname = NRC_DATA.get(response.nrc, "Unknown NRC")[0]
            response.nrcdesc = NRC_DATA.get(response.nrc, "Unknown NRC Recieved. There is no record of this NRC in UDS ISO 14229 Document")[1]
        elif(request[1] == 0x02):
            res = [0x7F, 0x10, 0x7F]
            response.resp = res.copy()
            response.type = "Negative Response"
            response.nrc = 0x7F
            response.nrcname = NRC_DATA.get(response.nrc, "Unknown NRC")[0]
            response.nrcdesc = NRC_DATA.get(response.nrc, "Unknown NRC Recieved. There is no record of this NRC in UDS ISO 14229 Document")[1]
        else:
            res = [0x7F, 0x10, 0x10]
            response.resp = res.copy()
            response.type = "Negative Response"
            response.nrc = 0x10
            response.nrcname = NRC_DATA.get(response.nrc, "Unknown NRC")[0]
            response.nrcdesc = NRC_DATA.get(response.nrc, "Unknown NRC Recieved. There is no record of this NRC in UDS ISO 14229 Document")[1]

    elif(request[0] == 0x14): #dummy implementation for service 14
        if(request[1] == 0xFF and request[2] == 0xFF and request[3] == 0x33):
            res = [0x54]
            response.resp = res.copy()
            response.type = "Positive Response"
            response.nrc = 0x00
            response.nrcname = NRC_DATA.get(response.nrc, "Unknown NRC")[0]
            response.nrcdesc = NRC_DATA.get(response.nrc, "Unknown NRC Recieved. There is no record of this NRC in UDS ISO 14229 Document")[1]

        else:
            res = [0x7F, 0x14, 0x31]
            response.resp = res.copy()
            response.type = "Negative Response"
            response.nrc = 0x31
            response.nrcname = NRC_DATA.get(response.nrc, "Unknown NRC")[0]
            response.nrcdesc = NRC_DATA.get(response.nrc, "Unknown NRC Recieved. There is no record of this NRC in UDS ISO 14229 Document")[1]


    elif(request[0] == 0x2E): #dummy implementation for service 2E
        if(request[1:3] == [0xF1, 0x28]):
            res = [0x7F, 0x2E, 0x10]
            response.resp = res.copy()
            response.type = "Negative Response"
            response.nrc = 0x10
            response.nrcname = NRC_DATA.get(response.nrc, "Unknown NRC")[0]
            response.nrcdesc = NRC_DATA.get(response.nrc, "Unknown NRC Recieved. There is no record of this NRC in UDS ISO 14229 Document")[1]
        
        elif(request[1:3] == [0xF1, 0x22]):
            res = [0x6E, 0xF1, 0x22]
            response.resp = res.copy()
            response.type = "Positive Response"
            response.nrc = 0x00
            response.nrcname = NRC_DATA.get(response.nrc, "Unknown NRC")[0]
            response.nrcdesc = NRC_DATA.get(response.nrc, "Unknown NRC Recieved. There is no record of this NRC in UDS ISO 14229 Document")[1]

        else:
            res = [0x7F, 0x2E, 0x31]
            response.resp = res.copy()
            response.type = "Negative Response"
            response.nrc = 0x31
            response.nrcname = NRC_DATA.get(response.nrc, "Unknown NRC")[0]
            response.nrcdesc = NRC_DATA.get(response.nrc, "Unknown NRC Recieved. There is no record of this NRC in UDS ISO 14229 Document")[1]

    elif(request[0] == 0x27): #dummy implementation for service 27
        if(request[1] == 0x01): #Get seed for security level 01
            res = [0x67, 0x01, 0x19, 0x47]
            response.resp = res.copy()
            response.type = "Positive Response"
            response.nrc = 0x00
            response.nrcname = NRC_DATA.get(response.nrc, "Unknown NRC")[0]
            response.nrcdesc = NRC_DATA.get(response.nrc, "Unknown NRC Recieved. There is no record of this NRC in UDS ISO 14229 Document")[1]
        elif(request[1] == 0x02):   #Validate Key for security level 01
            if((request[2] == 0xE6) and (request[3] == 0xB9)):
                res = [0x67, 0x02]
                response.resp = res.copy()
                response.type = "Positive Response"
                response.nrc = 0x00
                response.nrcname = NRC_DATA.get(response.nrc, "Unknown NRC")[0]
                response.nrcdesc = NRC_DATA.get(response.nrc, "Unknown NRC Recieved. There is no record of this NRC in UDS ISO 14229 Document")[1]
            else:
                res = [0x7F, 0x27, 0x35]
                response.resp = res.copy()
                response.type = "Negative Response"
                response.nrc = 0x35
                response.nrcname = NRC_DATA.get(response.nrc, "Unknown NRC")[0]
                response.nrcdesc = NRC_DATA.get(response.nrc, "Unknown NRC Recieved. There is no record of this NRC in UDS ISO 14229 Document")[1]
        else:
            res = [0x7F, 0x27, 0x33]
            response.resp = res.copy()
            response.type = "Negative Response"
            response.nrc = 0x33
            response.nrcname = NRC_DATA.get(response.nrc, "Unknown NRC")[0]
            response.nrcdesc = NRC_DATA.get(response.nrc, "Unknown NRC Recieved. There is no record of this NRC in UDS ISO 14229 Document")[1]

    elif(request[0] == 0x85): #dummy implementation for service 85
        if(request[1] == 0x02):
            res = [0xC5, 0x02]
            response.resp = res.copy()
            response.type = "Positive Response"
            response.nrc = 0x00
            response.nrcname = NRC_DATA.get(response.nrc, "Unknown NRC")[0]
            response.nrcdesc = NRC_DATA.get(response.nrc, "Unknown NRC Recieved. There is no record of this NRC in UDS ISO 14229 Document")[1]
        elif(request[1] == 0x01):
            res = [0xC5, 0x01]
            response.resp = res.copy()
            response.type = "Positive Response"
            response.nrc = 0x00
            response.nrcname = NRC_DATA.get(response.nrc, "Unknown NRC")[0]
            response.nrcdesc = NRC_DATA.get(response.nrc, "Unknown NRC Recieved. There is no record of this NRC in UDS ISO 14229 Document")[1]
        else:
            res = [0x7F, 0x85, 0x31]
            response.resp = res.copy()
            response.type = "Negative Response"
            response.nrc = 0x31
            response.nrcname = NRC_DATA.get(response.nrc, "Unknown NRC")[0]
            response.nrcdesc = NRC_DATA.get(response.nrc, "Unknown NRC Recieved. There is no record of this NRC in UDS ISO 14229 Document")[1]


    elif(request[0] == 0x28): #dummy implementation for service 28
        if(request[1] == [0x02]):
                res = [0x7F, 0x28]
                response.resp = res.copy()
                response.type = "Negative Response"
                response.nrc = 0x10
                response.nrcname = NRC_DATA.get(response.nrc, "Unknown NRC")[0]
                response.nrcdesc = NRC_DATA.get(response.nrc, "Unknown NRC Recieved. There is no record of this NRC in UDS ISO 14229 Document")[1]
            
        elif(request[1:3] == [0x01, 0x02]):
                res = [0x68, 0x01, 0x02]
                response.resp = res.copy()
                response.type = "Positive Response"
                response.nrc = 0x00
                response.nrcname = NRC_DATA.get(response.nrc, "Unknown NRC")[0]
                response.nrcdesc = NRC_DATA.get(response.nrc, "Unknown NRC Recieved. There is no record of this NRC in UDS ISO 14229 Document")[1]

        else:
                res = [0x7F, 0x28, 0x12]
                response.resp = res.copy()
                response.type = "Negative Response"
                response.nrc = 0x12
                response.nrcname = NRC_DATA.get(response.nrc, "Unknown NRC")[0]
                response.nrcdesc = NRC_DATA.get(response.nrc, "Unknown NRC Recieved. There is no record of this NRC in UDS ISO 14229 Document")[1]

    elif(request[0] == 0x23): #dummy implementation for service 28
        if(request[1] == 0x23):
            res = [0x7F, 0x28]
            response.resp = res.copy()
            response.type = "Negative Response"
            response.nrc = 0x10
            response.nrcname = NRC_DATA.get(response.nrc, "Unknown NRC")[0]
            response.nrcdesc = NRC_DATA.get(response.nrc, "Unknown NRC Recieved. There is no record of this NRC in UDS ISO 14229 Document")[1]
        
        elif(request[1] == 0X24):
            if(request[2:6]==[0x20,0x48,0x13,0x92]):
                if(request[6:]==[0x01,0x03]):
                    res = [0x63,0x00,0x00]
                    response.resp = res.copy()
                    response.type = "Positive Response"
                    response.nrc = 0x00
                    response.nrcname = NRC_DATA.get(response.nrc, "Unknown NRC")[0]
                    response.nrcdesc = NRC_DATA.get(response.nrc, "Unknown NRC Recieved. There is no record of this NRC in UDS ISO 14229 Document")[1]

        else:
            res = [0x7F, 0x28, 0x31]
            response.resp = res.copy()
            response.type = "Negative Response"
            response.nrc = 0x31
            response.nrcname = NRC_DATA.get(response.nrc, "Unknown NRC")[0]
            response.nrcdesc = NRC_DATA.get(response.nrc, "Unknown NRC Recieved. There is no record of this NRC in UDS ISO 14229 Document")[1]

    elif(request[0] == 0x31): #dummy implementation for service 2E
        if(request[1] == 0x02):
            res = [0x7F, 0x31, 0x10]
            response.resp = res.copy()
            response.type = "Negative Response"
            response.nrc = 0x10
            response.nrcname = NRC_DATA.get(response.nrc, "Unknown NRC")[0]
            response.nrcdesc = NRC_DATA.get(response.nrc, "Unknown NRC Recieved. There is no record of this NRC in UDS ISO 14229 Document")[1]
        
        elif(request[2:4] == [0x02, 0x01]):
            res = [0x71, 0x02, 0x01]
            response.resp = res.copy()
            response.type = "Positive Response"
            response.nrc = 0x00
            response.nrcname = NRC_DATA.get(response.nrc, "Unknown NRC")[0]
            response.nrcdesc = NRC_DATA.get(response.nrc, "Unknown NRC Recieved. There is no record of this NRC in UDS ISO 14229 Document")[1]

        else:
            res = [0x7F, 0x2E, 0x31]
            response.resp = res.copy()
            response.type = "Negative Response"
            response.nrc = 0x31
            response.nrcname = NRC_DATA.get(response.nrc, "Unknown NRC")[0]
            response.nrcdesc = NRC_DATA.get(response.nrc, "Unknown NRC Recieved. There is no record of this NRC in UDS ISO 14229 Document")[1]
    
    elif(request[0] == 0x19): #dummy implementation for service 19
        if(request[1] == 0x01 and request[2]==0x08):
            res = [0x59, 0x01, 0x2F, 0x01, 0x00, 0x01]
            response.resp = res.copy()
            response.type = "Positive Response"
            response.nrc = 0x00
            response.nrcname = NRC_DATA.get(response.nrc, "Unknown NRC")[0]
            response.nrcdesc = NRC_DATA.get(response.nrc, "Unknown NRC Recieved. There is no record of this NRC in UDS ISO 14229 Document")[1]
        elif(request[1] == 0x02 and request[2]==0x84):
            res = [0x59, 0x02, 0x7F, 0x0A, 0x9B, 0x17, 0x24, 0x08, 0x05, 0x11, 0x2F]
            response.resp = res.copy()
            response.type = "Positive Response"
            response.nrc = 0x00
            response.nrcname = NRC_DATA.get(response.nrc, "Unknown NRC")[0]
            response.nrcdesc = NRC_DATA.get(response.nrc, "Unknown NRC Recieved. There is no record of this NRC in UDS ISO 14229 Document")[1]
        elif(request[1] == 0x04):
            res = [0x59, 0x04, 0x7F, 0x0A, 0x9B, 0x17, 0x24, 0x08, 0x05, 0x11, 0x2F]
            response.resp = res.copy()
            response.type = "Positive Response"
            response.nrc = 0x00
            response.nrcname = NRC_DATA.get(response.nrc, "Unknown NRC")[0]
            response.nrcdesc = NRC_DATA.get(response.nrc, "Unknown NRC Recieved. There is no record of this NRC in UDS ISO 14229 Document")[1]
        elif(request[1] == 0x0A):
            res = [0x59, 0x0A, 0x7F, 0x12, 0x34, 0x56, 0x24, 0x23, 0x45, 0x05, 0x00, 0xAB, 0xCD, 0x01, 0x2F]
            response.resp = res.copy()
            response.type = "Positive Response"
            response.nrc = 0x00
            response.nrcname = NRC_DATA.get(response.nrc, "Unknown NRC")[0]
            response.nrcdesc = NRC_DATA.get(response.nrc, "Unknown NRC Recieved. There is no record of this NRC in UDS ISO 14229 Document")[1]  
        elif(request[1] == 0x02 and request[2]==0x01):
            res = [0x59, 0x02, 0x7F]
            response.resp = res.copy()
            response.type = "Positive Response"
            response.nrc = 0x00
            response.nrcname = NRC_DATA.get(response.nrc, "Unknown NRC")[0]
            response.nrcdesc = NRC_DATA.get(response.nrc, "Unknown NRC Recieved. There is no record of this NRC in UDS ISO 14229 Document")[1]      
        else:
            res = [0x7F, 0x19, 0x10]
            response.resp = res.copy()
            response.type = "Negative Response"
            response.nrc = 0x10
            response.nrcname = NRC_DATA.get(response.nrc, "Unknown NRC")[0]
            response.nrcdesc = NRC_DATA.get(response.nrc, "Unknown NRC Recieved. There is no record of this NRC in UDS ISO 14229 Document")[1]

    elif(request[0] == 0x3d): #dummy implementation for service 3d
        if(request[1] == 0x22):
            res = [0x7F, 0x28]
            response.resp = res.copy()
            response.type = "Negative Response"
            response.nrc = 0x10
            response.nrcname = NRC_DATA.get(response.nrc, "Unknown NRC")[0]
            response.nrcdesc = NRC_DATA.get(response.nrc, "Unknown NRC Recieved. There is no record of this NRC in UDS ISO 14229 Document")[1]
        
        elif(request[1] == 0X12):
            if(request[2:4]==[0x20,0x48]):
                if(request[4]==0x02):
                    if(request[5:]==[0x00,0x8c]):
                        res = [0x7D,0x12,0x20,0x48,0x02]
                        response.resp = res.copy()
                        response.type = "Positive Response"
                        response.nrc = 0x00
                        response.nrcname = NRC_DATA.get(response.nrc, "Unknown NRC")[0]
                        response.nrcdesc = NRC_DATA.get(response.nrc, "Unknown NRC Recieved. There is no record of this NRC in UDS ISO 14229 Document")[1]

        else:
            res = [0x7F, 0x28, 0x31]
            response.resp = res.copy()
            response.type = "Negative Response"
            response.nrc = 0x31
            response.nrcname = NRC_DATA.get(response.nrc, "Unknown NRC")[0]
            response.nrcdesc = NRC_DATA.get(response.nrc, "Unknown NRC Recieved. There is no record of this NRC in UDS ISO 14229 Document")[1]

    elif(request[0] == 0x34): #dummy implementation for service 34
        if(request[1] == 0x00):
            res = [0x7F, 0x28]
            response.resp = res.copy()
            response.type = "Negative Response"
            response.nrc = 0x10
            response.nrcname = NRC_DATA.get(response.nrc, "Unknown NRC")[0]
            response.nrcdesc = NRC_DATA.get(response.nrc, "Unknown NRC Recieved. There is no record of this NRC in UDS ISO 14229 Document")[1]
        
        elif(request[1] == 0X10):
            if(request[2]==0x12):
                if(request[3:5]==[0x20,0x48]):
                    if(request[5]==0x8c):
                        res = [0x74,0xff,0xff,0xff,0xff]
                        response.resp = res.copy()
                        response.type = "Positive Response"
                        response.nrc = 0x00
                        response.nrcname = NRC_DATA.get(response.nrc, "Unknown NRC")[0]
                        response.nrcdesc = NRC_DATA.get(response.nrc, "Unknown NRC Recieved. There is no record of this NRC in UDS ISO 14229 Document")[1]

        else:
            res = [0x7F, 0x34, 0x12]
            response.resp = res.copy()
            response.type = "Negative Response"
            response.nrc = 0x12
            response.nrcname = NRC_DATA.get(response.nrc, "Unknown NRC")[0]
            response.nrcdesc = NRC_DATA.get(response.nrc, "Unknown NRC Recieved. There is no record of this NRC in UDS ISO 14229 Document")[1]

    else:
        res = [0x7F, request[0], 0x11]
        response.resp = res.copy()
        response.type = "Negative Response"
        response.nrc = 0x11
        response.nrcname = NRC_DATA.get(response.nrc, "Unknown NRC")[0]
        response.nrcdesc = NRC_DATA.get(response.nrc, "Unknown NRC Recieved. There is no record of this NRC in UDS ISO 14229 Document")[1]

    

    response_copy = copy.deepcopy(response)
    return(response_copy)    
