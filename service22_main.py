from environment import *

if RUNNING_ON_RASPBERRYPI == False:
    import uds_dummy as uds
else:
    import uds
    import can

from service22_base import Ui_Form_SID22
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import service22_functions as fun
from bs4 import BeautifulSoup
import os
import datetime
import general as gen
import configure as conf
import json

class Ui_Service22(Ui_Form_SID22):
    def redesign_ui(self):
        pass

    def connectFunctions(self):
        self.pushButton_Send22Req.clicked.connect(self.send22service)
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
        self.lineEdit_DID.clear()
        self.comboBox_DIDs.setCurrentIndex(0)
        self.update_status("Userform cleared successfully")
        gen.log_action("Button Click", "Clear Form for Service 22 window clicked. Userfields cleared successfully.")
        return

    def addlog(self):
        gen.log_udsreport(self.logentrystring)
        self.logentrystring = ""
        self.update_status("Log file appended with the current UDS transaction (./reports/uds_log_report.txt)")
        gen.log_action("Button Click", "Add to Log button for Service 22 window clicked.")
        return

    def clearlog(self):
        gen.clearudslogfile()
        self.update_status("Log file cleared (./reports/uds_log_report.txt)")
        gen.log_action("Button Click", "Clear Log button for Service 22 window clicked.")
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
                QMessageBox.warning(None, "No Matching DIDs", "No DIDs found with 22 service enabled.")


    def send22service(self):
        try:
                with open("data.json", "r", encoding='utf-8') as f:
                    data_list = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
                data_list = []
        mode = self.comboBox_entryType.currentText()
        if mode == "Enable Manual Entry":
            did_string = self.lineEdit_manualDID.text().strip().replace(" ", "")
        else:
            selected_text = self.comboBox_DID.currentText()
            if not selected_text:
                self.update_status("Please select a DID before sending.")
                return
            did_string = selected_text.split("-")[0].strip()

        gen.log_action("Button Click", f"Send 22 request button clicked with DID[{did_string}].")

        if not gen.check_2Bytehexadecimal(did_string):
            self.update_status("Please enter a valid DID value. It must be 2 byte in hexadecimal format")
            gen.log_action("UDS Request Fail", "22 Request not happened due to invalid DID format")
            return

        self.update_status("DID is validated.")
        service_request = fun.form_reqmsg4srv22(did_string)

        gen.IsAnyServiceActive = True
        while gen.IsTesterPresentActive:
            self.update_status("WAIT!! Tester present (Service 3E) is currently ongoing")

        response = uds.sendRequest(service_request, True)
        gen.IsAnyServiceActive = False

        self.update_status("Service 22 request is sent")
        gen.log_action("UDS Request Success", f"22 Request Successfully sent : {' '.join(hex(number) for number in service_request)}")
       
       
        if response.type == "Positive Response":
            sid = response.resp[0]
            did = f"{response.resp[1]:02X}{response.resp[2]:02X}"  # Combine DID bytes
            print(did)
            data_bytes = response.resp[3:]
            entry = next((d for d in data_list if d["DID"].replace("0x","").replace(" ", " ").upper()==did.upper()),None)
            #entry = next((d for d in data_list if d["DID"].upper()==did.upper()))
            if not entry:
                return f"<p><strong>DID:</strong> <i>{did}</i></p><p><strong>Error:</strong> DID not found</p>"

            name = entry.get("Name", "")
            value_did = entry.get("DID")
            value_type = entry.get("Value type", "").lower()
            value_table = entry.get("Value Table", {})
            print(value_type)
            interpreted = []
            if value_did == did:
                if value_type == "list" and isinstance(value_table,str) and "-" in value_table:
                    vt_dict = {}
                    for pair in value_table.split(","): 
                        if "-" in pair:
                            key,val = pair.strip().split("-",1)
                            vt_dict[key.strip().lower()] = val.strip()
                    for byte in data_bytes:
                        value_hex = f"0x{int(byte):02x}".lower()
                        if value_hex in vt_dict:
                            interpreted.append(f"{value_hex} - {vt_dict[value_hex]}")
                        else:
                            interpreted.append(f"{value_hex} - No data found")

                elif value_type == "formatted string":
                    
                    try:
                        hex_str = ''.join(f"{byte:02X}" for byte in data_bytes)
                        value = int(hex_str,16)
                        interpreted_value = eval(f'f"""{value_table}"""')
                            
                    except Exception as e:
                        interpreted_value = f"Error in format: {e}"
                        print(interpreted_value)
                    interpreted.append(str(interpreted_value))
                interpreted_html ="<br>".join(interpreted)
                

            
            response_html = f'''<h4><U>Positive Response Recieved</U></h4>
    <p><strong>Service ID:</strong> <I>{hex(response.resp[0]-0x40)}</I></p>
    <p><strong>DID:</strong> <I>{hex(response.resp[1])} {hex(response.resp[2])}</I></p>
    <p><strong>Data:</strong> <I>{" ".join(hex(number) for number in response.resp[3:])}</I></p>
    <p><strong>Interpreted:</strong> <I>{interpreted_html}</I></p>
'''
            
        elif response.type == "Negative Response":
            response_html = f'''<h4><U>Negative Response Recieved</U></h4>
    <p><strong>NRC Code:</strong> <I>{hex(response.nrc)}</I></p>
    <p><strong>NRC Name:</strong> <I>{response.nrcname}</I></p>
    <p><strong>NRC Desc:</strong> <I>{response.nrcdesc}</I></p>
'''
        elif response.type == "Unknown Response Type":
            response_html = f'''<h4><U>Unidentified Response Recieved</U></h4>
    <p><strong>Response Bytes:</strong> <I>{" ".join(hex(number) for number in response.resp)}</I></p>
'''
        elif response.type == "No Response":
            response_html = f'''<h4><U>No Response Recieved</U></h4>
    <p><strong>Response Bytes:</strong> <I>{" ".join(hex(number) for number in response.resp)}</I></p>
'''
        else:
            response_html = f'''<h4><U>ERROR OCCURED</U></h4>'''

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
        gen.log_action("Window Close", "Service 22 Window Closed.")
        return


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form_SID22 = QtWidgets.QWidget()
    ui = Ui_Service22()
    ui.setupUi(Form_SID22)
    ui.redesign_ui()
    ui.connectFunctions()

    if RUNNING_ON_RASPBERRYPI:
        os.system(f'sudo ip link set {conf.can_channel} up type can bitrate {conf.baudrate} dbitrate {conf.datarate} restart-ms 1000 berr-reporting on fd on')
        conf.tx = can.interface.Bus(channel=conf.can_channel, bustype='socketcan', fd=True)
        conf.rx = can.interface.Bus(channel=conf.can_channel, bustype='socketcan', fd=True)

    Form_SID22.show()
    sys.exit(app.exec_())