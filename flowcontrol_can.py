from environment import *

if RUNNING_ON_RASPBERRYPI == True:
    import can
elif RUNNING_ON_WINDOWS_WAVESHARE == True:
    from waveshare_wrapper import Message as can_Message
else:
    pass

import time
import datetime
import configure as conf
import general as gen


def receive_specific_can_message(target_id, timeout = 2):
    """
    Wait for a specific CAN message ID within a given timeout period.
    """
    start_time = time.time()

    while True:
        # Calculate the remaining time
        remaining_time = timeout - (time.time() - start_time)

        if remaining_time <= 0:
            print("Timeout: Message not received.")
            return None

        # Wait for a message, with the remaining time as the timeout
        message = conf.rx.recv(timeout=remaining_time)

        if message:
            if message.arbitration_id == target_id:
                print(f"Received message: ID=0x{message.arbitration_id:X}, Data={message.data.hex()}")
                # Record the time and log traffic
                recv_time = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f')
                databytes = list(message.data)
                gen.logcantraffic("RX", recv_time, message.arbitration_id, len(databytes), databytes)
                return message
            else:
                # Ignore other CAN IDs
                continue

###############################################################################################################
##                                SECTION TO SEND DATA                                                       ##
###############################################################################################################

#Function to Send First frame
def send_firstframe(n_sdu):
    nsdu_length = len(n_sdu)
    pci_H = 0x10 | ((nsdu_length & 0xF00) >> 8)
    pci_L = (nsdu_length & 0xFF)
    pci = [pci_H, pci_L]
    nsdu_FFchunk = n_sdu[:6]    #First 6 bytes are sent in First Frame

    databytes = pci + nsdu_FFchunk
    
    is_ext = (conf.id_type == "EXTENDED")
    
    if RUNNING_ON_RASPBERRYPI == True:
        can_msg = can.Message(arbitration_id=conf.diag_req_msgid, data=databytes, is_extended_id=is_ext, is_fd=False)
    elif RUNNING_ON_WINDOWS_WAVESHARE == True:
        can_msg = can_Message(arbitration_id=conf.diag_req_msgid, data=databytes, is_extended_id=is_ext, is_fd=False)
    
    conf.tx.send(can_msg)
    
    # Traffic logging
    send_time = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f')
    gen.logcantraffic("TX", send_time, conf.diag_req_msgid, len(databytes), databytes)

    canmsg = f'TX\tID:{hex(can_msg.arbitration_id)}\tdatalength:{len(can_msg.data)}bytes\t data:[{" ".join(hex(number) for number in can_msg.data)}].'
    gen.tp_log("First Frame Sent", canmsg)
    print(f"The First frame sent : {can_msg}")

    return 


#Function to Send Consecutive frame
def send_consecutiveframe(sequence_number, data_chunk, cf_gap_time_min):
    pci = 0x20 | (sequence_number & 0x0F)
    databytes = [pci] + data_chunk
    
    # Pad to 8 bytes for Standard CAN if necessary (optional but good practice)
    if len(databytes) < 8:
        databytes += [0x00] * (8 - len(databytes))

    is_ext = (conf.id_type == "EXTENDED")
    
    if RUNNING_ON_RASPBERRYPI == True:
        can_msg = can.Message(arbitration_id=conf.diag_req_msgid, data=databytes, is_extended_id=is_ext, is_fd=False)
    elif RUNNING_ON_WINDOWS_WAVESHARE == True:
        can_msg = can_Message(arbitration_id=conf.diag_req_msgid, data=databytes, is_extended_id=is_ext, is_fd=False)
    
    conf.tx.send(can_msg)
    
    send_time = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f')
    gen.logcantraffic("TX", send_time, conf.diag_req_msgid, len(databytes), databytes)
    
    time.sleep(cf_gap_time_min)
    canmsg = f'TX\tID:{hex(can_msg.arbitration_id)}\tdatalength:{len(can_msg.data)}bytes\t data:[{" ".join(hex(number) for number in can_msg.data)}].'
    gen.tp_log(f"Consecutive Frame - {sequence_number} Sent", canmsg)
    print(f"The Consecutive Frame - {sequence_number} sent : {can_msg}")

    return True


#Function to process Flow Control Frame
def process_flowcontrolframe(msg):
    data = msg.data
    pci = data[0] & 0xF0
    if (pci == 0x30):
        flow_status = data[0] & 0x0F
        block_size = data[1]
        st_min = data[2]
        return(flow_status,block_size,st_min)
    else: 
        print(f"Not a Flow Control Frame")
        return(None)


#Function to send small chunk (data <= 7 bytes)
def send_small_data(n_sdu):
    datalength = len(n_sdu)
    pci = 0x00 | (datalength & 0x0F)

    databytes = [pci] + n_sdu
    # Pad to 8 bytes
    if len(databytes) < 8:
        databytes += [0x00] * (8 - len(databytes))

    is_ext = (conf.id_type == "EXTENDED")

    if RUNNING_ON_RASPBERRYPI == True:
        can_msg = can.Message(arbitration_id=conf.diag_req_msgid, data=databytes, is_extended_id=is_ext, is_fd=False)
    elif RUNNING_ON_WINDOWS_WAVESHARE == True:
        can_msg = can_Message(arbitration_id=conf.diag_req_msgid, data=databytes, is_extended_id=is_ext, is_fd=False)
    
    conf.tx.send(can_msg)
    
    send_time = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f')
    gen.logcantraffic("TX", send_time, conf.diag_req_msgid, len(databytes), databytes)

    canmsg = f'TX\tID:{hex(can_msg.arbitration_id)}\tdatalength:{len(can_msg.data)}bytes\t data:[{" ".join(hex(number) for number in can_msg.data)}].'
    gen.tp_log("Single Frame Sent", canmsg)
    print(f"The single frame sent : {can_msg}")

    return True
        

#Function to send big chunk (data > 7 bytes)
def send_big_data(n_sdu):
    datalength = len(n_sdu)
    send_firstframe(n_sdu)
    pending_datalength = datalength - 6 
    pending_data = n_sdu[6:]

    wait4FCFrame = True
    total_cf_count = 1
    block_count = 1
    while(wait4FCFrame == True):
        received_message = receive_specific_can_message(target_id=conf.diag_resp_msgid, timeout=conf.flowcontrolframe_maxwaittime)

        if received_message:
            flowParameters = process_flowcontrolframe(received_message)
            if(flowParameters != None):
                flow_status = flowParameters[0]
                if (flow_status == 0):
                    block_size = flowParameters[1]
                    st_min = flowParameters[2]
                    if (st_min == 0):
                        cf_gap_time_min = 1/1000
                    elif (st_min in range(1,128)):
                        cf_gap_time_min = st_min/1000
                    else:
                        cf_gap_time_min = 1/1000
                    
                    cf_count = 1
                    if (block_size == 0):
                        block_size = 4096//7 + 1
                    while((pending_datalength > 0) and (cf_count <= block_size)):
                        seq_num = total_cf_count % 16 # Correct ISO-TP sequence
                        current_chunk = pending_data[:7]
                        send_consecutiveframe(seq_num,current_chunk,cf_gap_time_min)
                        pending_data = pending_data[7:]
                        cf_count = cf_count + 1
                        total_cf_count = total_cf_count + 1
                        pending_datalength = pending_datalength - 7

                    if(len(pending_data) == 0):
                        wait4FCFrame = False
                        print(f"A full N-SDU of {len(n_sdu)} bytes sent.")
                        return True
                    elif(cf_count >  block_size):
                        wait4FCFrame = True 
                        block_count = block_count + 1
                elif(flow_status == 1):
                    gen.tp_log("Flow control frame with Flow Status = WAIT Recieved", received_message)
                elif(flow_status == 2):
                    gen.tp_log("Flow control frame with Flow Status = OVERFLOW Recieved.", received_message)
                    return False
            else:
                gen.tp_log("Non Flow control message recieved over Diag Resp ID", received_message)
                return False
        else:
            gen.tp_log(f"No Flow control message recieved before timeout {conf.flowcontrolframe_maxwaittime}", received_message)
            return False
    return True

def send_data(n_sdu):
    length = len(n_sdu)
    if(length < 8):
        return(send_small_data(n_sdu))
    elif(length < 4096):
        return(send_big_data(n_sdu))
    else:
        print(f"Data too large for Standard CAN.")
        return False

###############################################################################################################
##                             SECTION TO RECIEVE DATA                                                       ##
###############################################################################################################

def send_flowcontrolframe(flow_status, block_size, st_min):
    databytes = [0x30 | (flow_status & 0xF), block_size, st_min]
    # Pad to 8 bytes
    databytes += [0x00] * (8 - len(databytes))
    
    is_ext = (conf.id_type == "EXTENDED")
    
    if RUNNING_ON_RASPBERRYPI == True:
        can_msg = can.Message(arbitration_id=conf.diag_req_msgid, data=databytes, is_extended_id=is_ext, is_fd=False)
    elif RUNNING_ON_WINDOWS_WAVESHARE == True:
        can_msg = can_Message(arbitration_id=conf.diag_req_msgid, data=databytes, is_extended_id=is_ext, is_fd=False)
    
    conf.tx.send(can_msg)
    
    send_time = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f')
    gen.logcantraffic("TX", send_time, conf.diag_req_msgid, len(databytes), databytes)

    canmsg = f'TX\tID:{hex(can_msg.arbitration_id)}\tdatalength:{len(can_msg.data)}bytes\t data:[{" ".join(hex(number) for number in can_msg.data)}].'
    gen.tp_log("FLow Control Frame Sent", canmsg)
    return True


def recieve_data():
    n_sdu_rx = []
    received_message = receive_specific_can_message(target_id=conf.diag_resp_msgid)

    if received_message:
        data = received_message.data
        frametype = data[0] & 0xF0
        
        if(frametype == 0x00):  # Single frame
            datalength = data[0] & 0x0F
            n_sdu_rx.extend(data[1:1+datalength])
            canmsg = f'RX\tID:{hex(conf.diag_resp_msgid)}\tdatalength:{datalength}bytes\t data:[{" ".join(hex(number) for number in n_sdu_rx)}].'
            gen.tp_log("Single Frame Recieved", canmsg)
            return(n_sdu_rx)
        
        elif(frametype == 0x10):  # First frame
            n_sdu_length = (((data[0] & 0x0F)<<8) | (data[1]))
            n_sdu_rx.extend(data[2:])
            pendingbyteslength = n_sdu_length - len(data[2:])
            canmsg = f'RX\tID:{hex(conf.diag_resp_msgid)}\tnsdulength:{n_sdu_length}bytes\t data:[{" ".join(hex(number) for number in n_sdu_rx)}].'
            gen.tp_log("First Frame Recieved", canmsg)
        else:
            return False
    else:
        gen.tp_log(f"No Frame recieved before timeout 2s", None)
        return False

    send_flowcontrolframe(0, 0, 50)
    oldseqnum = 0
    while(pendingbyteslength > 0):
        received_message = receive_specific_can_message(target_id=conf.diag_resp_msgid)
        if received_message:
            data = received_message.data
            frametype = data[0] & 0xF0
            if(frametype == 0x20):
                seqnum = data[0] & 0x0F
                expected_seqnum = (oldseqnum + 1) % 16
                chunk = data[1:]
                if len(chunk) > pendingbyteslength:
                    chunk = chunk[:pendingbyteslength]
                
                n_sdu_rx.extend(chunk)
                canmsg = f'RX\tID:{hex(conf.diag_resp_msgid)}\tdata:[{" ".join(hex(number) for number in n_sdu_rx)}].'
                gen.tp_log(f"Consecutive Frame - {seqnum} Recieved", canmsg)
                pendingbyteslength -= len(chunk)
                oldseqnum = seqnum
            else:
                return False            
        else:
            gen.tp_log(f"No Frame recieved before timeout 2s", None)
            return False
    return(n_sdu_rx)
