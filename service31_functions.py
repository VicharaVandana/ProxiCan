import re
import general as gen

def get_subfunction(index):
     if(index == 0):
        return(0x01)
     elif(index == 1):
        return(0x02)
     elif(index == 2):
        return(0x03)
     
def get_subfunction_name(index):
     if(index == 0):
        return("Start Routine")
     elif(index == 1):
        return("Stop Routine")
     elif(index == 2):
        return("Requesting Routine Results")
     else:
          return("")

def pair_hex_values(hex_list):
    # Remove any spaces or unwanted characters from the string
    hex_string = ''.join(hex_list).replace(" ", "")
    
    # Ensure the length of the string is even
    if len(hex_string) % 2 != 0:
        gen.log_action("UDS Request Fail", "ff Request failed due to invalid memory size.")
        return
    
    # Pair the hex string in 2-digit pairs
    paired_list = [hex_string[i:i+2] for i in range(0, len(hex_string), 2)]
    
    return paired_list

def hex_bytes_to_int_list(hex_string):
    # Regular expression to match two hex characters (a byte)
    byte_pattern = re.compile(r'[0-9A-Fa-f]{2}')
    
    # Find all matching two-character hex bytes in the input string
    bytes_list = byte_pattern.findall(hex_string)
    
    # Convert hex strings to integers
    int_list = [int(byte, 16) for byte in bytes_list]
    
    return int_list
      
def form_reqmsg4srv31_without_SR(sub_functions,routine_identifier,sprmib_flag):

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

def form_reqmsg4srv31_with_SR(sub_functions,routine_identifier,status_record,sprmib_flag):

    RID_without_spaces = re.sub(r"\s+", "", routine_identifier)

    rid_highbyte = int(RID_without_spaces[:2], 16)
    rid_lowbyte = int(RID_without_spaces[2:], 16)
    sid = int("31", 16)

    SR_without_spaces = re.sub(r"\s+", "", status_record)   

    if (sprmib_flag == True):
         subfunction = int(sub_functions) | 0x80   #MSB is set if SPRMIB is requested.
    else:
         subfunction = int(sub_functions)   

    paired_SR = pair_hex_values([SR_without_spaces])

    SR_decimal_values = [int(hex_val, 16) for hex_val in paired_SR]

    req_bytes = [sid, subfunction, rid_highbyte, rid_lowbyte] + SR_decimal_values

    print(f"{sid} {subfunction} {rid_highbyte} {rid_lowbyte} {' '.join(map(str, SR_decimal_values))}")
    return(req_bytes)
    

if __name__ == "__main__":
     print(form_reqmsg4srv31_without_SR("01","02 01",False))



