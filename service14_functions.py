import re

def hex_bytes_to_int_list(hex_string):
    # Regular expression to match three hex characters (a byte)
    byte_pattern = re.compile(r'[0-9A-Fa-f]{3}')
    
    # Find all matching two-character hex bytes in the input string
    bytes_list = byte_pattern.findall(hex_string)
    
    # Convert hex strings to integers
    int_list = [int(byte, 16) for byte in bytes_list]
    
    return int_list
        
def form_reqmsg4srv14(dtcstring):
    dtcstring_without_spaces = re.sub(r"\s+", "", dtcstring)
    #SID part
    sid = int("14", 16)

    #DID part
    did_highbyte = int(dtcstring_without_spaces[:2], 16)
    did_middlebyte = int(dtcstring_without_spaces[2:4], 16)
    did_lowbyte = int(dtcstring_without_spaces[4:], 16)

    req_bytes = [sid, did_highbyte,did_middlebyte, did_lowbyte]


    print(f"{sid} {did_highbyte} {did_middlebyte} {did_lowbyte}")
    return(req_bytes)
    

if __name__ == "__main__":
     print(form_reqmsg4srv14("FF FF 33"))