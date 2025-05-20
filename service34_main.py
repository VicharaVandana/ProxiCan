from environment import *

if RUNNING_ON_RASPBERRYPI == False:
    import uds_dummy as uds     #will have to be replaced with actual uds file while testing on board
else:
    import uds
    import can
from service36_base import Ui_Ui_form_sid36
from intelhex import IntelHex 
from service34_base import Ui_Form_SID34
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
import service36_functions as DT
import service36_main as main36
import data_trans_variable as DTV



class Ui_Service34(Ui_Form_SID34):
    def redesign_ui(self):
        pass    
        
    def connectFunctions(self):
        self.pushButton_Send34Req_2.clicked.connect(self.send34service)
        self.pushButton_reset_2.clicked.connect(self.clearform)
        self.pushButton_appendLog_2.clicked.connect(self.addlog)
        self.pushButton_clearLog_2.clicked.connect(self.clearlog)
        self.pushButton_Browse.clicked.connect(self.browse_file)
        self.pushButton_ExtractData.clicked.connect(self.extract_data)
        

        return
    
    def update_status(self, msg):
        # Create a QMessageBox instance
        self.label_status.setText(msg)
        return
    
    def clearform(self):
        #Clears all the fields for entering new service request
        self.logentrystring = ""
        self.label_ResType_2.setText("No Response")
        self.textBrowser_Resp_2.clear()

        self.update_status("Userform cleared successfully")
        gen.log_action("Button Click", "Clear Form for Service 28 window clicked. Userfields cleared successfully.")
        return
    
    def addlog(self):
        #Add the uds transaction to the log file
        gen.log_udsreport(self.logentrystring)
        self.logentrystring = ""    #Clear the log entry so that if multiple tiomes the button is clicked continuously only one entry is made.
        self.update_status(f"Log file appended with the current UDS transaction (./reports/uds_log_report.txt)")
        gen.log_action("Button Click", "Add to Log button for Service 34 window clicked.")
        return
    
    def clearlog(self):
        gen.clearudslogfile()
        self.update_status(f"Log file cleared (./reports/uds_log_report.txt)")
        gen.log_action("Button Click", "Clear Log button for Service 34 window clicked.")
        return
    
    def browse_file(self):
        # Open file dialog to browse files
        file_path, _ = QFileDialog.getOpenFileName(Form_SID34, "Select File", "", "Hex Files (*.hex);;All Files (*)")

  # Customize filter as needed
        if file_path:
            self.filepath=file_path
            self.lineEdit_Mem_address_2.setText(file_path)
            self.update_status(f"File selected: {file_path}")
            gen.log_action("File Browsed", f"User browsed the file: {file_path}")
        else:
            self.update_status("No file selected.")
            self.filepath=None
        return 
    
    def extract_data(self, start_address=None, size=None):
        # Get memory size and address from line edits
        mem_size = self.lineEdit_Mem_size.text().strip().replace(" ", "")
        mem_add = self.lineEdit_Mem_address.text().strip().replace(" ", "")
        
        mem_size_int = int(mem_size, 16)
        mem_add_int = int(mem_add, 16)

        # Use integers for computation
        start_address = mem_add_int
        size = mem_size_int

        file_path = self.filepath
        e_data = []
        if file_path:
            address_data_map = {}  # Dictionary to store address-to-data mapping

            try:
                with open(file_path, 'r') as hex_file:
                    for line in hex_file:
                        if not line.startswith(':'):
                            continue

                        # Extract the length, address, and data portion
                        length = int(line[1:3], 16)
                        address = int(line[3:7], 16)
                        data = line[9:9 + length * 2]

                        # Map each byte of data to its corresponding address
                        for i in range(length):
                            byte_address = address + i
                            byte_data = data[i * 2:(i * 2) + 2]
                            address_data_map[byte_address] = byte_data

                    # If start_address and size are provided, extract mapped data
                    if start_address is not None and size is not None:
                        extracted_data = [
                            address_data_map.get(addr, "00")  # Default to "00" if address is missing
                            for addr in range(start_address, start_address + size)
                        ]
                        # Print the extracted data in the terminal
                        print(f"Data from address 0x{start_address:04X} for size {size}:")
                        e_data = " ".join(extracted_data)
                        DTV.ex_data=e_data

                    else:
                        # Print all address-to-data mappings for debugging
                        print("Full Address-to-Data Map:")
                        for addr, data in address_data_map.items():
                            print(f"0x{addr:04X}: {data}")

                    self.textEdit.setText(e_data)

            except Exception as e:
                print(f"Error processing the file: {e}")
        else:
            print("No file was selected.")



    
    def send34service(self):
                #define the alfid based on your requirement
        dfi="00"
        alfid="22"            
        # alfid = self.lineEdit_ALFID.text().strip().replace(" ","").replace(" ","").replace(" ","")




        # if not gen.check_1Bytehexadecimal(alfid):
        #     self.update_status("Invalid ALFID. Please enter a valid hexadecimal value of 1 byte.")
        #     gen.log_action("UDS Request Fail", "23 Request failed due to invalid ALFID byte.")
        #     return        
        
        # if not gen.check_hexadecimal(alfid):
        #     self.update_status("Invalid ALFID. Please enter a valid hexadecimal value of 1 byte.")
        #     gen.log_action("UDS Request Fail", "23 Request failed due to invalid ALFID byte.")
        #     return 
        
        alfid_mem_size=int(alfid[0],16)
        alfid_mem_add=int(alfid[1],16)
        mem_add = self.lineEdit_Mem_address.text().strip().replace(" ","").replace(" ","").replace(" ","")
        mem_size = self.lineEdit_Mem_size.text().strip().replace(" ","").replace(" ","").replace(" ","")
        # Validate memory address and size
        if not gen.check_hexadecimal(mem_add):
            self.update_status("Invalid memory address. Please enter a valid hexadecimal value.")
            gen.log_action("UDS Request Fail", "23 Request failed due to invalid memory address.")
            return

        if len(mem_add) % 2 != 0:
            self.update_status("The length of Memory address must be even since its in bytes formart.")
            gen.log_action("UDS Request Fail", "23 Request failed due to invalid memory address.")
            return
        
        if(alfid_mem_add!=len(mem_add)//2):
            self.update_status(f"The Memory address size must match with ALFID byte of {alfid_mem_add}.")
            gen.log_action("UDS Request Fail", "23 Request failed due to invalid memory address size.")
            return
        
        if not gen.check_hexadecimal(mem_size):
            self.update_status("Invalid memory size. Please enter a valid hexadecimal value.")
            gen.log_action("UDS Request Fail", "23 Request failed due to invalid memory size.")
            return

        if len(mem_size) % 2 != 0:
            self.update_status("The length of Memory size must be even since its in bytes formart.")
            gen.log_action("UDS Request Fail", "23 Request failed due to invalid memory size.")
            return

        if(alfid_mem_size!=len(mem_size)//2):
            self.update_status(f"The Memory size must match with ALFID byte of {alfid_mem_size}.")
            gen.log_action("UDS Request Fail", "23 Request failed due to invalid memory address size.")
            return    
        
        self.update_status("Memory address and size validated.")
        
        # Send the service request
        service_request = fun.form_reqmsg4srv34(dfi,alfid,mem_add, mem_size)


        response = uds.sendRequest(service_request)
        
        self.update_status("Service 34 request is sent")
        gen.log_action("UDS Request Success", f"34 Request Successfully sent : {' '.join(hex(number) for number in service_request)}")

        # Process the response
        if response.type == "Positive Response":
            blocksize = response.resp[2:]  # Example input
            memsize=int(mem_size,16)
            print(memsize)

        # Step 1: Convert each element to a 2-character hex string
            hex_blocksize = ''.join(f'{byte:02x}' for byte in blocksize)
        # Step 2: Convert the concatenated hex string to a decimal integer
            DTV.decimal_blocksize = int(hex_blocksize, 16)
            DTV.blocks=(memsize//DTV.decimal_blocksize)+1

            DTV.blocksize_hex_values = [f"{value:02x}" for value in blocksize]
    
    # Modify the first hexadecimal value by adding 1
            if DTV.blocksize_hex_values:
                first_value = int(DTV.blocksize_hex_values[0], 16) +16
                DTV.blocksize_hex_values[0] = f"{first_value:02x}"
                print(DTV.blocksize_hex_values)
    #Data transfer part using service 36

            d = main36.Ui_Service36.send36service(DTV.ex_data,DTV.blocksize_hex_values,DTV.blocks,DTV.decimal_blocksize)


         

            #data_transfer = data_transfer()
            response_html = f'''
            <h4><U>Positive Response Received</U></h4>
            <p><strong>Service ID:</strong> <I>{hex(response.resp[0]-0x40)}</I></p>
            <p><strong>Memory Address:</strong> <I>{mem_add}</I></p>
            <p><strong>Memory Size:</strong> <I>{mem_size}</I></p>
            <p><strong>Info:</strong> <I> Service 34 response successfully received with Block size {DTV.decimal_blocksize}</I></p>
            <p><strong>Info:</strong> <I> Number of blocks required {DTV.blocks}</I></p>
            '''
        elif response.type == "Negative Response":
            response_html = f'''
            <h4><U>Negative Response Received</U></h4>
            <p><strong>NRC Code:</strong> <I>{hex(response.nrc)}</I></p>
            <p><strong>NRC Name:</strong> <I>{response.nrcname}</I></p>
            <p><strong>NRC Description:</strong> <I>{response.nrcdesc}</I></p>
            '''
        elif response.type == "Unknown Response Type":
            response_html = f'''
            <h4><U>Unidentified Response Received</U></h4>
            <p><strong>Response Bytes:</strong> <I>{" ".join(hex(number) for number in response.resp)}</I></p>
            '''
        elif response.type == "No Response":
            response_html = f'''
            <h4><U>No Response Received</U></h4>
            <p><strong>Response Bytes:</strong> <I>{" ".join(hex(number) for number in response.resp)}</I></p>
            '''
        else:
            response_html = f'''<h4><U>ERROR OCCURRED</U></h4>'''

        # Update the response data on the user form
        self.label_ResType_2.setText(response.type)
        self.textBrowser_Resp_2.setHtml(response_html)

        current_user = os.getlogin()
        currenttime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        soup = BeautifulSoup(response_html, 'html.parser')
        response_text = soup.get_text()

        self.logentrystring = f'''<---- LOG ENTRY [{current_user} - {currenttime}] ---->
        UDS Request :   [{" ".join(hex(number) for number in service_request)}]
        Explanation:    Request Download Service for memory address {mem_add} and size {mem_size}
        UDS Response:   [{" ".join(hex(number) for number in response.resp)}]
        Explanation:    {response_text}<------------------- LOG ENTRY END ------------------->

        '''
        return 




if __name__ == "__main__":
    import sys
    #current_user = os.getlogin()
    #currenttime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #print(f"<---- LOG ENTRY [{current_user} - {currenttime}] ---->")
    app = QtWidgets.QApplication(sys.argv)
    Form_SID34 = QtWidgets.QWidget()
    ui = Ui_Service34()
    ui.setupUi(Form_SID34)
    ui.redesign_ui()
    ui.connectFunctions()
    
    #Initializing the CAN
    #os.system(f'sudo ip link set {conf.can_channel} up type can bitrate {conf.baudrate} dbitrate {conf.datarate} restart-ms 1000 berr-reporting on fd on')

    #conf.tx = can.interface.Bus(channel=conf.can_channel, bustype='socketcan', fd=True)
    #conf.rx = can.interface.Bus(channel=conf.can_channel, bustype='socketcan', fd=True)

    Form_SID34.show()
    sys.exit(app.exec_())