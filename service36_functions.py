from environment import *

if RUNNING_ON_RASPBERRYPI == False:
    import uds_dummy as uds     #will have to be replaced with actual uds file while testing on board
else:
    import uds
    import can 
from service34_base import Ui_Form_SID34
import service34_main as main34
from service34_main import Ui_Form_SID34
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox,QFileDialog
import service34_functions as fun
from bs4 import BeautifulSoup
import os
import datetime
import general as gen
#import uds_dummy as uds     #will have to be replaced with actual uds file while testing on board
import configure as conf
import os

def first_data_transfer(ex_data, blocksize_hex_values, blocks, decimal_blocksize):
    blocksize_decimal_values = [int(hex_str, 16) for hex_str in blocksize_hex_values]  
    sid=int("36",16)
    block_no=int("01",16)
    edata_list = ex_data.split()
    edata_decimal_values = [int(hex_str, 16) for hex_str in edata_list]
    first_e_data=edata_decimal_values[0:60]
    first_req_bytes = blocksize_decimal_values + [sid] + [block_no] + first_e_data
    print(f"{' '.join(map(str, blocksize_decimal_values))} {sid} {block_no} {' '.join(map(str, first_e_data))} ")
    print("FIRST_REQ",first_req_bytes)
    return first_req_bytes

            

         
        
def consecutive_data_transfer(e_data,blocksize,no_of_blocks,decimal_blocksize):
    first=60
    last=123
    blocksize_decimal_values = [int(hex_str, 16) for hex_str in blocksize]  
    remaining_blocksize=decimal_blocksize-60
    consecutive_frame_number=32
    consecutive_frame_number_hex=hex(consecutive_frame_number)
    edata_list = e_data.split()
    edata_decimal_values = [int(hex_str, 16) for hex_str in edata_list]
    cons_e_data=edata_decimal_values[first:last]
    cons_req_bytes = [consecutive_frame_number] + cons_e_data
    print(cons_req_bytes)
    first+=63
    last+=63
    if consecutive_frame_number==47:
        consecutive_frame_number=32
    else:
        consecutive_frame_number+=1


if __name__ == "__main__":
     print(first_data_transfer("00","44","00 50 00 00","00 17 ff e0"))