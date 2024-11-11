import re

def get_subfunction(index):
     if(index == 0):
        return(0x01)
     elif(index == 1):
        return(0x02)
     elif(index == 2):
        return(0x04)
     elif(index == 3):
        return(0x06)
     elif(index == 4):
        return(0x07)
     elif(index == 5):
        return(0x08)
     elif(index == 6):
        return(0x09)
     elif(index == 7):
        return(0x0A)
     elif(index == 8):
        return(0x0C)
     elif(index == 9):
        return(0x0E)
     elif(index == 10):
        return([0x14,0xFF,0xFF,0xFF])
     else:
          return(0x00)
     
def getsubfunction_name(subfun):
     if(subfun == 0x01):
          return("Report Number of DTC by Status Mask")
     elif(subfun == 0x02) :
          return("Report DTC by Status Mask")
     elif(subfun == 0x04):
          return("Report DTC Snapshot Record by DTC Number") 
     elif(subfun == 0x06):
          return("Report DTC ExtData Record by DTC Number")
     elif(subfun == 0x07):
          return("Report Number of DTC by Severity Mask Record")
     elif(subfun == 0x08):
          return("Report DTC by Severity Mask Record")
     elif(subfun == 0x09) :
          return("Report Severity Information of DTC")
     elif(subfun == 0x0A):
          return("Report Supported DTC") 
     elif(subfun == 0x0C):
          return("Report First Confirmed DTC")
     elif(subfun == 0x0E):
          return("Report Most Recent Confirmed DTC")
     elif(subfun == [0x14,0xFF,0xFF,0xFF]):
          return("Fault Memory Clear")

     
def form_reqmsg4srv19_subfun_3_4(subfun,DTCMaskRecord,DTCSnapshotRecordNumber,sprmib_flag): 
    sid = int("19", 16)
    if (sprmib_flag == True):
         subfunction = int(subfun) | 0x80   #MSB is set if SPRMIB is requested.
    else:
         subfunction = int(subfun)   
    DTCMaskRecord_without_spaces = re.sub(r"\s+", "", DTCMaskRecord)
    DTC_highbyte = int(DTCMaskRecord_without_spaces[:2], 16)
    DTC_middlebyte = int(DTCMaskRecord_without_spaces[2:4], 16)
    DTC_lowbyte = int(DTCMaskRecord_without_spaces[4:], 16)
    DTCSnapchotRecordNumber_without_spaces = re.sub(r"\s+", "", DTCSnapshotRecordNumber)
    DTCSnapshotRecordNumber_hex = int(DTCSnapchotRecordNumber_without_spaces, 16)
    req_bytes = [sid, subfunction, DTC_highbyte,DTC_middlebyte,DTC_lowbyte,DTCSnapshotRecordNumber_hex]
    print(f"{sid} {subfunction} {DTC_highbyte} {DTC_middlebyte} {DTC_lowbyte} {DTCSnapshotRecordNumber_hex}")
    return(req_bytes)

def form_reqmsg4srv19_subfun_6_10(subfun,DTCMaskRecord,DTCExtDataRecordNumber,sprmib_flag): 
    sid = int("19", 16)
    if (sprmib_flag == True):
         subfunction = int(subfun) | 0x80   #MSB is set if SPRMIB is requested.
    else:
         subfunction = int(subfun)   
    DTCMaskRecord_without_spaces = re.sub(r"\s+", "", DTCMaskRecord)
    DTC_highbyte = int(DTCMaskRecord_without_spaces[:2], 16)
    DTC_middlebyte = int(DTCMaskRecord_without_spaces[2:4], 16)
    DTC_lowbyte = int(DTCMaskRecord_without_spaces[4:], 16)
    DTCExtDataRecordNumber_without_spaces = re.sub(r"\s+", "", DTCExtDataRecordNumber)
    DTCExtDataRecordNumber_hex = int(DTCExtDataRecordNumber_without_spaces, 16)
    req_bytes = [sid, subfunction, DTC_highbyte,DTC_middlebyte,DTC_lowbyte,DTCExtDataRecordNumber_hex]
    print(f"{sid} {subfunction} {DTC_highbyte} {DTC_middlebyte} {DTC_lowbyte} {DTCExtDataRecordNumber_hex}")
    return(req_bytes)

def form_reqmsg4srv19_subfun_7_8(subfun,DTCSeverityMaskRecord,sprmib_flag): 
    sid = int("19", 16)
    if (sprmib_flag == True):
         subfunction = int(subfun) | 0x80   #MSB is set if SPRMIB is requested.
    else:
         subfunction = int(subfun)   
    DTCSeverityMaskRecord_without_spaces = re.sub(r"\s+", "", DTCSeverityMaskRecord)
    DTC_highbyte = int(DTCSeverityMaskRecord_without_spaces[:2], 16)
    DTC_lowbyte = int(DTCSeverityMaskRecord_without_spaces[2:], 16)
    req_bytes = [sid, subfunction, DTC_highbyte,DTC_lowbyte]
    print(f"{sid} {subfunction} {DTC_highbyte} {DTC_lowbyte} ")
    return(req_bytes)

def form_reqmsg4srv19_subfun_9(subfun,DTCMaskRecord,sprmib_flag): 
    sid = int("19", 16)
    if (sprmib_flag == True):
         subfunction = int(subfun) | 0x80   #MSB is set if SPRMIB is requested.
    else:
         subfunction = int(subfun)   
    DTCMaskRecord_without_spaces = re.sub(r"\s+", "", DTCMaskRecord)
    DTC_highbyte = int(DTCMaskRecord_without_spaces[:2], 16)
    DTC_middlebyte = int(DTCMaskRecord_without_spaces[2:4], 16)
    DTC_lowbyte = int(DTCMaskRecord_without_spaces[4:], 16)
    req_bytes = [sid, subfunction, DTC_highbyte,DTC_middlebyte,DTC_lowbyte]
    print(f"{sid} {subfunction} {DTC_highbyte} {DTC_middlebyte} {DTC_lowbyte}")
    return(req_bytes)

def form_reqmsg4srv19_subfun_1_2_0F_11_12_13(subfun,DTCStatusMask,sprmib_flag): 
    sid = int("19", 16)
    if (sprmib_flag == True):
         subfunction = int(subfun) | 0x80   #MSB is set if SPRMIB is requested.
    else:
         subfunction = int(subfun)   
    DTCStatusMask_without_spaces = re.sub(r"\s+", "", DTCStatusMask)
    DTCStatusMask_hex = int(DTCStatusMask_without_spaces, 16)
    req_bytes = [sid, subfunction, DTCStatusMask_hex]
    print(f"{sid} {subfunction} {DTCStatusMask_hex}")
    return(req_bytes)

def form_reqmsg4srv19_subfun_A_B_C_D_E_14_15(subfun,sprmib_flag): 
    sid = int("19", 16)
    if (sprmib_flag == True):
         subfunction = int(subfun) | 0x80   #MSB is set if SPRMIB is requested.
    else:
         subfunction = int(subfun)   
    req_bytes = [sid, subfunction]
    print(f"{sid} {subfunction}")
    return(req_bytes)

def form_reqmsg4srv19_subfun_clear(sprmib_flag): 
    req_bytes = [0x14,0xff,0xff,0xff]
    print(req_bytes)
    return(req_bytes)


if __name__ == "__main__":
     print(form_reqmsg4srv19_subfun_1_2_0F_11_12_13("0A","0A",False))
     #pass

   
