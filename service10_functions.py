
def getsubfunction(index):
     if(index == 0):
          return(0x01)
     elif(index == 1):
          return(0x02)
     elif(index == 2):
          return(0x03)
     elif(index == 3):
          return(0x04)
     else:
          return(0x00)
     
     
        
def form_reqmsg4srv10(session, sprmib_flag):    
    sid = int("10", 16)
    if (sprmib_flag == True):
         subfunction = int(session) | 0x80   #MSB is set if SPRMIB is requested.
    else:
         subfunction = int(session)   

    req_bytes = [sid, subfunction]
    print(f"{sid} {subfunction}")
    return(req_bytes)
    

if __name__ == "__main__":
     print(form_reqmsg4srv10("03", False))

   
