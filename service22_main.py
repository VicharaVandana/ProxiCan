from service22_base import Ui_Form_SID22
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import service22_functions as fun
from bs4 import BeautifulSoup
import os
import datetime
import general as gen
import uds_dummy as uds     #will have to be replaced with actual uds file while testing on board
#pc#import uds
import configure as conf
import os
#pc#import can

class Ui_Service22(Ui_Form_SID22):
    def redesign_ui(self):
        pass    
        
    def connectFunctions(self):
        self.pushButton_Send22Req.clicked.connect(self.send22service)
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
        self.lineEdit_DID.clear()
        self.update_status("Userform cleared successfully")
        gen.log_action("Button Click", "Clear Form for Service 22 window clicked. Userfields cleared successfully.")
        return
    
    def addlog(self):
        #Add the uds transaction to the log file
        gen.log_udsreport(self.logentrystring)
        self.logentrystring = ""    #Clear the log entry so that if multiple tiomes the button is clicked continuously only one entry is made.
        self.update_status(f"Log file appended with the current UDS transaction (./reports/uds_log_report.txt)")
        gen.log_action("Button Click", "Add to Log button for Service 22 window clicked.")
        return
    
    def clearlog(self):
        gen.clearudslogfile()
        self.update_status(f"Log file cleared (./reports/uds_log_report.txt)")
        gen.log_action("Button Click", "Clear Log button for Service 22 window clicked.")
        return
    
    def send22service(self):
        #First check if a valid DID is entered in DID field
        did_string = self.lineEdit_DID.text().strip().replace(" ","").replace(" ","").replace(" ","")
        gen.log_action("Button Click", f"Send 22 request button clicked with DID[{did_string}].")

        if(False == gen.check_2Bytehexadecimal(did_string)):
            #Show messagebox with enter valid DID value
            self.update_status("Please enter a valid DID value. It must be 2 byte in hexadecimal format")
            gen.log_action("UDS Request Fail", "22 Request not happened due to invalid DID format")
            return 
        #DID is valid  
        self.update_status("DID is validated.")
        #Get the service Request List for Read Data By Identifier
        service_request = fun.form_reqmsg4srv22(did_string)
        
        gen.IsAnyServiceActive = True   #Next request is triggered, so make True
        while(gen.IsTesterPresentActive == True):
            self.update_status("WAIT!! Tester present (Service 3E) is currently ongoing")
        
        #Send the service request        
        response = uds.sendRequest(service_request, True)

        gen.IsAnyServiceActive = False   #Next response recieved , so make False

        
        
        self.update_status("Service 22 request is sent")
        gen.log_action("UDS Request Success", f"22 Request Successfully sent : {' '.join(hex(number) for number in service_request)}")

        

        if(response.type == "Positive Response"):
            response_html = f'''<h4><U>Positive Response Recieved</U></h4>
    <p><strong>Service ID:</strong> <I>{hex(response.resp[0]-0x40)}</I></p>
    <p><strong>DID:</strong> <I>{hex(response.resp[1])} {hex(response.resp[2])}</I></p>
    <p><strong>Data:</strong> <I>{" ".join(hex(number) for number in response.resp[3:])}</I></p>
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
Explaination:   Read Data By Itentifier (Service 22) Requested for DID 0x{did_string}
UDS Response:   [{" ".join(hex(number) for number in response.resp)}]
Explaination:   {response_text}<------------------- LOG ENTRY END ------------------->

'''
        return
    
    def closeEvent(self, event):
        # Custom logic when the window is closed
        gen.log_action(f"Window Close", f"Service 22 Window Closed.")
        return        


        
        
if __name__ == "__main__":
    import sys
    #current_user = os.getlogin()
    #currenttime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #print(f"<---- LOG ENTRY [{current_user} - {currenttime}] ---->")
    app = QtWidgets.QApplication(sys.argv)
    Form_SID22 = QtWidgets.QWidget()
    ui = Ui_Service22()
    ui.setupUi(Form_SID22)
    ui.redesign_ui()
    ui.connectFunctions()
    #Initializing the CAN
    #pc#os.system(f'sudo ip link set {conf.can_channel} up type can bitrate {conf.baudrate} dbitrate {conf.datarate} restart-ms 1000 berr-reporting on fd on')

    #pc#conf.tx = can.interface.Bus(channel=conf.can_channel, bustype='socketcan', fd=True)
    #pc#conf.rx = can.interface.Bus(channel=conf.can_channel, bustype='socketcan', fd=True)

    Form_SID22.show()
    sys.exit(app.exec_())