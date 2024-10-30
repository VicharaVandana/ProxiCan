import re
import general as gen

def get_data_identifier(index):
     if(index == 0):
        return(0x10)
     elif(index == 1):
        return(0x01)
     elif(index == 2):
        return(0x00)


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
      
def form_reqmsg4srv34(data_identifier,alfid,mem_add,mem_size):

    alfid_without_spaces = re.sub(r"\s+", "", alfid)
    alfid_hex=int(alfid_without_spaces,16)

    sid = int("34", 16)


    mem_add_without_spaces=re.sub(r"\s+", "", mem_add)


    mem_size_without_spaces=re.sub(r"\s+", "", mem_size)



    paired_mem_add = pair_hex_values([mem_add_without_spaces])
    paired_mem_size=pair_hex_values([mem_size_without_spaces])

    mem_add_decimal_values = [int(hex_val, 16) for hex_val in paired_mem_add]
    mem_size_decimal_values = [int(hex_val, 16) for hex_val in paired_mem_size]
    distr=str(data_identifier)
    DI=int(distr,16)

    req_bytes = [sid] + [data_identifier] + [alfid_hex] + mem_add_decimal_values + mem_size_decimal_values 
    print(f"{sid} {data_identifier} {alfid_hex} {' '.join(map(str, mem_add_decimal_values))} {' '.join(map(str, mem_size_decimal_values))} ")
    return(req_bytes)
    

if __name__ == "__main__":
     print(form_reqmsg4srv34("10","12","20 48","8C"))



