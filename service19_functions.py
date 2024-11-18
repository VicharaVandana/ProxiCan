import re

def calculate_dtc_status_mask(bit0, bit1, bit2, bit3, bit4, bit5, bit6, bit7):
    # Create a binary string based on the checkbox states
    bits = [
        int(bit0.isChecked()),
        int(bit1.isChecked()),
        int(bit2.isChecked()),
        int(bit3.isChecked()),
        int(bit4.isChecked()),
        int(bit5.isChecked()),
        int(bit6.isChecked()),
        int(bit7.isChecked())
    ]
    
    # Combine bits into a binary number, with Bit 7 as the MSB and Bit 0 as the LSB
    binary_string = ''.join(map(str, bits[::-1]))  # Reverse the order for correct bit placement
    dtc_status_mask_decimal = int(binary_string, 2)
    #dtc_status_mask_hex = f"{dtc_status_mask_decimal:02X}"

    # Convert the binary string to a hexadecimal value
    #dtc_status_mask_hex = hex(int(binary_string, 2)).upper()
    
    # Return the hexadecimal result
    return dtc_status_mask_decimal

def getDTCFormatIdentifiername(FID):
     if(FID == "0x0"):
          return("SAE_J2012-DA_DTCFormat_00 ")
     elif(FID =="0x1") :
          return("ISO_14229-1_DTCFormat ")
     elif(FID == "0x2"):
          return("SAE_J1939-73_DTCFormat ") 
     elif(FID == "0x3"):
          return("ISO_11992-4_DTCFormat ") 
     elif(FID == "0x4"):
          return("SAE_J2012-DA_DTCFormat_04 ") 
     else:
          return(" ISO/SAE reserved ")

def form_reqmsg4srv19_subfun_3(DTCMaskRecord,DTCSnapshotRecordNumber,sprmib_flag): 
    sid = int("19", 16)
    subfun=int("3",16)
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

def form_reqmsg4srv19_subfun_4(DTCMaskRecord,DTCSnapshotRecordNumber,sprmib_flag): 
    sid = int("19", 16)
    subfun=int("4",16)
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

def form_reqmsg4srv19_subfun_5(DTCStoredDataRecordNumber,sprmib_flag): 
    sid = int("19", 16)
    subfun=int("5",16)
    if (sprmib_flag == True):
         subfunction = int(subfun) | 0x80   #MSB is set if SPRMIB is requested.
    else:
         subfunction = int(subfun)   
    DTCStoredDataRecordNumber_without_spaces = re.sub(r"\s+", "", DTCStoredDataRecordNumber)
    DTCStoredDataRecordNumber_hex = int(DTCStoredDataRecordNumber_without_spaces, 16)
    req_bytes = [sid, subfunction, DTCStoredDataRecordNumber_hex]
    print(f"{sid} {subfunction} {DTCStoredDataRecordNumber_hex}")
    return(req_bytes)

def form_reqmsg4srv19_subfun_6(DTCMaskRecord,DTCExtDataRecordNumber,sprmib_flag): 
    sid = int("19", 16)
    subfun=int("6",16)
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

def form_reqmsg4srv19_subfun_10(DTCMaskRecord,DTCExtDataRecordNumber,sprmib_flag): 
    sid = int("19", 16)
    subfun=int("10",16)
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

def form_reqmsg4srv19_subfun_7(DTCSeverityMaskRecord,sprmib_flag): 
    sid = int("19", 16)
    subfun=int("7",16)
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

def form_reqmsg4srv19_subfun_8(DTCSeverityMaskRecord,sprmib_flag): 
    sid = int("19", 16)
    subfun=int("8",16)
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

def form_reqmsg4srv19_subfun_9(DTCMaskRecord,sprmib_flag): 
    sid = int("19", 16)
    subfun=int("9",16)
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

def form_reqmsg4srv19_subfun_1(DTCStatusMask,sprmib_flag): 
    sid = int("19", 16)
    subfun=int("01",16)
    if (sprmib_flag == True):
         subfunction = int(subfun) | 0x80   #MSB is set if SPRMIB is requested.
    else:
         subfunction = int(subfun)   
    #DTCStatusMask_without_spaces = re.sub(r"\s+", "", DTCStatusMask)
    #DTCStatusMask_hex = int(DTCStatusMask_without_spaces, 16)

    
    req_bytes = [sid, subfunction, DTCStatusMask]
    print(f"{sid} {subfunction} {DTCStatusMask}")
    return(req_bytes)

def form_reqmsg4srv19_subfun_A(sprmib_flag): 
    sid = int("19", 16)
    subfun=int("0A",16)
    if (sprmib_flag == True):
         subfunction = int(subfun) | 0x80   #MSB is set if SPRMIB is requested.
    else:
         subfunction = int(subfun)   
    req_bytes = [sid, subfunction]
    print(f"{sid} {subfunction}")
    return(req_bytes)

def form_reqmsg4srv19_subfun_B(sprmib_flag): 
    sid = int("19", 16)
    subfun=int("0B",16)
    if (sprmib_flag == True):
         subfunction = int(subfun) | 0x80   #MSB is set if SPRMIB is requested.
    else:
         subfunction = int(subfun)   
    req_bytes = [sid, subfunction]
    print(f"{sid} {subfunction}")
    return(req_bytes)

def form_reqmsg4srv19_subfun_C(sprmib_flag): 
    sid = int("19", 16)
    subfun=int("0C",16)
    if (sprmib_flag == True):
         subfunction = int(subfun) | 0x80   #MSB is set if SPRMIB is requested.
    else:
         subfunction = int(subfun)   
    req_bytes = [sid, subfunction]
    print(f"{sid} {subfunction}")
    return(req_bytes)

def form_reqmsg4srv19_subfun_D(sprmib_flag): 
    sid = int("19", 16)
    subfun=int("0D",16)
    if (sprmib_flag == True):
         subfunction = int(subfun) | 0x80   #MSB is set if SPRMIB is requested.
    else:
         subfunction = int(subfun)   
    req_bytes = [sid, subfunction]
    print(f"{sid} {subfunction}")
    return(req_bytes)

def form_reqmsg4srv19_subfun_E(sprmib_flag): 
    sid = int("19", 16)
    subfun=int("0E",16)
    if (sprmib_flag == True):
         subfunction = int(subfun) | 0x80   #MSB is set if SPRMIB is requested.
    else:
         subfunction = int(subfun)   
    req_bytes = [sid, subfunction]
    print(f"{sid} {subfunction}")
    return(req_bytes)

def form_reqmsg4srv19_subfun_14(sprmib_flag): 
    sid = int("19", 16)
    subfun=int("14",16)
    if (sprmib_flag == True):
         subfunction = int(subfun) | 0x80   #MSB is set if SPRMIB is requested.
    else:
         subfunction = int(subfun)   
    req_bytes = [sid, subfunction]
    print(f"{sid} {subfunction}")
    return(req_bytes)

def form_reqmsg4srv19_subfun_15(sprmib_flag): 
    sid = int("19", 16)
    subfun=int("15",16)
    if (sprmib_flag == True):
         subfunction = int(subfun) | 0x80   #MSB is set if SPRMIB is requested.
    else:
         subfunction = int(subfun)   
    req_bytes = [sid, subfunction]
    print(f"{sid} {subfunction}")
    return(req_bytes)

def form_reqmsg4srv19_subfun_16(DTCExtDataRecordNumber,sprmib_flag): 
    sid = int("19", 16)
    subfun=int("16",16)
    if (sprmib_flag == True):
         subfunction = int(subfun) | 0x80   #MSB is set if SPRMIB is requested.
    else:
         subfunction = int(subfun)   
    DTCExtDataRecordNumber_without_spaces = re.sub(r"\s+", "", DTCExtDataRecordNumber)
    DTCExtDataRecordNumber_hex = int(DTCExtDataRecordNumber, 16)
    req_bytes = [sid, subfunction, DTCExtDataRecordNumber_hex]
    print(f"{sid} {subfunction} {DTCExtDataRecordNumber_hex}")
    return(req_bytes)

def form_reqmsg4srv19_subfun_18(DTCMaskRecord, DTCSnapshotRecordNumber, MemorySelection, sprmib_flag): 
    sid = int("19", 16)
    subfun=int("18",16)
    if (sprmib_flag == True):
         subfunction = int(subfun) | 0x80   #MSB is set if SPRMIB is requested.
    else:
         subfunction = int(subfun)   
    DTCMaskRecord_without_spaces = re.sub(r"\s+", "", DTCMaskRecord)
    DTC_highbyte = int(DTCMaskRecord_without_spaces[:2], 16)
    DTC_middlebyte = int(DTCMaskRecord_without_spaces[2:4], 16)
    DTC_lowbyte = int(DTCMaskRecord_without_spaces[4:], 16)
    DTCSnapshotRecordNumber_without_spaces = re.sub(r"\s+", "", DTCSnapshotRecordNumber)
    DTCSnapshotRecordNumber_hex = int(DTCSnapshotRecordNumber_without_spaces, 16)
    MemorySelection_without_spaces = re.sub(r"\s+", "", MemorySelection)
    MemorySelection_hex = int(MemorySelection_without_spaces, 16)
    req_bytes = [sid, subfunction, DTC_highbyte,DTC_middlebyte,DTC_lowbyte,DTCSnapshotRecordNumber_hex,MemorySelection_hex]
    print(f"{sid} {subfunction} {DTC_highbyte} {DTC_middlebyte} {DTC_lowbyte} {DTCSnapshotRecordNumber_hex} {MemorySelection_hex}")
    return(req_bytes)

def form_reqmsg4srv19_subfun_19(DTCMaskRecord, DTCExtDataRecordNumber, MemorySelection, sprmib_flag): 
    sid = int("19", 16)
    subfun=int("19",16)
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
    MemorySelection_without_spaces = re.sub(r"\s+", "", MemorySelection)
    MemorySelection_hex = int(MemorySelection_without_spaces, 16)
    req_bytes = [sid, subfunction, DTC_highbyte,DTC_middlebyte,DTC_lowbyte,DTCExtDataRecordNumber_hex,MemorySelection_hex]
    print(f"{sid} {subfunction} {DTC_highbyte} {DTC_middlebyte} {DTC_lowbyte} {DTCExtDataRecordNumber_hex} {MemorySelection_hex}")
    return(req_bytes)

def form_reqmsg4srv19_subfun_42(FunctionalGroupIdentifier, DTCSeverityMaskRecord, sprmib_flag): 
    sid = int("19", 16)
    subfun=int("42",16)
    if (sprmib_flag == True):
         subfunction = int(subfun) | 0x80   #MSB is set if SPRMIB is requested.
    else:
         subfunction = int(subfun)   
    FunctionalGroupIdentifier_without_spaces = re.sub(r"\s+", "", FunctionalGroupIdentifier)
    FunctionalGroupIdentifier_hex = int(FunctionalGroupIdentifier_without_spaces, 16)
    DTCSeverityMaskRecord_without_spaces = re.sub(r"\s+", "", DTCSeverityMaskRecord)
    DTC_highbyte = int(DTCSeverityMaskRecord_without_spaces[:2], 16)
    DTC_lowbyte = int(DTCSeverityMaskRecord_without_spaces[2:], 16)
    req_bytes = [sid, subfunction, DTC_highbyte,DTC_lowbyte,FunctionalGroupIdentifier_hex]
    print(f"{sid} {subfunction} {DTC_highbyte} {DTC_lowbyte} {FunctionalGroupIdentifier_hex}")
    return(req_bytes)

def form_reqmsg4srv19_subfun_55(FunctionalGroupIdentifier, sprmib_flag): 
    sid = int("19", 16)
    subfun=int("55",16)
    if (sprmib_flag == True):
         subfunction = int(subfun) | 0x80   #MSB is set if SPRMIB is requested.
    else:
         subfunction = int(subfun)   
    FunctionalGroupIdentifier_without_spaces = re.sub(r"\s+", "", FunctionalGroupIdentifier)
    FunctionalGroupIdentifier_hex = int(FunctionalGroupIdentifier_without_spaces, 16)
    req_bytes = [sid, subfunction, FunctionalGroupIdentifier_hex]
    print(f"{sid} {subfunction} {FunctionalGroupIdentifier_hex}")
    return(req_bytes)

if __name__ == "__main__":
     print(form_reqmsg4srv19_subfun_1("0A","0A",False))
     #pass

   
