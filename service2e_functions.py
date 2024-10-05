import re

def hex_bytes_to_int_list(hex_string):
    # Regular expression to match two hex characters (a byte)
    byte_pattern = re.compile(r'[0-9A-Fa-f]{2}')
    
    # Find all matching two-character hex bytes in the input string
    bytes_list = byte_pattern.findall(hex_string)
    
    # Convert hex strings to integers
    int_list = [int(byte, 16) for byte in bytes_list]
    
    return int_list
        
def form_reqmsg4srv2E(didstring, datavaluestring):
    didstring_without_spaces = re.sub(r"\s+", "", didstring)
    datastring_without_spaces = re.sub(r"\s+", "", datavaluestring)
    #SID part
    sid = int("2E", 16)

    #DID part
    did_highbyte = int(didstring_without_spaces[:2], 16)
    did_lowbyte = int(didstring_without_spaces[2:], 16)

    req_bytes = [sid, did_highbyte, did_lowbyte]

    #Data Values part
    data_bytes = hex_bytes_to_int_list(datastring_without_spaces)

    req_bytes.extend(data_bytes)

    print(f"{sid} {did_highbyte} {did_lowbyte}, {datastring_without_spaces}")
    return(req_bytes)
    

if __name__ == "__main__":
     print(form_reqmsg4srv2E("10 0A", "A3F122 6D 3A5B  FF FF FF"))