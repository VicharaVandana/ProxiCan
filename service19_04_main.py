from environment import *

if RUNNING_ON_RASPBERRYPI == False:
    import uds_dummy as uds     #will have to be replaced with actual uds file while testing on board
else:
    import uds
    import can
    
from service19_04_base import Ui_Form_SID_19_04
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


class Ui_Service19_04(Ui_Form_SID_19_04):
    def redesign_ui(self):
        pass

    def connectFunctions(self):
        self.pushButton_Send19_04Req.clicked.connect(self.send19_04service)
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
        self.lineEdit_DTCMaskRecord.clear()
        self.lineEdit_DTCSnapshotRecNumber.clear()
        self.update_status("Userform cleared successfully")
        gen.log_action("Button Click", "Clear Form for Service 19 subfunction 04 window clicked. Userfields cleared successfully.")
        return
    
    def addlog(self):
        #Add the uds transaction to the log file
        gen.log_udsreport(self.logentrystring)
        self.logentrystring = ""    #Clear the log entry so that if multiple tiomes the button is clicked continuously only one entry is made.
        self.update_status(f"Log file appended with the current UDS transaction (./reports/uds_log_report.txt)")
        gen.log_action("Button Click", "Add to Log button for Service 19 subfunction 04 window clicked.")
        return
    
    def clearlog(self):
        gen.clearudslogfile()
        self.update_status(f"Log file cleared (./reports/uds_log_report.txt)")
        gen.log_action("Button Click", "Clear Log button for Service 19 subfunction 04 window clicked.")
        return
    
    def send19_04service(self):
        sprmib_flg = self.checkBox_suppressposmsg.isChecked()
        DTCMaskRecord = self.lineEdit_DTCMaskRecord.text().strip().replace(" ","").replace(" ","").replace(" ","")
        DTCSnapshotRecordNumber = self.lineEdit_DTCSnapshotRecNumber.text().strip().replace(" ","").replace(" ","").replace(" ","")

        if not gen.check_3Bytehexadecimal(DTCMaskRecord):
            self.update_status("Invalid DTC Mask Record. Please enter a valid hexadecimal value of 3 bytes.")
            gen.log_action("UDS Request Fail", "19 Request failed due to invalid DTC Mask Record.")
            return
        
        if not gen.check_1Bytehexadecimal(DTCSnapshotRecordNumber):
            self.update_status("Invalid DTC Snapshot Record Number. Please enter a valid hexadecimal value of 1 byte.")
            gen.log_action("UDS Request Fail", "19 Request failed due to invalid DTC Snapshot Record Number.")
            return

        service_request = fun.form_reqmsg4srv19_subfun_4(DTCMaskRecord,DTCSnapshotRecordNumber,sprmib_flg)

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
            self.update_status("Service 19 subfunction 04 response is received")
 
            response_html = f'''<h4><U>Positive Response Recieved</U></h4>
    <p><strong>Service ID:</strong> <I>{hex(response.resp[0]-0x40)}</I></p>
    <p><strong>Subfunction Name:</strong> <I>Report DTC Snapshot Record By DTC Number {hex(response.resp[1])} </I></p>
    <p><strong>Suppress Positive Message Request:</strong> <I>{sprmib_flg}</I></p>
    <p><strong>DTC And Status Record:</strong> <I> {" ".join(hex(number) for number in response.resp[2:6])} </I></p>
    <p><strong>DTC Snapshot Record Number:</strong> <I> {" ".join(hex(number) for number in response.resp[6:7])} </I></p>
    <p><strong>DTC Snapshot Record Number Of Identifiers:</strong> <I> {" ".join(hex(number) for number in response.resp[7:])} </I></p>
    <p><strong>Info:</strong> <I> Service 19 sunfunction 04 is successfully executed with DTC Mask Record 0x{DTCMaskRecord} and DTC Snapshot Record Number 0x{DTCSnapshotRecordNumber}</I></p>
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
 Explaination:   Read DTC Information (Service 19 subfunction 04) Requested for DTC Mask Record {DTCMaskRecord} , DTC Snapshot Record Number {DTCSnapshotRecordNumber} and SPRMIB flag {sprmib_flg}
 UDS Response:   [{" ".join(hex(number) for number in response.resp)}]
 Explaination:   {response_text}<------------------- LOG ENTRY END ------------------->

# '''
        return
    
    def closeEvent(self, event):
        # Custom logic when the window is closed
        gen.log_action(f"Window Close", f"Service 19 04 Window Closed.")
        return
    





if __name__ == "__main__":
    import sys
    #current_user = os.getlogin()
    #currenttime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #print(f"<---- LOG ENTRY [{current_user} - {currenttime}] ---->")
    app = QtWidgets.QApplication(sys.argv)
    Form_SID19_04 = QtWidgets.QWidget()
    ui = Ui_Service19_04()
    ui.setupUi(Form_SID19_04)
    ui.redesign_ui()
    ui.connectFunctions()
    #Initializing the CAN
    if RUNNING_ON_RASPBERRYPI == True:
        os.system(f'sudo ip link set {conf.can_channel} up type can bitrate {conf.baudrate} dbitrate {conf.datarate} restart-ms 1000 berr-reporting on fd on')
        conf.tx = can.interface.Bus(channel=conf.can_channel, bustype='socketcan', fd=True)
        conf.rx = can.interface.Bus(channel=conf.can_channel, bustype='socketcan', fd=True)

    Form_SID19_04.show()
    sys.exit(app.exec_())