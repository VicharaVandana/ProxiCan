from environment import *
 
if RUNNING_ON_RASPBERRYPI == False:
    import uds_dummy as uds  # Replace with actual uds on target
else:
    import uds
    import can
 
from service2e_base import Ui_Form_SID2E
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import service2e_functions as fun
from bs4 import BeautifulSoup
import os
import datetime
import general as gen
import configure as conf
import json
 
class Ui_Service2E(Ui_Form_SID2E):
 
    def redesign_ui(self):
        pass
 
    def connectFunctions(self):
        self.pushButton_Send2EReq.clicked.connect(self.send2Eservice)
        self.pushButton_reset.clicked.connect(self.clearform)
        self.pushButton_appendLog.clicked.connect(self.addlog)
        self.pushButton_clearLog.clicked.connect(self.clearlog)
        self.comboBox_entryType.currentTextChanged.connect(self.updateEntryModeAndLoadDIDs)
        return
 
    def update_status(self, msg):
        self.label_status.setText(msg)
        return
 
    def clearform(self):
        self.logentrystring = ""
        self.label_ResType.setText("No Response")
        self.textBrowser_Resp.clear()
        self.lineEdit_manualDID.clear()
        self.textEdit_datavalue.clear()
        self.update_status("Userform cleared successfully")
        gen.log_action("Button Click", "Clear Form for Service 2E window clicked. Userfields cleared successfully.")
        return
 
    def addlog(self):
        gen.log_udsreport(self.logentrystring)
        self.logentrystring = ""
        self.update_status("Log file appended with the current UDS transaction (./reports/uds_log_report.txt)")
        gen.log_action("Button Click", "Add to Log button for Service 2E window clicked.")
        return
 
    def clearlog(self):
        gen.clearudslogfile()
        self.update_status("Log file cleared (./reports/uds_log_report.txt)")
        gen.log_action("Button Click", "Clear Log button for Service 2E window clicked.")
        return
 
    def updateEntryModeAndLoadDIDs(self, mode):
        self.updateEntryMode(mode)
        if mode == "Enable Dropdown Entry":
            self.comboBox_DID.clear()
            try:
                with open("data.json", "r", encoding='utf-8') as f:
                    data_list = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                data_list = []

            if not data_list:
                QMessageBox.warning(None, "No Data", "No DID data available. Load a file ")
                return

            filtered_dids = [
                f"{row['DID']} - {row['Name']}"
                for row in data_list if row.get("0x22 Service", "").upper() in ["TRUE", "1"]
            ]

            if filtered_dids:
                self.comboBox_DID.addItems(filtered_dids)
            else:
                QMessageBox.warning(None, "No Matching DIDs", "No DIDs found with 2E service enabled.")


    def send2Eservice(self):
        mode = self.comboBox_entryType.currentText()
        if mode == "Enable Manual Entry":
            did_string = self.lineEdit_manualDID.text().strip()
        else:
            selected_text = self.comboBox_DID.currentText()
            if not selected_text:
                self.update_status("Please select a DID before sending.")
                return
            did_string = selected_text.split("-")[0].strip()
 
        dataval_string = self.textEdit_datavalue.toPlainText().replace(" ", "").replace("\t", "").replace("\n", "")
        gen.log_action("Button Click", f"Send 2E request button clicked with DID[{did_string}] and data value[{dataval_string}].")
 
        if False == gen.check_2Bytehexadecimal(did_string):
            self.update_status("Please enter a valid DID value. It must be 2 byte in hexadecimal format")
            gen.log_action("UDS Request Fail", "2E Request not happened due to invalid DID format")
            return
 
        if False == gen.check_min1Bytehexadecimal(dataval_string):
            self.update_status("Please enter a valid Data value. It must be in hexadecimal format in bytes. Each byte needs to have 2 characters. lik 03 or 6F etc Minimum 1 byte is needed.")
            gen.log_action("UDS Request Fail", "2E Request not happened due to invalid data value format")
            return
 
        service_request = fun.form_reqmsg4srv2E(did_string, dataval_string)
        gen.IsAnyServiceActive = True
 
        while gen.IsTesterPresentActive:
            self.update_status("WAIT!! Tester present (Service 3E) is currently ongoing")
 
        response = uds.sendRequest(service_request, True)
        gen.IsAnyServiceActive = False
        print(response)
        self.update_status("Service 2E request is sent")
        gen.log_action("UDS Request Success", f"2E Request Successfully sent : {' '.join(hex(number) for number in service_request)}")
 
        if response.type == "Positive Response":
            response_html = f'''<h4><U>Positive Response Received</U></h4>
<p><strong>Service ID:</strong> <I>{hex(response.resp[0]-0x40)}</I></p>
<p><strong>DID:</strong> <I>{hex(response.resp[1])} {hex(response.resp[2])}</I></p>
<p><strong>Data:</strong> <I>{' '.join(hex(number) for number in service_request[3:])}</I></p>'''
 
        elif response.type == "Negative Response":
            response_html = f'''<h4><U>Negative Response Received</U></h4>
<p><strong>NRC Code:</strong> <I>{hex(response.nrc)}</I></p>
<p><strong>NRC Name:</strong> <I>{response.nrcname}</I></p>
<p><strong>NRC Desc:</strong> <I>{response.nrcdesc}</I></p>'''
 
        elif response.type == "Unknown Response Type":
            response_html = f'''<h4><U>Unidentified Response Received</U></h4>
<p><strong>Response Bytes:</strong> <I>{' '.join(hex(number) for number in response.resp)}</I></p>'''
 
        elif response.type == "No Response":
            response_html = f'''<h4><U>No Response Received</U></h4>
<p><strong>Response Bytes:</strong> <I>{' '.join(hex(number) for number in response.resp)}</I></p>'''
 
        else:
            response_html = f'''<h4><U>ERROR OCCURRED</U></h4>'''
 
        self.label_ResType.setText(response.type)
        self.textBrowser_Resp.setHtml(response_html)
 
        current_user = os.getlogin()
        currenttime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        soup = BeautifulSoup(response_html, 'html.parser')
        response_text = soup.get_text()
 
        self.logentrystring = f'''<---- LOG ENTRY [{current_user} - {currenttime}] ---->
UDS Request :   [{' '.join(hex(number) for number in service_request)}]
Explanation:   Write Data By Identifier (Service 2E) Requested for DID 0x{did_string} and data: 0x{dataval_string}
UDS Response:   [{' '.join(hex(number) for number in response.resp)}]
Explanation:   {response_text}<------------------- LOG ENTRY END ------------------->'''
 
        return
 
    def closeEvent(self, event):
        gen.log_action("Window Close", "Service 2E Window Closed.")
        return
 
 
if __name__ == "__main__":
    import sys
    #current_user = os.getlogin()
    #currenttime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #print(f"<---- LOG ENTRY [{current_user} - {currenttime}] ---->")
    app = QtWidgets.QApplication(sys.argv)
    Form_SID2E = QtWidgets.QWidget()
    ui = Ui_Service2E()
    ui.setupUi(Form_SID2E)
    ui.redesign_ui()
    ui.connectFunctions()
    
    #Initializing the CAN
    if RUNNING_ON_RASPBERRYPI == True:
        os.system(f'sudo ip link set {conf.can_channel} up type can bitrate {conf.baudrate} dbitrate {conf.datarate} restart-ms 1000 berr-reporting on fd on')
        conf.tx = can.interface.Bus(channel=conf.can_channel, bustype='socketcan', fd=True)
        conf.rx = can.interface.Bus(channel=conf.can_channel, bustype='socketcan', fd=True)

    Form_SID2E.show()
    sys.exit(app.exec_())
        
 
