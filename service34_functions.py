import re
import general as gen

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
      
def form_reqmsg4srv34(dfi,alfid,mem_add, mem_size):
    #alfid_without_spaces = re.sub(r"\s+", "", alfid)
    dfi_hex = int(dfi, 16)
    alfid_hex=int(alfid,16)

    sid = int("34", 16)


    mem_add_without_spaces=re.sub(r"\s+", "", mem_add)


    mem_size_without_spaces=re.sub(r"\s+", "", mem_size)



    paired_mem_add = pair_hex_values([mem_add_without_spaces])
    paired_mem_size=pair_hex_values([mem_size_without_spaces])

    mem_add_decimal_values = [int(hex_val, 16) for hex_val in paired_mem_add]
    mem_size_decimal_values = [int(hex_val, 16) for hex_val in paired_mem_size]

    req_bytes = [sid] + [dfi_hex] +[alfid_hex] + mem_add_decimal_values + mem_size_decimal_values 
    print(f"{sid} {dfi_hex} {alfid_hex} {' '.join(map(str, mem_add_decimal_values))} {' '.join(map(str, mem_size_decimal_values))} ")
    return(req_bytes)  
    

if __name__ == "__main__":
     print(form_reqmsg4srv34("00","44","00 50 00 00","00 17 ff e0"))



