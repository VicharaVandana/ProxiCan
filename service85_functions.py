import re
def getsubfunction(session_name):
    # Mapping for the DTC Setting Type
    session_mapping = {
        "ON": 0x01,
        "OFF": 0x02
    }
    
    # Return the corresponding value, default to 0x00 if not found
    return session_mapping.get(session_name, 0x00)

     
def getsubfunctionname(session_name):
    # Mapping for the DTC Setting Type (using session_name as keys)
    session_mapping = {
        0x01: "ON - To enable setting of DTCs",
        0x02: "OFF - To disable setting of DTCs"
    }
    # Return the corresponding description, default to "User defined setting (Unknown)" if not found
    return session_mapping.get(session_name, "User defined setting (Unknown)")
     
def form_reqmsg4srv85_withdtc(session, sprmib_flag,dtc_string):    
    sid = int("85", 16)
    dtcstring_without_spaces = re.sub(r"\s+", "", dtc_string)
    if (sprmib_flag == True):
         subfunction = int(session) | 0x80   #MSB is set if SPRMIB is requested.
    else:
         subfunction = int(session)  

    dtc_highbyte = int(dtcstring_without_spaces[:2], 16)
    dtc_middlebyte = int(dtcstring_without_spaces[2:4], 16)
    dtc_lowbyte = int(dtcstring_without_spaces[4:], 16)
    #dtc_lowbyte=int(0xff)
    #dtc_middlebyte=int(0xff)
    #dtc_highbyte=int(0xff)
    print("dh",dtc_highbyte)
    print("dm",dtc_middlebyte)
    print("dl",dtc_lowbyte)
    req_bytes = [sid, subfunction, dtc_highbyte,dtc_middlebyte, dtc_lowbyte]
    print(f"{sid} {subfunction} {dtc_highbyte} {dtc_middlebyte} {dtc_lowbyte}" ) 
    return(req_bytes)
     
     
        
def form_reqmsg4srv85(session, sprmib_flag):    
    sid = int("85", 16)
    if (sprmib_flag == True):
         subfunction = int(session) | 0x80   #MSB is set if SPRMIB is requested.
    else:
         subfunction = int(session)   

    req_bytes = [sid, subfunction]
    print(f"{sid} {subfunction}")
    return(req_bytes)
    

if __name__ == "__main__":
     print(form_reqmsg4srv85("03", False))

   
