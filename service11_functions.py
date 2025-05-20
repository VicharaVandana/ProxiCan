#import re
def getsubfunction(session_name):
    session_mapping = {
        "Hard reset": 0x01,
        "KeyOffOn reset": 0x02,
        "Soft reset": 0x03
    }
    return session_mapping.get(session_name, 0x00)

def form_reqmsg4srv11(session, sprmib_flag):    
    sid = int("11", 16)
    if (sprmib_flag == True):
         subfunction = int(session) | 0x80   #MSB is set if SPRMIB is requested.
    else:
         subfunction = int(session)   

    req_bytes = [sid, subfunction]
    print(f"{sid} {subfunction}")
    return(req_bytes)
    
def checkresetinitiation(response):
     if(response.type == "Positive Response"): 
          return("Yes")
     else:
          return("No")
     
if __name__ == "__main__":
     print(form_reqmsg4srv11("03", False))

   
