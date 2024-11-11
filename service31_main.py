from environment import *

if RUNNING_ON_RASPBERRYPI == False:
    import uds_dummy as uds     #will have to be replaced with actual uds file while testing on board
else:
    import uds
    import can
from service31_base import Ui_Form_SID_31
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import service31_functions as fun
from bs4 import BeautifulSoup
import os
import datetime
import general as gen
import uds_dummy as uds     #will have to be replaced with actual uds file while testing on board
import configure as conf
import os



class Ui_Service31(Ui_Form_SID_31):
    def redesign_ui(self):
        pass

    def connectFunctions(self):
        self.pushButton_Send31Req.clicked.connect(self.send31service)
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
        self.lineEdit_RoutineIdentifier.clear()
        self.update_status("Userform cleared successfully")
        gen.log_action("Button Click", "Clear Form for Service 31 window clicked. Userfields cleared successfully.")
        return
    
    def addlog(self):
        #Add the uds transaction to the log file
        gen.log_udsreport(self.logentrystring)
        self.logentrystring = ""    #Clear the log entry so that if multiple tiomes the button is clicked continuously only one entry is made.
        self.update_status(f"Log file appended with the current UDS transaction (./reports/uds_log_report.txt)")
        gen.log_action("Button Click", "Add to Log button for Service 31 window clicked.")
        return
    
    def clearlog(self):
        gen.clearudslogfile()
        self.update_status(f"Log file cleared (./reports/uds_log_report.txt)")
        gen.log_action("Button Click", "Clear Log button for Service 31 window clicked.")
        return
    
    def send31service(self):
        index_sub_fun = self.Subfunction.currentIndex()
        sub_fun = fun.get_subfunction(index_sub_fun)
        sub_fun_name=fun.get_subfunction_name(sub_fun)
        rid_string = self.lineEdit_RoutineIdentifier.text().strip().replace(" ","").replace(" ","").replace(" ","")
        gen.log_action("Button Click", f"Send 31 request button clicked with RID[{rid_string}].")
        sprmib_flg = self.checkBox_suppressposmsg.isChecked()
        SR=self.checkBox_StatusRecord.isChecked()

        #First check if a valid DID is entered in DID field        
        if(False == gen.check_2Bytehexadecimal(rid_string)):
            #Show messagebox with enter valid DID value
            self.update_status("Please enter a valid RID value. It must be 2 byte in hexadecimal format")
            #print(f"DID {did_string} is invalid")
            gen.log_action("UDS Request Fail", "31 Request not happened due to invalid RID format")
            return 
        
        #print(f"RID {rid_string} is valid")
        if(SR==False):
            service_request = fun.form_reqmsg4srv31_without_SR(sub_fun,rid_string,sprmib_flg)
        else:
            status_record = self.lineEdit_StatusRecord.text().strip().replace(" ","").replace(" ","").replace(" ","")
            if not gen.check_hexadecimal(status_record):
                self.update_status("Invalid Option  Record. Please enter a valid hexadecimal value.")
                gen.log_action("UDS Request Fail", "31 Request failed due to invalid option Record.")
                return
            if len(status_record) % 2 != 0:
                self.update_status("The length of Option record must be even since its in bytes formart.")
                gen.log_action("UDS Request Fail", "31 Request failed due to invalid option record.")
                return
            gen.log_action("Button Click", f"Send 31 request button clicked with Status Record[{status_record}].")
            service_request = fun.form_reqmsg4srv31_with_SR(sub_fun,rid_string,status_record,sprmib_flg)
        #Send the service request and get the response 
        if(sprmib_flg == False):
            IsPosResExpected = True 
        else:
            IsPosResExpected = False 

        gen.IsAnyServiceActive = True   #Next request is triggered, so make True      
        while(gen.IsTesterPresentActive == True):
            self.update_status("WAIT!! Tester present (Service 31) is currently ongoing")
            
        response = uds.sendRequest(service_request, IsPosResExpected)

        #print(f'The request is {" ".join(hex(number) for number in service_request)}')
        
        gen.IsAnyServiceActive = True   #Next request is triggered, so make True
        #Send the service request  
        while(gen.IsTesterPresentActive == True):
            self.update_status("WAIT!! Tester present (Service 31) is currently ongoing")
            
        response = uds.sendRequest(service_request, True)

        gen.IsAnyServiceActive = False   #Next response recieved , so make False
        
        self.update_status("Service 31 request is sent")
        gen.log_action("UDS Request Success", f"31 Request Successfully sent : {' '.join(hex(number) for number in service_request)}")

        if(response.type == "Positive Response"):
            response_html = f'''<h4><U>Positive Response Recieved</U></h4>
    <p><strong>Service ID:</strong> <I>{hex(response.resp[0]-0x40)}</I></p>
    <p><strong>RID:</strong> <I>{hex(response.resp[1])} {hex(response.resp[2])}</I></p>
    <p><strong>Info:</strong> <I>Service 31 is successfully sent with the sub function {sub_fun_name} with RID {hex(response.resp[1])} {hex(response.resp[2])} successfully</I></p>
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
Explaination:   Routine control (Service 31) Requested for {sub_fun_name} with RID 0x{rid_string}
UDS Response:   [{" ".join(hex(number) for number in response.resp)}]
Explaination:   {response_text}<------------------- LOG ENTRY END ------------------->

'''
        return
    
    def closeEvent(self, event):
        # Custom logic when the window is closed
        gen.log_action(f"Window Close", f"Service 31 Window Closed.")
        return
    





if __name__ == "__main__":
    import sys
    #current_user = os.getlogin()
    #currenttime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #print(f"<---- LOG ENTRY [{current_user} - {currenttime}] ---->")
    app = QtWidgets.QApplication(sys.argv)
    Form_SID31 = QtWidgets.QWidget()
    ui = Ui_Service31()
    ui.setupUi(Form_SID31)
    ui.redesign_ui()
    ui.connectFunctions()
    #Initializing the CAN
    #os.system(f'sudo ip link set {conf.can_channel} up type can bitrate {conf.baudrate} dbitrate {conf.datarate} restart-ms 1000 berr-reporting on fd on')

    #conf.tx = can.interface.Bus(channel=conf.can_channel, bustype='socketcan', fd=True)
    #conf.rx = can.interface.Bus(channel=conf.can_channel, bustype='socketcan', fd=True)

    Form_SID31.show()
    sys.exit(app.exec_())