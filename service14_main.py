from environment import *

if RUNNING_ON_RASPBERRYPI == False:
    import uds_dummy as uds     #will have to be replaced with actual uds file while testing on board
else:
    import uds
    import can
    
from service14_base import Ui_Form_SID14
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import service14_functions as fun
from bs4 import BeautifulSoup
import os
import datetime
import general as gen
#import uds_dummy as uds     #will have to be replaced with actual uds file while testing on board
import configure as conf
import os


class Ui_Service14(Ui_Form_SID14):
    def redesign_ui(self):
        pass

    def connectFunctions(self):
        self.pushButton_Send14Req.clicked.connect(self.send14service)
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
        self.lineEdit_dtc.clear()
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
    
    def send14service(self):
        dtc_string = self.lineEdit_dtc.text().strip().replace(" ","").replace(" ","").replace(" ","")
        gen.log_action("Button Click", f"Send 14 request button clicked with DTC[{dtc_string}]].")

        #First check if a valid DTC is entered in DTC field        
        if(False == gen.check_3Bytehexadecimal(dtc_string)):
            #Show messagebox with enter valid DTC value
            self.update_status("Please enter a valid DTC value. It must be 3 byte in hexadecimal format")
            #print(f"DTC {dtc_string} is invalid")
            gen.log_action("UDS Request Fail", "14 Request not happened due to invalid DTC format")
            return 
        
        #print(f"DTC {dtc_string} is valid")
         #Next check if a valid Data values is entered in hex format

        
        #print(f"Data {dataval_string} is valid")
        #Get the service Request List for Read Data By Identifier
        service_request = fun.form_reqmsg4srv14(dtc_string)

        #print(f'The request is {" ".join(hex(number) for number in service_request)}')
        
        gen.IsAnyServiceActive = True   #Next request is triggered, so make True
        #Send the service request  
        while(gen.IsTesterPresentActive == True):
            self.update_status("WAIT!! Tester present (Service 3E) is currently ongoing")
            
        response = uds.sendRequest(service_request, True)

        gen.IsAnyServiceActive = False   #Next response recieved , so make False
        
        self.update_status("Service 14 request is sent")
        gen.log_action("UDS Request Success", f"14 Request Successfully sent : {' '.join(hex(number) for number in service_request)}")
        print("RRRRR",response)

        if(response.type == "Positive Response"):
            response_html = f'''<h4><U>Positive Response Recieved</U></h4>
    <p><strong>Service ID:</strong> <I>{hex(response.resp[0]-0x40)}</I></p>
    <p><strong>DTC:</strong> <I>{dtc_string}</I></p>
    <p><strong>Info:</strong> <I> Service 14 is successfully sent with DTC bytes {dtc_string}</I></p>
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
Explaination:   Write Data By Itentifier (Service 14) Requested for DTC 0x{dtc_string}
UDS Response:   [{" ".join(hex(number) for number in response.resp)}]
Explaination:   {response_text}<------------------- LOG ENTRY END ------------------->

'''
        return
    
    def closeEvent(self, event):
        # Custom logic when the window is closed
        gen.log_action(f"Window Close", f"Service 14 Window Closed.")
        return
    





if __name__ == "__main__":
    import sys
    #current_user = os.getlogin()
    #currenttime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #print(f"<---- LOG ENTRY [{current_user} - {currenttime}] ---->")
    app = QtWidgets.QApplication(sys.argv)
    Form_SID14 = QtWidgets.QWidget()
    ui = Ui_Service14()
    ui.setupUi(Form_SID14)
    ui.redesign_ui()
    ui.connectFunctions()
    #Initializing the CAN
    if RUNNING_ON_RASPBERRYPI == True:
        os.system(f'sudo ip link set {conf.can_channel} up type can bitrate {conf.baudrate} dbitrate {conf.datarate} restart-ms 1000 berr-reporting on fd on')
        conf.tx = can.interface.Bus(channel=conf.can_channel, bustype='socketcan', fd=True)
        conf.rx = can.interface.Bus(channel=conf.can_channel, bustype='socketcan', fd=True)

    Form_SID14.show()
    sys.exit(app.exec_())