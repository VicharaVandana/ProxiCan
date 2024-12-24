import re
def get_subfunction(control_type_name):
    """Map Control_Type name to subfunction value."""
    mapping = {
        "Enable Rx and Tx": 0x00,
        "Enable Rx and Disable Tx": 0x01,
        "Disable Rx and Enable Tx": 0x02,
        "Disable Rx and Tx": 0x03,
        "Enable Rx and Disable Tx with Address Info": 0x04,
        "Enable Rx and Tx  with Address Info": 0x05
    }
    return mapping.get(control_type_name, 0x00)  # Default to 0x00 if name not found

def get_communication_type(comm_type_name):
    """Map Communication_type name to communication type value."""
    mapping = {
        "Normal communication": 0x01,
        "Network Management": 0x02,
        "Normal comm and network management": 0x03
    }
    return mapping.get(comm_type_name, 0x00)  # Default to 0x00 if name not found

     
def form_reqmsg4srv28_withoutNIN(Control,communication, sprmib_flag):    
    sid = int("28", 16)
    if (sprmib_flag == True):
         subfunction = int(Control) | 0x80   #MSB is set if SPRMIB is requested.
    else:
         subfunction = int(Control)  
    req_bytes = [sid, subfunction,communication]
    print(f"{sid} {subfunction} {communication} ")
    return(req_bytes)

def form_reqmsg4srv28_withNIN(Control,communication,ninstring, sprmib_flag):    
    sid = int("28", 16)
    if (sprmib_flag == True):
         subfunction = int(Control) | 0x80   #MSB is set if SPRMIB is requested.
    else:
         subfunction = int(Control) 
    ninstring_without_spaces = re.sub(r"\s+", "", ninstring)
    
    nin_highbyte = int(ninstring_without_spaces[:2], 16)
    nin_lowbyte = int(ninstring_without_spaces[2:], 16)
    req_bytes = [sid, subfunction,communication,nin_highbyte, nin_lowbyte]
    print(f"{sid} {subfunction} {communication} {nin_highbyte} {nin_lowbyte}")
    return(req_bytes)  



if __name__ == "__main__":
     print(form_reqmsg4srv28_withNIN("05","01","00 0A",False))
     #pass

   
