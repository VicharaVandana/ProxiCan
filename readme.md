# How to configure the CAN channel and make it redy for communication

Call the function **connectCAN** with argument object **canconfig** and this parameter must contain necessary values mentioned below as its elements:
- ReqCanId  
- RespCanId 
- channel
- idtype
- bitrate
- fdftype
- brsrate
- samplepoint
- FlowCtrlTimeout

# How to Send the Data 
Invoke the function **send_data** from the file **flowcontrol_can.py** with the complete N-SDU as argument. The Argument to this function **n_sdu** is python list of numbers. Each byte is one element of this list ordered properly.

# How to Recieve the Data
Invoke the Function **recieve_data** from the file **flowcontrol_can.py** to get the full N_SDU. This function if everything goes fine would return the **n_sdu** which contains all the Recieved data as list of bytes in proper order. 

# Order in which the Functions must be invoked
1. Call *connectCAN* to configure the CAN and keep the Setup Ready
2. Call *send_data* with UDS request message data - UDS Level
3. Call *recieve_data* and the process the return value for the UDS response message data
