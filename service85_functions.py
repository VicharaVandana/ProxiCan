import re
def getsubfunction(index):
     if(index == 0):
          return(0x01)
     elif(index == 1):
          return(0x02)
     else:
          return(0x00)
     
def getsubfunctionname(session):
     if(session == 0x01):
          return("ON")
     elif(session == 0x02) :
          return("OFF")
     else:
          return("User defined setting (Unknown)")
     
def form_reqmsg4srv85(session, sprmib_flag):
     sid = int("85", 16)
     if (sprmib_flag == True):
         subfunction = int(session) | 0x80   #MSB is set if SPRMIB is requested.
     else:
         subfunction = int(session)  
     req_bytes = [sid, subfunction]
     print(f"{sid} {subfunction} " ) 
     return(req_bytes)

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
    

if __name__ == "__main__":
     print(form_reqmsg4srv85("03", False))

   
