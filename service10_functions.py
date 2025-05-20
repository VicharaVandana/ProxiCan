
def getsubfunction(session_name):
    session_mapping = {
        "Default": 0x01,
        "Programming": 0x02,
        "Extended": 0x03,
        "Safety": 0x04
    }
    # Return the corresponding value or a default value if the session name is not found
    return session_mapping.get(session_name, 0x00)
     

        
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

   
