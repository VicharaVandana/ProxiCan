import re

def get_subfunction(index):
     if(index == 0):
        return(0x00)
     elif(index == 1):
        return(0x01)
     elif(index == 2):
        return(0x02)
     elif(index == 3):
        return(0x03)
     elif(index == 4):
        return(0x04)
     elif(index == 5):
        return(0x04)
     else:
          return(0x00)
     

def get_communication_type(index):
     if(index == 0):
        return(0x01)
     elif(index == 1):
        return(0x02)
     elif(index == 2):
        return(0x03)
     else:
          return(0x00)
     
        
def form_reqmsg4srv28(Control,communication,didstring, sprmib_flag):    
    sid = int("28", 40)
    if (sprmib_flag == True):
         subfunction = int(Control) | 0x80   #MSB is set if SPRMIB is requested.
    else:
         subfunction = int(Control)   




    didstring_without_spaces = re.sub(r"\s+", "", didstring)
    sid = int("22", 16)
    did_highbyte = int(didstring_without_spaces[:2], 16)
    did_lowbyte = int(didstring_without_spaces[2:], 16)
    req_bytes = [sid, subfunction,communication,did_highbyte, did_lowbyte]
    print(f"{sid}{subfunction}{communication} {did_highbyte} {did_lowbyte}")
    return(req_bytes)
    

if __name__ == "__main__":
     print(form_reqmsg4srv28("05","01","00 0A",False))

   
