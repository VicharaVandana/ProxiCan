from securityaccesslogic import *

def getsecurityaccessdetails(index):
     if(index == 0):
          securitydetails = {
                "subfunction_getseed": 0x01,
                "subfunction_validatekey": 0x02,
                "seedLength": 2, #value in Bytes
                "keyLength": 2, #value in Bytes
                "SecurityFunction": "getKey4mSeed_SecuLvl_01"
                }
     elif(index == 1):
          securitydetails = {
                "subfunction_getseed": 0x61,
                "subfunction_validatekey": 0x62,
                "seedLength": 2, #value in Bytes
                "keyLength": 1, #value in Bytes
                "SecurityFunction": "getKey4mSeed_SecuLvl_31"
                }
     else:
          securitydetails = {
                "subfunction_getseed": 0x00,
                "subfunction_validatekey": 0x00,
                "seedLength": 0, #value in Bytes
                "keyLength": 0, #value in Bytes
                "SecurityFunction": "getKey4mSeed_SecuLvl_00"
                }
     
     return(securitydetails)
     

def number_to_bytes(number, length, byteorder='big'):
    # Convert the number to a byte array
    byte_array = number.to_bytes(length, byteorder)
    
    # Convert the byte array into a list of individual bytes
    byte_list = list(byte_array)
    
    return byte_list

def bytes_to_number(byte_array, byteorder='big'):
    
    # Convert the byte array to a single integer
    number = int.from_bytes(byte_array, byteorder=byteorder)  # 'big' for big-endian byte order
    
    return number
   
        
def form_reqmsg4srv27_getSeed(subfunction):    
    sid = int("27", 16)
    req_bytes = [sid, subfunction]
    print(f"{sid} {subfunction}")
    return(req_bytes)

def form_reqmsg4srv27_validateKey(subfunction,key,keylength):    
    sid = int("27", 16)
    req_bytes = [sid, subfunction]
    keybytes = number_to_bytes(key, keylength, 'big')
    req_bytes.extend(keybytes)
    print(f"{sid} {subfunction} {keybytes}")
    return(req_bytes)
    

if __name__ == "__main__":
     print(locals()["getKey4mSeed_SecuLvl_01"](0xFFFF))
     byte_list = number_to_bytes(300, 2, 'big')  # You can use 'little' as well for little-endian
     print(byte_list)

   
