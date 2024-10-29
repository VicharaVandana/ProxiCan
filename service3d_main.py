from environment import *

if RUNNING_ON_RASPBERRYPI == False:
    import uds_dummy as uds  # Replace with actual uds file while testing on board
else:
    import uds
    import can

from service3d_base import Ui_Form_SID3D
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import service3d_functions as fun
from bs4 import BeautifulSoup
import os
import datetime
import general as gen
import configure as conf
import uds_dummy as uds  # Replace with actual uds file while testing on board
import os


class Ui_Service3D(Ui_Form_SID3D):
    def redesign_ui(self):
        pass

    def connectFunctions(self):
        self.pushButton_Send3DReq.clicked.connect(self.send3dservice)
        self.pushButton_reset.clicked.connect(self.clearform)
        self.pushButton_appendLog.clicked.connect(self.addlog)
        self.pushButton_clearLog.clicked.connect(self.clearlog)
        return

    def update_status(self, msg):
        # Update the status label
        self.label_status.setText(msg)
        return

    def clearform(self):
        # Clears all the fields for entering new service request
        self.logentrystring = ""
        self.label_ResType_2.setText("No Response")
        self.textBrowser_Resp.clear()
        self.update_status("User form cleared successfully")
        gen.log_action("Button Click", "Clear Form for Service 3d window clicked. User fields cleared successfully.")
        return

    def addlog(self):
        # Add the uds transaction to the log file
        gen.log_udsreport(self.logentrystring)
        self.logentrystring = ""  # Clear the log entry so that only one entry is made
        self.update_status(f"Log file appended with the current UDS transaction (./reports/uds_log_report.txt)")
        gen.log_action("Button Click", "Add to Log button for Service 3d window clicked.")
        return

    def clearlog(self):
        gen.clearudslogfile()
        self.update_status(f"Log file cleared (./reports/uds_log_report.txt)")
        gen.log_action("Button Click", "Clear Log button for Service 3d window clicked.")
        return

    def send3dservice(self):
        alfid = self.lineEdit_ALFID.text().strip().replace(" ","").replace(" ","").replace(" ","")




        if not gen.check_1Bytehexadecimal(alfid):
            self.update_status("Invalid ALFID. Please enter a valid hexadecimal value of 1 byte.")
            gen.log_action("UDS Request Fail", "23 Request failed due to invalid ALFID byte.")
            return        
        
        if not gen.check_hexadecimal(alfid):
            self.update_status("Invalid ALFID. Please enter a valid hexadecimal value of 1 byte.")
            gen.log_action("UDS Request Fail", "23 Request failed due to invalid ALFID byte.")
            return 
        
        alfid_mem_size=int(alfid[0],16)
        alfid_mem_add=int(alfid[1],16)
        mem_add = self.lineEdit_Mem_address.text().strip().replace(" ","").replace(" ","").replace(" ","")
        mem_size = self.lineEdit_Mem_size.text().strip().replace(" ","").replace(" ","").replace(" ","")
        # Validate memory address and size
        if not gen.check_hexadecimal(mem_add):
            self.update_status("Invalid memory address. Please enter a valid hexadecimal value.")
            gen.log_action("UDS Request Fail", "3d Request failed due to invalid memory address.")
            return

        if len(mem_add) % 2 != 0:
            self.update_status("The length of the Memory address must be even since its in bytes formart.")
            gen.log_action("UDS Request Fail", "3d Request failed due to invalid memory address.")
            return
        
        if(alfid_mem_add!=len(mem_add)//2):
            self.update_status("The Memory address size must match with ALFID byte.")
            gen.log_action("UDS Request Fail", "3d Request failed due to invalid memory address size.")
            return
        
        if not gen.check_hexadecimal(mem_size):
            self.update_status("Invalid memory size. Please enter a valid hexadecimal value.")
            gen.log_action("UDS Request Fail", "3d Request failed due to invalid memory size.")
            return

        if len(mem_size) % 2 != 0:
            self.update_status("The length of the Memory size must be even since its in bytes formart.")
            gen.log_action("UDS Request Fail", "3d Request failed due to invalid memory size.")
            return

        if(alfid_mem_size!=len(mem_size)//2):
            self.update_status("The Memory address size must match with ALFID byte.")
            gen.log_action("UDS Request Fail", "3d Request failed due to invalid memory address size.")
            return    
        data_record = self.lineEdit_DataRec.text().strip().replace(" ","").replace(" ","").replace(" ","")

        if not gen.check_hexadecimal(data_record):
            self.update_status("Invalid Data Record. Please enter a valid hexadecimal value.")
            gen.log_action("UDS Request Fail", "3d Request failed due to invalid memory size.")
            return
        
        if len(data_record) % 2 != 0:
            self.update_status("The length of the Data Record must be even since its in bytes formart.")
            gen.log_action("UDS Request Fail", "3d Request failed due to invalid Data Record.")
            return

        self.update_status("Memory address, size and data record is validated.")
        
        # Send the service request
        service_request = fun.form_reqmsg4srv3d(alfid,mem_add, mem_size,data_record)
        #IsPosResExpected = not self.checkBox_suppressposmsg.isChecked()

        response = uds.sendRequest(service_request)
        
        self.update_status("Service 3d request is sent")
        gen.log_action("UDS Request Success", f"3d Request Successfully sent : {' '.join(hex(number) for number in service_request)}")

        # Process the response
        if response.type == "Positive Response":
            response_html = f'''
            <h4><U>Positive Response Received</U></h4>
            <p><strong>Service ID:</strong> <I>{hex(response.resp[0]-0x40)}</I></p>
            <p><strong>Memory Address:</strong> <I>{mem_add}</I></p>
            <p><strong>Memory Size:</strong> <I>{mem_size}</I></p>
            <p><strong>Data Record:</strong> <I>{data_record}</I></p>
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
        self.textBrowser_Resp.setHtml(response_html)

        current_user = os.getlogin()
        currenttime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        soup = BeautifulSoup(response_html, 'html.parser')
        response_text = soup.get_text()

        self.logentrystring = f'''<---- LOG ENTRY [{current_user} - {currenttime}] ---->
        UDS Request :   [{" ".join(hex(number) for number in service_request)}]
        Explanation:    Write Memory By Address request for memory address {mem_add} and size {mem_size} with Data Record of {data_record}
        UDS Response:   [{" ".join(hex(number) for number in response.resp)}]
        Explanation:    {response_text}<------------------- LOG ENTRY END ------------------->

        '''
        return


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form_SID_3D = QtWidgets.QWidget()
    ui = Ui_Service3D()
    ui.setupUi(Form_SID_3D)
    ui.redesign_ui()
    ui.connectFunctions()

    Form_SID_3D.show()
    sys.exit(app.exec_())