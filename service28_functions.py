import re

def get_subfunction(index):
     if(index == 0):
        return(0x00)
     elif(index == 1):
        return(0x01)
     elif(index == 2):
        return(0x02)
     elif(index == 3):
        return(0x03)
     elif(index == 4):
        return(0x04)
     elif(index == 5):
        return(0x05)
     else:
          return(0x00)
     
def getsubfunction_name(con_type):
     if(con_type == 0x00):
          return("EnableRxandTx")
     elif(con_type == 0x01) :
          return("EnableRxAndDisableTx")
     elif(con_type == 0x02):
          return("DisableRxAndEnableTx") 
     elif(con_type == 0x03):
          return("DisableRxAndTx")
     elif(con_type == 0x04):
          return("enableRxAndDisableTxWithEnhancedAddressInformation")
     elif(con_type == 0x05):
          return("enableRxAndTxWithEnhancedAddressInformation")
     

def get_communication_type(index):
     if(index == 0):
        return(0x01)
     elif(index == 1):
        return(0x02)
     elif(index == 2):
        return(0x03)
     else:
          return(0x00)
     
def get_communication_type_name(index):
     if(index == 1):
        return("Normal communication")
     elif(index == 2):
        return("Network Management")
     elif(index == 3):
        return("Normal comm and network management")
     else:
          return("")
     
def form_reqmsg4srv28_withoutNIN(Control,communication, sprmib_flag):    
    sid = int("28", 16)
    if (sprmib_flag == True):
         subfunction = int(Control) | 0x80   #MSB is set if SPRMIB is requested.
    else:
         subfunction = int(Control)  
    req_bytes = [sid, subfunction,communication]
    print(f"{sid}{subfunction}{communication} ")
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
    print(f"{sid}{subfunction}{communication} {nin_highbyte} {nin_lowbyte}")
    return(req_bytes)  




#    ninstring_without_spaces = re.sub(r"\s+", "", didstring)
#    sid = int("22", 16)
#    nin_highbyte = int(ninstring_without_spaces[:2], 16)
#    nin_lowbyte = int(ninstring_without_spaces[2:], 16)
#    req_bytes = [sid, subfunction,communication,nin_highbyte, nin_lowbyte]
#    print(f"{sid}{subfunction}{communication} {nin_highbyte} {nin_lowbyte}")
#    return(req_bytes)
    

if __name__ == "__main__":
     print(form_reqmsg4srv28_withNIN("05","01","00 0A",False))
     #pass

   
