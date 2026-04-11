import re


        
def form_reqmsg4srv22(didstring):
    didstring_without_spaces = re.sub(r"\s+", "", didstring)
    sid = int("22", 16)
    did_highbyte = int(didstring_without_spaces[:2], 16)
    did_lowbyte = int(didstring_without_spaces[2:], 16)
    req_bytes = [sid, did_highbyte, did_lowbyte]
    print(f"{sid} {did_highbyte} {did_lowbyte}")
    return(req_bytes)
    

if __name__ == "__main__":
     print(form_reqmsg4srv22("10 0A"))

   
