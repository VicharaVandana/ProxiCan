import re
import general as gen

def get_subfunction(index):
     if(index == 0):
        return(0x01)
     elif(index == 1):
        return(0x02)
     elif(index == 2):
        return(0x03)


def hex_bytes_to_int_list(hex_string):
    # Regular expression to match two hex characters (a byte)
    byte_pattern = re.compile(r'[0-9A-Fa-f]{2}')
    
    # Find all matching two-character hex bytes in the input string
    bytes_list = byte_pattern.findall(hex_string)
    
    # Convert hex strings to integers
    int_list = [int(byte, 16) for byte in bytes_list]
    
    return int_list
      
def form_reqmsg4srv31(sub_functions,routine_identifier,sprmib_flag):

    RID_without_spaces = re.sub(r"\s+", "", routine_identifier)

    rid_highbyte = int(RID_without_spaces[:2], 16)
    rid_lowbyte = int(RID_without_spaces[2:], 16)
    sid = int("31", 16)

    if (sprmib_flag == True):
         subfunction = int(sub_functions) | 0x80   #MSB is set if SPRMIB is requested.
    else:
         subfunction = int(sub_functions)   


    req_bytes = [sid, subfunction, rid_highbyte, rid_lowbyte]

    print(f"{sid} {subfunction} {rid_highbyte} {rid_lowbyte}")
    return(req_bytes)
    

if __name__ == "__main__":
     print(form_reqmsg4srv31("01","02 01",False))



