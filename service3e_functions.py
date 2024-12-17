
        
def form_reqmsg4srv3E(sprmib_flag):   
    sid = int("3E", 16)
    subfunction = int("00", 16)
    if (sprmib_flag == True):
         subfunction = subfunction| 0x80   #MSB is set if SPRMIB is requested.  
    req_bytes = [sid, subfunction]
    print(f"{sid} {subfunction}")
    return(req_bytes)
    

if __name__ == "__main__":
     print(form_reqmsg4srv3E(False))

   
