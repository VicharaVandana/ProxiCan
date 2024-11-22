from environment import *

if RUNNING_ON_RASPBERRYPI == False:
    import uds_dummy as uds     #will have to be replaced with actual uds file while testing on board
else:
    import uds
    import can
    
from service10_base import Ui_Form_SID10
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import service10_functions as fun
from bs4 import BeautifulSoup
import os
import datetime
import general as gen
import configure as conf
import os



class Ui_Service10(Ui_Form_SID10):
    def redesign_ui(self):
        pass    
        
    def connectFunctions(self):
        self.pushButton_Send10Req.clicked.connect(self.send10service)
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
        self.comboBox_Diagsession.setCurrentIndex(0)
        self.checkBox_suppressposmsg.setChecked(False)
        self.update_status("Userform cleared successfully")
        gen.log_action("Button Click", "Clear Form for Service 10 window clicked. Userfields cleared successfully.")
        return
    
    def addlog(self):
        #Add the uds transaction to the log file
        gen.log_udsreport(self.logentrystring)
        self.logentrystring = ""    #Clear the log entry so that if multiple tiomes the button is clicked continuously only one entry is made.
        self.update_status(f"Log file appended with the current UDS transaction (./reports/uds_log_report.txt)")
        gen.log_action("Button Click", "Add to Log button for Service 10 window clicked.")
        return
    
    def clearlog(self):
        gen.clearudslogfile()
        self.update_status(f"Log file cleared (./reports/uds_log_report.txt)")
        gen.log_action("Button Click", "Clear Log button for Service 10 window clicked.")
        return
    
    def send10service(self):
        index_dscSession = self.comboBox_Diagsession.currentIndex()
        session = fun.getsubfunction(index_dscSession)
        sprmib_flg = self.checkBox_suppressposmsg.isChecked()

        #session should be a valid value and not zero
        if(0 == session):
            self.update_status("Please select a valid diagnostic session.")
            gen.log_action("UDS Request Fail", f"10 Request not happened due to invalid Diag session selection [{self.comboBox_Diagsession.currentText()}]")
            return
        
        #Get the service Request List for Diagnostic Session Control
        service_request = fun.form_reqmsg4srv10(session,sprmib_flg)

        #Send the service request and get the response 
        if(sprmib_flg == False):
            IsPosResExpected = True 
        else:
            IsPosResExpected = False 

        gen.IsAnyServiceActive = True   #Next request is triggered, so make True      
        while(gen.IsTesterPresentActive == True):
            self.update_status("WAIT!! Tester present (Service 3E) is currently ongoing")
            
        response = uds.sendRequest(service_request, IsPosResExpected)
        gen.IsAnyServiceActive = False   #Next response recieved , so make False
        
        self.update_status("Service 10 request is sent")
        gen.log_action("UDS Request Success", f"10 Request Successfully sent : {' '.join(hex(number) for number in service_request)}")

        if(response.type == "Positive Response"):
            p2servermax = ((response.resp[2] << 8)|(response.resp[3]))
            p2starservermax = ((response.resp[4] << 8)|(response.resp[5]))

            response_html = f'''<h4><U>Positive Response Recieved</U></h4>
    <p><strong>Service ID:</strong> <I>{hex(response.resp[0]-0x40)}</I></p>
    <p><strong>Diag Session:</strong> <I>{hex(response.resp[1])}</I></p>
    <p><strong>Suppress Positive Message Request:</strong> <I>{sprmib_flg}</I></p>
    <p><strong>P2ServerMax:</strong> <I>{p2servermax} milliseconds</I></p>
    <p><strong>P2*ServerMax:</strong> <I>{p2starservermax} milliseconds</I></p>
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
        elif(response.type == "Positive Response" & sprmib_flg == True ):
            p2servermax = ((response.resp[2] << 8)|(response.resp[3]))
            p2starservermax = ((response.resp[4] << 8)|(response.resp[5]))
            response_html = f'''<h4><U>Positive Response Recieved after a Response Pending (0x78)</U></h4>
    <p><strong>Service ID:</strong> <I>{hex(response.resp[0]-0x40)}</I></p>
    <p><strong>Diag Session:</strong> <I>{hex(response.resp[1])}</I></p>
    <p><strong>Positive Response Pending count:</strong> <I>{response.positiveResponsePending_count}</I></p>
    <p><strong>Suppress Positive Message Request:</strong> <I>{sprmib_flg}</I></p>
    <p><strong>P2ServerMax:</strong> <I>{p2servermax} milliseconds</I></p>
    <p><strong>P2*ServerMax:</strong> <I>{p2starservermax} milliseconds</I></p>
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
Explaination:   Diagnostic Session Control (Service 10) Requested for session 0x{session} and SPRMIB flag {sprmib_flg}
UDS Response:   [{" ".join(hex(number) for number in response.resp)}]
Explaination:   {response_text}<------------------- LOG ENTRY END ------------------->

# '''
        return
    
    def closeEvent(self, event):
        # Custom logic when the window is closed
        gen.log_action(f"Window Close", f"Service 10 Window Closed.")
        return




if __name__ == "__main__":
    import sys
    #current_user = os.getlogin()
    #currenttime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #print(f"<---- LOG ENTRY [{current_user} - {currenttime}] ---->")
    app = QtWidgets.QApplication(sys.argv)
    Form_SID10 = QtWidgets.QWidget()
    ui = Ui_Service10()
    ui.setupUi(Form_SID10)
    ui.redesign_ui()
    ui.connectFunctions()
    
    #Initializing the CAN
    if RUNNING_ON_RASPBERRYPI == True:
        os.system(f'sudo ip link set {conf.can_channel} up type can bitrate {conf.baudrate} dbitrate {conf.datarate} restart-ms 1000 berr-reporting on fd on')
        conf.tx = can.interface.Bus(channel=conf.can_channel, bustype='socketcan', fd=True)
        conf.rx = can.interface.Bus(channel=conf.can_channel, bustype='socketcan', fd=True)

    Form_SID10.show()
    sys.exit(app.exec_())
