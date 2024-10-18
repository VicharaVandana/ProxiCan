#import re
def getsubfunction(index):
     if(index == 0):
          return(0x01)
     elif(index == 1):
          return(0x02)
     elif(index == 2):
          return(0x03)
     else:
          return(0x00)


def getsubfunctionname(session):
     if(session == 0x01):
          return("Hard reset")
     elif(session == 0x02) :
          return("Key Off/On Reset")
     elif(session == 0x03):
          return("Soft Reset") 
     else:
          return("User defined reset (Unknown) ")


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

   
