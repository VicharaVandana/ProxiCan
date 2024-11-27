from environment import *

if RUNNING_ON_RASPBERRYPI == True:
    import can
import time
import datetime
import configure as conf
import general as gen


def receive_specific_can_message(target_id, timeout = 5):
    """
    Wait for a specific CAN message ID within a given timeout period.
    
    :param interface: The CAN interface to listen on (e.g., 'can0').
    :param target_id: The CAN ID of the message to wait for.
    :param timeout: Time in seconds to wait for the message.
    :return: The received CAN message or None if timeout occurs.
    """

    #print(f"Waiting for message with ID 0x{target_id:X} on {conf.can_channel} for {timeout} seconds...")

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
                # Record the time before sending
                send_time = datetime.datetime.fromtimestamp(message.timestamp).strftime('%Y-%m-%d %H:%M:%S.%f')
                databytes = list(message.data)
                #gen.logcantraffic("RX", send_time, message.arbitration_id, len(message.data.hex()), message.data.hex())
                gen.logcantraffic("RX", send_time, message.arbitration_id, len(databytes), databytes)
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
    if(nsdu_length > 4095):
        #Frame pci format 6 5 4 3 2 1: 6 and 5 is 0x1000 and 4:1 is FF_DL
        pci_6 = 0x10
        pci_5 = 0x00
        pci_4 = ((nsdu_length & 0xFF000000) >> 24)
        pci_3 = ((nsdu_length & 0xFF0000) >> 16)
        pci_2 = ((nsdu_length & 0xFF00) >> 8)
        pci_1 = ((nsdu_length & 0xFF))
        
        pci = [pci_6, pci_5, pci_4, pci_3, pci_2, pci_1]
        nsdu_FFchunk = n_sdu[:58]    #First 58 bytes are sent in First Frame. Assumed that canfd frame is 64 byte long. if not then this code will have to be adjusted
    else:
        pci_H = 0x10 | ((nsdu_length & 0xF00) >> 8)
        pci_L = (nsdu_length & 0xFF)
        pci = [pci_H, pci_L]
        nsdu_FFchunk = n_sdu[:62]    #First 62 bytes are sent in First Frame. Assumed that canfd frame is 64 byte long. if not then this code will have to be adjusted

    databytes = pci + nsdu_FFchunk
    if(conf.id_type == "EXTENDED"):
        can_msg = can.Message(arbitration_id=conf.diag_req_msgid, data=databytes, is_extended_id=True, is_fd=True)
    else:
        can_msg = can.Message(arbitration_id=conf.diag_req_msgid, data=databytes, is_extended_id=False, is_fd=True)
    
    conf.tx.send(can_msg)
    # Record the time before sending
    send_time = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f')
    gen.logcantraffic("TX", send_time, conf.diag_req_msgid, len(databytes), databytes)

    gen.tp_log("First Frame Sent", can_msg)
    print(f"The First frame sent : {can_msg}")

    return 


#Function to Send Consecutive frame
def send_consecutiveframe(sequence_number, data_chunk, cf_gap_time_min):
    pci = 0x20 | (sequence_number & 0x0F)
    databytes = [pci] + data_chunk

    if(conf.id_type == "EXTENDED"):
        can_msg = can.Message(arbitration_id=conf.diag_req_msgid, data=databytes, is_extended_id=True, is_fd=True)
    else:
        can_msg = can.Message(arbitration_id=conf.diag_req_msgid, data=databytes, is_extended_id=False, is_fd=True)
    
    conf.tx.send(can_msg)
    # Record the time before sending
    send_time = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f')
    gen.logcantraffic("TX", send_time, conf.diag_req_msgid, len(databytes), databytes)

    time.sleep(cf_gap_time_min)
    gen.tp_log(f"Consecutive Frame - {sequence_number} Sent", can_msg)
    print(f"The Consecutive Frame - {sequence_number} sent : {can_msg}")

    return True


#Function to process Flow Control Frame
def process_flowcontrolframe(msg):
    #Check if this is flow control frame or not
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
    #Can be sent using single frame
    #Compute Single frame PCI
    datalength = len(n_sdu)
    if (datalength < 8):
        pci = 0x00 | (datalength & 0x0F)

        databytes = [pci] + n_sdu
    else:
        databytes = [0x00, datalength] + n_sdu

    if(conf.id_type == "EXTENDED"):
        can_msg = can.Message(arbitration_id=0x18DA6CF2, data=databytes, is_extended_id=True, is_fd=True)
    else:
        can_msg = can.Message(arbitration_id=conf.diag_req_msgid, data=databytes, is_extended_id=False, is_fd=True)
    
    conf.tx.send(can_msg)
    # Record the time before sending
    send_time = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f')
    gen.logcantraffic("TX", send_time, conf.diag_req_msgid, len(databytes), databytes)

    gen.tp_log("Single Frame Sent", can_msg)
    print(f"The single frame sent : {can_msg}")
    print(f'The can id is {conf.diag_req_msgid}')

    return True
        


#Function to send big chunk (data > 62 bytes)
def send_big_data(n_sdu):  #For big data more than 7 bytes up to 4095 bytes as specified by ISO15765 protocol
    datalength = len(n_sdu)
    if (datalength < 4095):
        #First we need to send the First Frame
        send_firstframe(n_sdu)
        pending_datalength = datalength - 62 #62 bytes of N_SDU is sent in first frame
        pending_data = n_sdu[61:]
    else:
        #First we need to send the First Frame
        send_firstframe(n_sdu)
        pending_datalength = datalength - 58 #58 bytes of N_SDU is sent in first frame
        pending_data = n_sdu[57:]


    #Let Us wait for Flow control frame and process it.
    wait4FCFrame = True
    total_cf_count = 1
    block_count = 1
    while(wait4FCFrame == True):
        received_message = receive_specific_can_message(target_id=conf.diag_resp_msgid, timeout=conf.flowcontrolframe_maxwaittime)

        if received_message:    #If a Message is recieved from ECU side with Diag Response CAN ID within the timeout period
            # Check if the message recieved is Flow control frame
            flowParameters = process_flowcontrolframe(received_message)
            if(flowParameters != None):
                #Here proper FLow control frame is recieved. So Get the flow parameters and proceed
                flow_status = flowParameters[0]
                if (flow_status == 0):   #Continue To Send Consecutive frames
                    block_size = flowParameters[1]
                    st_min = flowParameters[2]
                    if (st_min == 0):
                        cf_gap_time_min = 1/1000
                    elif (st_min in range(1,128)):
                        cf_gap_time_min = st_min/1000
                    elif(st_min in range(0xF1,0xFA)):
                        cf_gap_time_min = 1/1000
                    else:
                        cf_gap_time_min = 1/1000
                        print(f"The stmin value = {st_min} in Flow control is invalid. Default 1ms is taken for flow control purpose")
                    
                    # If it reaches here then proper flow control frame with Flow status as CTS is recieved. 
                    # Now Consecutive frame needs to be sent as per flow control parameters
                    cf_count = 1
                    if (block_size == 0):
                        #Then all the consecuitive frames can be sent till all data is transfered
                        block_size = 4096//7 + 1
                    while((pending_datalength > 0) and (cf_count <= block_size)):    #Either databytes are over or block size is crossed till then do this
                        seq_num = cf_count % 16
                        current_chunk = pending_data[:63]    #The data chunk which will be sent in the current consecutive frame
                        send_consecutiveframe(seq_num,current_chunk,cf_gap_time_min)    #Send the consecutive frame
                        pending_data = pending_data[63:] #Pending N_SDU Data to be transmitted
                        cf_count = cf_count + 1
                        total_cf_count = total_cf_count + 1
                        pending_datalength = pending_datalength - 63 #63 bytes sent in one consecutive frame max.

                    if(len(pending_data) == 0):     #All the data is sent. So nothing pending.
                        wait4FCFrame = False
                        print(f"A full N-SDU of {len(n_sdu)}bytes is sent fully with a First frame and {total_cf_count} consecutive frames.")
                        return True
                    elif(cf_count >  block_size):   #Previous block is sent. Now wait for one more FC Frame
                        wait4FCFrame = True 
                        print(f"N-SDU of {len(n_sdu)}bytes is sent partially in block num {block_count} with a First frame and {cf_count} consecutive frames.")
                        block_count = block_count + 1
                    else:
                        print("The flow should not reach here. SEVERITY POINT A")

                elif(flow_status == 1): #Wait for Next FLow Control frame
                    print ("Flow Control frame with Flow status as WAIT is recieved.")
                    gen.tp_log("Flow control frame with Flow Status = WAIT Recieved", received_message)
                    wait4FCFrame = True
                elif(flow_status == 2): #OverFLow So FLow has to be Aborted
                    print ("Flow Control frame with Flow status as OverFlow is recieved. FLOW is TERMINATED")
                    gen.tp_log("Flow control frame with Flow Status = OVERFLOW Recieved. FLOW is TERMINATED", received_message)
                    return False
                else:
                    print(f"Flow Control frame with invalid flow status [{flow_status}]is recieved. FLOW is TERMINATED")
                    gen.tp_log(f"Flow control frame with invalid Flow Status = {flow_status} Recieved. FLOW is TERMINATED", received_message)
                    return False
                
            else:
                gen.tp_log("Non Flow control message recieved over Diag Resp ID when Flow control frame is expected - FLOW is TERMINATED", received_message)
                return False
            
        else:
            print("No message received within the timeout period.")
            gen.tp_log(f"No Flow control message recieved before timeout {conf.flowcontrolframe_maxwaittime} -FLOW is TERMINATED ", received_message)
            return False
    
    return True

def send_data(n_sdu):
    length = len(n_sdu)
    if(length < 63):
        return(send_small_data(n_sdu))
    elif(length < ((2**31) -1)):
        return(send_big_data(n_sdu))
    else:
        print(f"The N-SDU length is {length}bytes which is more than 4095 bytes limit as per ISO15765 protocol. So Data Sending is not possible")
        return False
    
###############################################################################################################
##                             SECTION TO RECIEVE DATA                                                       ##
###############################################################################################################

#Function to send FLow Control Frame
def send_flowcontrolframe(flow_status, block_size, st_min):
    byte1 = 0x30 | (flow_status & 0xF)
    byte2 = block_size
    byte3 = st_min
    databytes = [byte1, byte2, byte3]

    if(conf.id_type == "EXTENDED"):
        can_msg = can.Message(arbitration_id=conf.diag_req_msgid, data=databytes, is_extended_id=True, is_fd=True)
    else:
        can_msg = can.Message(arbitration_id=conf.diag_req_msgid, data=databytes, is_extended_id=False, is_fd=True)
    
    conf.tx.send(can_msg)
    # Record the time before sending
    send_time = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f')
    gen.logcantraffic("TX", send_time, conf.diag_req_msgid, len(databytes), databytes)

    

    gen.tp_log("FLow Control Frame Sent", can_msg)
    print(f"The FLow Control frame sent : {can_msg}")

    return True


def recieve_data():
    n_sdu_rx = []

    #Initial message recieved from ECU
    received_message = receive_specific_can_message(target_id=conf.diag_resp_msgid)

    if received_message:    #If a Message is recieved from ECU side with Diag Response CAN ID within the timeout period
        #Check if recieved frame is FF or SF
        data = received_message.data
        frametype = data[0] & 0xF0
        
        if(frametype == 0x00):  #Single frame recieved
            datalength = data[0] & 0xF
            if((datalength) == 0x00): 
                n_sdu_rx.extend(data[2:])   #If lower nibble of byte0 is 0 then DL is more than 8 and so next byte contains the length
                datalength = data[1]
            else:
                n_sdu_rx.extend(data[1:])
            print(f'Single Frame Recieved of length {datalength}. N_SDU = [{" ".join(hex(number) for number in n_sdu_rx)}]')
            canmsg = f'RX\tID:{conf.diag_resp_msgid}\tdatalength:{datalength}bytes\t data:[{" ".join(hex(number) for number in n_sdu_rx)}].'
            gen.tp_log("Single Frame Recieved", canmsg)
            return(n_sdu_rx)
        
        elif(frametype == 0x10):  #First frame recieved
            n_sdu_length = (((data[0] & 0xF)<<8) | (data[1]))
            if(n_sdu_length == 00): #For data > 4095 bytes the format changes. 
                n_sdu_rx.extend(data[6:])
                n_sdu_length = ((data[2]<<24) | (data[3]<<16) | (data[4]<<8) | (data[5]))
                pendingbyteslength = n_sdu_length - len(data[6:])
            else:
                n_sdu_rx.extend(data[2:])
                pendingbyteslength = n_sdu_length - len(data[2:])
            print(f"First Frame Recieved. Total NSDU Length = {n_sdu_length}bytes. Data Chunk = [{' '.join(hex(number) for number in n_sdu_rx)}]")
            canmsg = f'RX\tID:{conf.diag_resp_msgid}\tnsdulength:{n_sdu_length}bytes\t data:[{" ".join(hex(number) for number in n_sdu_rx)}].'
            gen.tp_log("First Frame Recieved", canmsg)

        else:
            print(f"Expected SF or FF but Invalid Frame recieved in the flow with frame type = {frametype} and the whole data = [{' '.join(hex(number) for number in data)}]")
            return False
    
    else:
        print("No message received within the timeout period.")
        gen.tp_log(f"No Frame recieved before timeout {2}s -FLOW is TERMINATED ", received_message)
        return False
    #First Frame is recieved and now Flow control frame has to be sent and  consecutive frame has to be recieved
    #Lets send FLow Control frame
    send_flowcontrolframe(0, 0, 50) #Send all the consecutive frames with minimum 50 ms gap
    oldseqnum = 0
    #Lets process the Consecutive frames
    while(pendingbyteslength > 0):  #We process consecutive frames till no bytes pending to be recieved.
        received_message = receive_specific_can_message(target_id=conf.diag_resp_msgid)

        if received_message:    #If a Message is recieved from ECU side with Diag Response CAN ID within the timeout period
            #Check if recieved frame is CF
            data = received_message.data
            frametype = data[0] & 0xF0
            if(frametype == 0x20):  # Consecutive frame recieved
                seqnum = data[0] & 0x0F
                # Check sequence number order
                expected_seqnum = (oldseqnum + 1) % 16
                if (seqnum != expected_seqnum):
                    print(f"Sequence broken. Expected sequence num {expected_seqnum} but recieved sequence num {seqnum}. - FLOW TERMINATED")
                    canmsg = f'RX\tID:{conf.diag_resp_msgid}\tdata:[{" ".join(hex(number) for number in n_sdu_rx)}].'
                    gen.tp_log(f"Consecutive Frame - {seqnum} Recieved but expected seq num is {expected_seqnum}", canmsg)
                    return False
                #Update the N_SDU Buffer with consecutive frame data
                n_sdu_rx.extend(data[1:])
                print(f"Consecutive Frame Recieved. SeqNum:{seqnum} | Data Chunk = [{' '.join(hex(number) for number in data[1:])}]")
                canmsg = f'RX\tID:{conf.diag_resp_msgid}\tDatalength:{len(data)}\tdata:[{" ".join(hex(number) for number in n_sdu_rx)}].'
                gen.tp_log(f"Consecutive Frame - {seqnum} Recieved", canmsg)
                pendingbyteslength = pendingbyteslength - len(data[1:])

            else:
                print(f"Expected CF but Invalid Frame recieved in the flow with frame type = {frametype} and the whole data = [{' '.join(hex(number) for number in data)}]")
                gen.tp_log(f"Expected CF but Invalid Frame recieved in the flow with frame type = {frametype} and the whole data = ", f"[{' '.join(hex(number) for number in data)}]")
                #Update the N_SDU buffer with consecutive frame data
                n_sdu_rx.extend(data[1:])
                # Update sequence number tracking
                oldseqnum = seqnum
                print(f"DEBUG: Updated Old SeqNum={oldseqnum}")
                # Update pending data length
                pendingbyteslength -= len(data[1:])
                return False            
        
        else:
            print("No message received within the timeout period.")
            gen.tp_log(f"No Frame recieved before timeout {5}s -FLOW is TERMINATED ", received_message)
            return False
        
    #The complete N_SDU would be recieved by now. Let us Return complete N_SDU
    print(f"The complete N_SDU is recieved.")
    return(n_sdu_rx)


###############################################################################################################
##                                          SECTION END                                                      ##
###############################################################################################################








