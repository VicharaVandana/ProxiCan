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
      
def form_reqmsg4srv23(alfid,mem_add,mem_size):
    #alfid_without_spaces = re.sub(r"\s+", "", alfid)
    alfid_hex=int(alfid,16)

    sid = int("23", 16)


    mem_add_without_spaces=re.sub(r"\s+", "", mem_add)


    mem_size_without_spaces=re.sub(r"\s+", "", mem_size)



    paired_mem_add = pair_hex_values([mem_add_without_spaces])
    paired_mem_size=pair_hex_values([mem_size_without_spaces])
    mem_add_decimal_values = [int(hex_val, 16) for hex_val in paired_mem_add]
    mem_size_decimal_values = [int(hex_val, 16) for hex_val in paired_mem_size]
    req_bytes = [sid] + [alfid_hex] + mem_add_decimal_values + mem_size_decimal_values
    print(f"{sid} {alfid_hex} {' '.join(map(str, mem_add_decimal_values))} {' '.join(map(str, mem_size_decimal_values))}")
    return(req_bytes)
    

if __name__ == "__main__":
     print(form_reqmsg4srv23("24","20 48 13 92","01 03"))



