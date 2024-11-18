from environment import *

if RUNNING_ON_RASPBERRYPI == False:
    import uds_dummy as uds     #will have to be replaced with actual uds file while testing on board
else:
    import uds
    import can
    
from service19_01_base import Ui_Form_SID_19_01
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


class Ui_Service19_01(Ui_Form_SID_19_01):
    def redesign_ui(self):
        pass

    def connectFunctions(self):
        self.pushButton_Send19_01Req.clicked.connect(self.send19_01service)
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
        #self.lineEdit_dtc.clear()
        self.update_status("Userform cleared successfully")
        gen.log_action("Button Click", "Clear Form for Service 14 window clicked. Userfields cleared successfully.")
        return
    
    def addlog(self):
        #Add the uds transaction to the log file
        gen.log_udsreport(self.logentrystring)
        self.logentrystring = ""    #Clear the log entry so that if multiple tiomes the button is clicked continuously only one entry is made.
        self.update_status(f"Log file appended with the current UDS transaction (./reports/uds_log_report.txt)")
        gen.log_action("Button Click", "Add to Log button for Service 14 window clicked.")
        return
    
    def clearlog(self):
        gen.clearudslogfile()
        self.update_status(f"Log file cleared (./reports/uds_log_report.txt)")
        gen.log_action("Button Click", "Clear Log button for Service 2E window clicked.")
        return
    
    def send19_01service(self):
        sprmib_flg = self.checkBox_suppressposmsg.isChecked()
        status_mask= fun.calculate_dtc_status_mask(self.checkBox_statusMask_bit0,
    self.checkBox_statusMask_bit1,
    self.checkBox_statusMask_bit2,
    self.checkBox_statusMask_bit3,
    self.checkBox_statusMask_bit4,
    self.checkBox_statusMask_bit5,
    self.checkBox_statusMask_bit6,
    self.checkBox_statusMask_bit7)
        gen.log_action("Button Click", f"Send 19 01 request button clicked with DTC Status Mask[{status_mask}]].")

        service_request = fun.form_reqmsg4srv19_subfun_1(status_mask,sprmib_flg)

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
            DTCFormatIdentifierName = fun.getDTCFormatIdentifiername(hex(response.resp[3]))
            # Extract the last two bytes
            msb = response.resp[4]  # Most Significant Byte
            lsb = response.resp[5]  # Least Significant Byte # Combine them into a single 16-bit value
            combined_value = (msb << 8) | lsb
 
            response_html = f'''<h4><U>Positive Response Recieved</U></h4>
    <p><strong>Service ID:</strong> <I>{hex(response.resp[0]-0x40)}</I></p>
    <p><strong>Subfunction Name:</strong> <I>Report Number Of DTC By Status Mask {hex(response.resp[1])} </I></p>
    <p><strong>DTC Status Availability Mask:</strong> <I> {hex(response.resp[2])} </I></p>
    <p><strong>DTC Format Identifier:</strong> <I> {hex(response.resp[3])} {DTCFormatIdentifierName} </I></p>
    <p><strong>DTC Count:</strong> <I> {combined_value} </I></p>
    <p><strong>Info:</strong> <I> Service 19 sunfunction 01 is successfully executed with DTC Status Mask 0x{status_mask}</I></p>
'''

        elif(response.type == "Negative Response"):
            response_html = f'''<h4><U>Negative Response Recieved</U></h4>
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
 Explaination:   Read DTC Information (Service 19 subfunction 01) Requested for DTC Status Mask {status_mask}
 UDS Response:   [{" ".join(hex(number) for number in response.resp)}]
 Explaination:   {response_text}<------------------- LOG ENTRY END ------------------->

# '''
        return
    
    def closeEvent(self, event):
        # Custom logic when the window is closed
        gen.log_action(f"Window Close", f"Service 19 01 Window Closed.")
        return
    





if __name__ == "__main__":
    import sys
    #current_user = os.getlogin()
    #currenttime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #print(f"<---- LOG ENTRY [{current_user} - {currenttime}] ---->")
    app = QtWidgets.QApplication(sys.argv)
    Form_SID19_01 = QtWidgets.QWidget()
    ui = Ui_Service19_01()
    ui.setupUi(Form_SID19_01)
    ui.redesign_ui()
    ui.connectFunctions()
    #Initializing the CAN
    if RUNNING_ON_RASPBERRYPI == True:
        os.system(f'sudo ip link set {conf.can_channel} up type can bitrate {conf.baudrate} dbitrate {conf.datarate} restart-ms 1000 berr-reporting on fd on')
        conf.tx = can.interface.Bus(channel=conf.can_channel, bustype='socketcan', fd=True)
        conf.rx = can.interface.Bus(channel=conf.can_channel, bustype='socketcan', fd=True)

    Form_SID19_01.show()
    sys.exit(app.exec_())