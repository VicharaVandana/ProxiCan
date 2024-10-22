from environment import *

if RUNNING_ON_RASPBERRYPI == False:
    import uds_dummy as uds     #will have to be replaced with actual uds file while testing on board
else:
    import uds
    import can


from service85_base import Ui_Form_SID85
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import service85_functions as fun
from bs4 import BeautifulSoup
import os
import datetime
import general as gen
import configure as conf
import os



class Ui_Service85(Ui_Form_SID85):
    def redesign_ui(self):
        pass    
        
    def connectFunctions(self):
        self.pushButton_Send85Req.clicked.connect(self.send85service)
        self.pushButton_reset.clicked.connect(self.clearform)
        self.pushButton_appendLog.clicked.connect(self.addlog)
        self.pushButton_clearLog.clicked.connect(self.clearlog)
        
        
    
    def update_status(self, msg):
        # Create a QMessageBox instance
        self.label_status.setText(msg)
        return
    
    def clearform(self):
        #Clears all the fields for entering new service request
        self.logentrystring = ""
        self.label_ResType.setText("No Response")
        self.textBrowser_Resp.clear()
        self.comboBox_DTCSettingType.setCurrentIndex(0)
        self.checkBox_suppressposmsg.setChecked(False)
        self.update_status("Userform cleared successfully")
        gen.log_action("Button Click", "Clear Form for Service 85 window clicked. Userfields cleared successfully.")
        return
    
    def addlog(self):
        #Add the uds transaction to the log file
        gen.log_udsreport(self.logentrystring)
        self.logentrystring = ""    #Clear the log entry so that if multiple tiomes the button is clicked continuously only one entry is made.
        self.update_status(f"Log file appended with the current UDS transaction (Mainwindow/reports/cantraffic_log_report.txt)")
        gen.log_action("Button Click", "Add to Log button for Service 85 window clicked.")
        return
    
    def clearlog(self):
        gen.clearudslogfile()
        self.update_status(f"Log file cleared (Mainwindow/reports/cantraffic_log_report.txt)")
        gen.log_action("Button Click", "Clear Log button for Service 85 window clicked.")
        return
    
    def send85service(self):
        index_DTCSession = self.comboBox_DTCSettingType.currentIndex()
        session = fun.getsubfunction(index_DTCSession)
        session_name = fun.getsubfunctionname(session)
        sprmib_flg = self.checkBox_suppressposmsg.isChecked()
        if(self.checkBox_DTCOption.isChecked()): 
            dtc_string= self.lineEdit_DTCSettingInput.text().strip().replace(" ","").replace(" ","").replace(" ","")
            if(False == gen.check_3Bytehexadecimal(dtc_string)):
                self.update_status("Please enter a valid DTC value. It must be 3 byte in hexadecimal format")
                print(f"DTC {dtc_string} is invalid")
                gen.log_action("UDS Request Fail", "85 Request not happened due to invalid DTC format")
                return
        
    
        


        #session should be a valid value and not zero
        if(0 == session):
            self.update_status("Please select a valid Reset Type.")
            gen.log_action("UDS Request Fail", f"85 Request not happened due to invalid  Reset Type selection [{self.comboBox_DTCSettingType.currentText()}]")
            return
        
        #Get the service Request List for Control DTC Setting service

        if(self.checkBox_DTCOption.isChecked()):
            service_request = fun.form_reqmsg4srv85_withdtc(session,sprmib_flg,dtc_string)
        else:
            service_request = fun.form_reqmsg4srv85(session,sprmib_flg)
        

        #Send the service request and get the response 
        if(sprmib_flg == False):
            IsPosResExpected = True 
        else:
            IsPosResExpected = False 
               
        response = uds.sendRequest(service_request, IsPosResExpected)
        
        self.update_status("Service 85 request is sent")
        gen.log_action("UDS Request Success", f"85 Request Successfully sent : {' '.join(hex(number) for number in service_request)}")

        if(response.type == "Positive Response"):
            #p2servermax = ((response.resp[2] << 8)|(response.resp[3]))
            #p2starservermax = ((response.resp[4] << 8)|(response.resp[5]))

            response_html = f'''<h4><U>Positive Response Recieved</U></h4>
    <p><strong>Service ID:</strong> <I>{hex(response.resp[0]-0x40)}</I></p>
    <p><strong>Control DTC Setting Type:</strong> <I>{hex(response.resp[1])} {session_name}</I></p>
    <p><strong>Suppress Positive Message Request:</strong> <I>{sprmib_flg}</I></p>
    
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
Explaination:   Control DTC Setting (Service 85) Requested for Control DTC Setting type 0x{session} {session_name} 
SPRMIB flag :   {sprmib_flg}
UDS Response:   [{" ".join(hex(number) for number in response.resp)}]
Explaination:   {response_text}<------------------- LOG ENTRY END ------------------->

'''
        return




if __name__ == "__main__":
    import sys
    #current_user = os.getlogin()
    #currenttime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #print(f"<---- LOG ENTRY [{current_user} - {currenttime}] ---->")
    app = QtWidgets.QApplication(sys.argv)
    Form_SID85 = QtWidgets.QWidget()
    ui = Ui_Service85()
    ui.setupUi(Form_SID85)
    ui.redesign_ui()
    ui.connectFunctions()
    #Initializing the CAN
    if RUNNING_ON_RASPBERRYPI == True:
        os.system(f'sudo ip link set {conf.can_channel} up type can bitrate {conf.baudrate} dbitrate {conf.datarate} restart-ms 1000 berr-reporting on fd on')
        conf.tx = can.interface.Bus(channel=conf.can_channel, bustype='socketcan', fd=True)
        conf.rx = can.interface.Bus(channel=conf.can_channel, bustype='socketcan', fd=True)

    Form_SID85.show()
    sys.exit(app.exec_())
