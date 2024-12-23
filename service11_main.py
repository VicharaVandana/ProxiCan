from environment import *

if RUNNING_ON_RASPBERRYPI == False:
    import uds_dummy as uds     #will have to be replaced with actual uds file while testing on board
else:
    import uds
    import can
    
from service11_base import Ui_Form_SID11
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import service11_functions as fun
from bs4 import BeautifulSoup
import os
import datetime
import general as gen
import configure as conf
import os
from service11_subfunctionsettings import Service11Subfunc_EnDis_Window
import json



class Ui_Service11(Ui_Form_SID11):
    def redesign_ui(self):
        self.load_subfunction_visibility()
        self.update_subfunction_visibility()
        return

    def load_subfunction_visibility(self):
        """Load the visibility settings for subfunctions from the JSON file."""
        try:
            with open('service11_subfunctionsettings.json', 'r') as file:
                data = json.load(file)
                self.subfunction11_visibility = data["Service_11_Subfunctions_Visibility"]
                print("Loaded JSON: ", self.subfunction11_visibility)  # Debugging line
        except FileNotFoundError:
            print("Error: service11_subfunctionsettings.json file not found.")
            self.subfunction11_visibility = {"01": True, "02": True, "03": True}  # Default visibility
        return

    def update_subfunction_visibility(self):
        """
        Update the visibility of each item in the combo box based on the loaded JSON data.
        Iterate backwards to safely remove items without affecting the loop.
        """
        for index in range(self.comboBox_ECUReset.count() - 1, -1, -1):
            item_text = self.comboBox_ECUReset.itemText(index)  # Get the text of the item (e.g., "01 - Hard reset")
            
            # Extract the numeric part of the item text to match the JSON keys
            item_key = item_text.split(" ")[0]  # Get the part before the space (e.g., "01", "02")
            print(f"Checking visibility for item: {item_key}")  # Debugging line
            
            # Check if the item key exists in visibility settings; default to True (visible) if not found
            visibility = self.subfunction11_visibility.get(item_key, True)
            print(f"Visibility for {item_key}: {visibility}")  # Debugging line
            
            if not visibility:
                # Remove the item from the combo box if it should be hidden
                self.comboBox_ECUReset.removeItem(index)
                print(f"Subfunction {item_key} hidden.")  # Debugging line
            else:
                print(f"Subfunction {item_key} visible.")  # Debugging line
        
        # Force an update of the combo box display
        self.comboBox_ECUReset.update()
        print("ComboBox update completed.")  # Debugging line
        return   
        
    def connectFunctions(self):
        self.pushButton_Send11Req.clicked.connect(self.send11service)
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
        self.comboBox_ECUReset.setCurrentIndex(0)
        self.checkBox_suppressposmsg.setChecked(False)
        self.update_status("Userform cleared successfully")
        gen.log_action("Button Click", "Clear Form for Service 11 window clicked. Userfields cleared successfully.")
        return
    
    def addlog(self):
        #Add the uds transaction to the log file
        gen.log_udsreport(self.logentrystring)
        self.logentrystring = ""    #Clear the log entry so that if multiple tiomes the button is clicked continuously only one entry is made.
        self.update_status(f"Log file appended with the current UDS transaction (Mainwindow/reports/cantraffic_log_report.txt)")
        gen.log_action("Button Click", "Add to Log button for Service 11 window clicked.")
        return
    
    def clearlog(self):
        gen.clearudslogfile()
        self.update_status(f"Log file cleared (Mainwindow/reports/cantraffic_log_report.txt)")
        gen.log_action("Button Click", "Clear Log button for Service 11 window clicked.")
        return
    
    def send11service(self):
        index_ERSession = self.comboBox_ECUReset.currentIndex()
        session_name = self.comboBox_ECUReset.itemText(index_ERSession)
        session_name_cleaned = session_name.split('-')[-1].strip()    
        print(session_name_cleaned)
        session = fun.getsubfunction(session_name_cleaned)
        print(session)
        #session_name_returned = fun.getsubfunctionname(session)
        sprmib_flg = self.checkBox_suppressposmsg.isChecked()
        

        

        #session should be a valid value and not zero
        if(0 == session):
            self.update_status("Please select a valid Reset Type.")
            gen.log_action("UDS Request Fail", f"11 Request not happened due to invalid Reset Type selection [{self.comboBox_ECUReset.currentText()}]")
            return
        
        #Get the service Request List for ECU Reset service
        service_request = fun.form_reqmsg4srv11(session,sprmib_flg)

        #Send the service request and get the response 
        if(sprmib_flg == False):
            IsPosResExpected = True 
        else:
            IsPosResExpected = False 
               
        response = uds.sendRequest(service_request, IsPosResExpected)

        
        self.update_status("Service 11 request is sent")
        gen.log_action("UDS Request Success", f"11 Request Successfully sent : {' '.join(hex(number) for number in service_request)}")
        reset_initiation=fun.checkresetinitiation(response)

        if(response.type == "Positive Response"):
            #p2servermax = ((response.resp[2] << 8)|(response.resp[3]))
            #p2starservermax = ((response.resp[4] << 8)|(response.resp[5]))

            response_html = f'''<h4><U>Positive Response Recieved</U></h4>
    <p><strong>Service ID:</strong> <I>{hex(response.resp[0]-0x40)}</I></p>
    <p><strong>Reset Type:</strong> <I>{hex(response.resp[1])} {session_name_cleaned}</I></p>
    <p><strong>Requested Reset Initiated:</strong> <I>{reset_initiation}</I></p>
    <p><strong>Suppress Positive Message Request:</strong> <I>{sprmib_flg}</I></p>
    <p><strong>Info:</strong> <I>Service 11 is successfully sent with reset type {session_name_cleaned}</I></p>   
'''

        elif(response.type == "Negative Response"):
            response_html = f'''<h4><U>Negative Response Recieved</U></h4>    
    <p><strong>Suppress Positive Message Request:</strong> <I>{sprmib_flg}</I></p>
    <p><strong>Requested Reset Initiated:</strong> <I>{reset_initiation}</I></p>
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
    <p><strong>Requested Reset Initiated:</strong> <I>{reset_initiation}</I></p>
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
Explaination:   ECU Reset (Service 11) Requested for reset type 0x{session} ({session_name_cleaned}) and SPRMIB flag {sprmib_flg}
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
    Form_SID11 = QtWidgets.QWidget()
    ui = Ui_Service11()
    ui.setupUi(Form_SID11)
    ui.redesign_ui()
    ui.connectFunctions()
    
    #Initializing the CAN
    if RUNNING_ON_RASPBERRYPI == True:
        os.system(f'sudo ip link set {conf.can_channel} up type can bitrate {conf.baudrate} dbitrate {conf.datarate} restart-ms 1000 berr-reporting on fd on')
        conf.tx = can.interface.Bus(channel=conf.can_channel, bustype='socketcan', fd=True)
        conf.rx = can.interface.Bus(channel=conf.can_channel, bustype='socketcan', fd=True)

    Form_SID11.show()
    sys.exit(app.exec_())
