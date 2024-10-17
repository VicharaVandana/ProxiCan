#import re
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
    print(f"{sid} {subfunction}")
    return(req_bytes)
    

if __name__ == "__main__":
     print(form_reqmsg4srv85("03", False))

   
