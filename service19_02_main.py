from environment import *

if RUNNING_ON_RASPBERRYPI == False:
    import uds_dummy as uds     #will have to be replaced with actual uds file while testing on board
else:
    import uds
    import can
    
from service19_02_base import Ui_Form_SID_19_02
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import service19_functions as fun
from bs4 import BeautifulSoup
import os
import datetime
import general as gen
#import uds_dummy as uds     #will have to be replaced with actual uds file while testing on board
import configure as conf
import os


class Ui_Service19_02(Ui_Form_SID_19_02):
    def redesign_ui(self):
        pass

    def connectFunctions(self):
        self.pushButton_Send19_02Req.clicked.connect(self.send19_02service)
        self.pushButton_reset.clicked.connect(self.clearform)
        self.pushButton_appendLog.clicked.connect(self.addlog)
        self.pushButton_clearLog.clicked.connect(self.clearlog)
        return
    
    def update_status(self, msg):
        # Create a QMessageBox instance
        self.label_status.setText(msg)
        return
    
    def clearform(self):
        #Clears all the fields for entering new service request
        self.logentrystring = ""
        self.label_ResType.setText("No Response")
        self.textBrowser_Resp.clear()
        self.lineEdit_DTCStatusMask.clear()
        checkboxes = [self.checkBox_statusMask_bit0, self.checkBox_statusMask_bit1,
                      self.checkBox_statusMask_bit2, self.checkBox_statusMask_bit3,
                      self.checkBox_statusMask_bit4, self.checkBox_statusMask_bit5,
                      self.checkBox_statusMask_bit6, self.checkBox_statusMask_bit7
        ]
        for checkbox in checkboxes:
            checkbox.setChecked(False)
        self.comboBox_DTCStatusMask_entryType.currentIndexChanged.connect(self.reset_fields_on_entry_type_change)
        self.update_status("Userform cleared successfully")
        gen.log_action("Button Click", "Clear Form for Service 19 subfunction 02 window clicked. Userfields cleared successfully.")
        return
    
    def reset_fields_on_entry_type_change(self, index):    #Handles actions when the entry type in the combo box changes. Clears specific fields based on the selected index.
            self.textBrowser_Resp.clear()                  # Clear the response text browser when the combo box index change
            if index == 1:
                self.lineEdit_DTCStatusMask.clear()        # Clear the line edit field if index is 1
            else:                                          # Call the clearform method for resetting all fields
                self.clearform()
    
    def addlog(self):
        #Add the uds transaction to the log file
        gen.log_udsreport(self.logentrystring)
        self.logentrystring = ""    #Clear the log entry so that if multiple tiomes the button is clicked continuously only one entry is made.
        self.update_status(f"Log file appended with the current UDS transaction (./reports/uds_log_report.txt)")
        gen.log_action("Button Click", "Add to Log button for Service 19 subfunction 02 window clicked.")
        return
    
    def clearlog(self):
        gen.clearudslogfile()
        self.update_status(f"Log file cleared (./reports/uds_log_report.txt)")
        gen.log_action("Button Click", "Clear Log button for Service 19 subfunction 02 window clicked.")
        return
    
    def send19_02service(self):
        sprmib_flg = self.checkBox_suppressposmsg.isChecked()

        if self.comboBox_DTCStatusMask_entryType.currentIndex() == 1: # Option 2 selected
            status_mask = self.lineEdit_DTCStatusMask.text().strip().replace(" ", "")
            formatted_status_mask = f"0x{status_mask}"
            if(False == gen.check_1Bytehexadecimal(status_mask)):
            #Show messagebox with enter valid DTC status mask value
                self.update_status("Please enter a valid DTC Status Mask. It must be 1 byte in hexadecimal format")
                gen.log_action("UDS Request Fail", "19 02 Request not sent due to invalid DTC Status Mask")
                return 
            self.update_status("DTC Status Mask is validated.")
            service_request = fun.form_reqmsg4srv19_subfun_2_manual(status_mask,sprmib_flg)
            gen.log_action("Button Click", f"Send 19 02 request button clicked with DTC Status Mask {formatted_status_mask} .")
        else:
            status_mask= fun.calculate_dtc_status_mask(self.checkBox_statusMask_bit0, self.checkBox_statusMask_bit1,
                                                   self.checkBox_statusMask_bit2, self.checkBox_statusMask_bit3,
                                                   self.checkBox_statusMask_bit4, self.checkBox_statusMask_bit5,
                                                   self.checkBox_statusMask_bit6, self.checkBox_statusMask_bit7
        )
            formatted_status_mask = f"{hex(status_mask)}"
            if status_mask == 0:
                self.update_status("Please select atleast one bit in DTC status mask")
                print(f"DTC Status mask {formatted_status_mask} is invalid")
                gen.log_action("UDS Request Fail", "19 02 Request not happened due to invalid DTC Status Mask")
                return
            self.update_status("DTC Status Mask is validated.")
            service_request = fun.form_reqmsg4srv19_subfun_2(status_mask,sprmib_flg)
        
        gen.log_action("Button Click", f"Send 19 02 request button clicked with DTC Status Mask {formatted_status_mask} .")

        self.comboBox_DTCStatusMask_entryType.currentIndexChanged.connect(self.reset_fields_on_entry_type_change)

        #Send the service request and get the response 
        if(sprmib_flg == False):
            IsPosResExpected = True 
        else:
            IsPosResExpected = False 
        #print(f'The request is {" ".join(hex(number) for number in service_request)}')
        
        gen.IsAnyServiceActive = True   #Next request is triggered, so make True
        #Send the service request  
        while(gen.IsTesterPresentActive == True):
            self.update_status("WAIT!! Tester present (Service 3E) is currently ongoing")
            
        response = uds.sendRequest(service_request, True)

        gen.IsAnyServiceActive = False   #Next response recieved , so make False
        
        self.update_status("Service 19 request is sent")
        gen.log_action("UDS Request Success", f"19 Request Successfully sent : {' '.join(hex(number) for number in service_request)}")
        

        if(response.type == "Positive Response"):
            self.update_status("Service 19 subfunction 02 response is received")

            length=len(response.resp)
            response_data = fun.getDTCASR(length, response.resp)
            dtc_records_html = response_data["html"]
            dtc_records_text = response_data["text"]
            
 
            response_html = f'''<h4><U>Positive Response Recieved</U></h4>
    <p><strong>Service ID:</strong> <I>{hex(response.resp[0]-0x40)}</I></p>
    <p><strong>Subfunction Name:</strong> <I>Report DTC By Status Mask {hex(response.resp[1])} </I></p>
    <p><strong>Suppress Positive Message Request:</strong> <I>{sprmib_flg}</I></p>
    <p><strong>DTC Status Availability Mask:</strong> <I> {hex(response.resp[2])} </I></p>
    {dtc_records_html} <!-- This will display the DTC records generated in the function -->
    <p><strong>Info:</strong> <I> Service 19 sunfunction 02 is successfully executed with DTC Status Mask {formatted_status_mask}</I></p>
'''

        elif(response.type == "Negative Response"):
            response_html = f'''<h4><U>Negative Response Recieved</U></h4>
    <p><strong>Suppress Positive Message Request:</strong> <I>{sprmib_flg}</I></p>
    <p><strong>NRC Code:</strong> <I>{hex(response.nrc)}</I></p>
    <p><strong>NRC Name:</strong> <I>{response.nrcname}</I></p>
    <p><strong>NRC Desc:</strong> <I>{response.nrcdesc}</I></p>
'''
            
        elif(response.type == "Unknown Response Type"):
            response_html = f'''<h4><U>Unidentified Response Recieved</U></h4>
    <p><strong>Response Bytes:</strong> <I>{" ".join(hex(number) for number in response.resp)}</I></p>
'''
        elif(response.type == "No Response"):
            response_html = f'''<h4><U>No Response Recieved</U></h4>
            <p><strong>Suppress Positive Message Request:</strong> <I>{sprmib_flg}</I></p>
            <p><strong>Response Bytes:</strong> <I>{" ".join(hex(number) for number in response.resp)}</I></p>
'''
        else:
            response_html = f'''<h4><U>ERROR OCCURED</U></h4>'''

        
        #Update the response data on userform
        self.label_ResType.setText(response.type)
        self.textBrowser_Resp.setHtml(response_html)

        current_user = os.getlogin()
        currenttime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        soup = BeautifulSoup(response_html, 'html.parser')
        response_text = soup.get_text()

        self.logentrystring = f'''<---- LOG ENTRY [{current_user} - {currenttime}] ---->
 UDS Request :   [{" ".join(hex(number) for number in service_request)}]
 Explaination:   Read DTC Information (Service 19 subfunction 02) Requested for DTC Status Mask {formatted_status_mask} and SPRMIB flag {sprmib_flg}
 UDS Response:   [{" ".join(hex(number) for number in response.resp)}]
 '''
        # Conditional part of the log entry
        if response.type == "Positive Response":
            self.logentrystring += f'''Explanation:   Positive Response Received
Service ID: {hex(response.resp[0] - 0x40)}
Subfunction Name: Report DTC By Status Mask {hex(response.resp[1])}
Suppress Positive Message Request: {sprmib_flg}
DTC Status Availability Mask: {hex(response.resp[2])}
{dtc_records_text}
Info: Service 19 Subfunction 02 was successfully executed with DTC Status Mask {formatted_status_mask}
<------------------- LOG ENTRY END ------------------->

# '''
        else:
            self.logentrystring += f'''Explanation:   {response_text}
<------------------- LOG ENTRY END ------------------->

# '''
        return
    
    def closeEvent(self, event):
        # Custom logic when the window is closed
        gen.log_action(f"Window Close", f"Service 19 02 Window Closed.")
        return
    





if __name__ == "__main__":
    import sys
    #current_user = os.getlogin()
    #currenttime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #print(f"<---- LOG ENTRY [{current_user} - {currenttime}] ---->")
    app = QtWidgets.QApplication(sys.argv)
    Form_SID19_02 = QtWidgets.QWidget()
    ui = Ui_Service19_02()
    ui.setupUi(Form_SID19_02)
    ui.redesign_ui()
    ui.connectFunctions()
    #Initializing the CAN
    if RUNNING_ON_RASPBERRYPI == True:
        os.system(f'sudo ip link set {conf.can_channel} up type can bitrate {conf.baudrate} dbitrate {conf.datarate} restart-ms 1000 berr-reporting on fd on')
        conf.tx = can.interface.Bus(channel=conf.can_channel, bustype='socketcan', fd=True)
        conf.rx = can.interface.Bus(channel=conf.can_channel, bustype='socketcan', fd=True)

    Form_SID19_02.show()
    sys.exit(app.exec_())