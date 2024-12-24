from environment import *

if RUNNING_ON_RASPBERRYPI == False:
    import uds_dummy as uds     #will have to be replaced with actual uds file while testing on board
else:
    import uds
    import can
from service28_base import Ui_Form_SID28
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import service28_functions as fun
from bs4 import BeautifulSoup
import os
import datetime
import general as gen
#import uds_dummy as uds     #will have to be replaced with actual uds file while testing on board
import configure as conf
import os
from service28_subfunctionsettings import Service28Subfunc_CommType_EnDis_Window
import json



class Ui_Service28(Ui_Form_SID28):
    def redesign_ui(self):
        self.load_subfunction_visibility()
        self.update_control_and_communication_visibility()
        return
    
    def load_subfunction_visibility(self):
        """Load the visibility settings for Service 28 from the JSON file."""
        try:
            with open('service28_subfunctionsettings.json', 'r') as file:
                data = json.load(file)
                self.subfunction28_visibility = data["Service_28_Subfunctions_Visibility"]
                print("Loaded JSON:", self.subfunction28_visibility)  # Debugging line
        except FileNotFoundError:
            print("Error: service28_subfunctionsettings.json file not found.")
            self.subfunction28_visibility = {
                "Control_Types": {"00": True, "01": True, "02": True, "03": True, "04": True, "05": True},
                "Communication_Types": {"01": True, "02": True, "03": True}
            }  # Default visibility
        return

    def update_control_and_communication_visibility(self):
        """
        Update the visibility of each item in the combo boxes based on the loaded JSON data.
        """
        # Update Control_Type combo box
        for index in range(self.Control_Type.count() - 1, -1, -1):
            item_text = self.Control_Type.itemText(index)  # Get the text of the item (e.g., "00 - Enable Rx and Tx")
            
            # Extract the numeric part of the item text to match the JSON keys
            item_key = item_text.split(" ")[0]  # Get the part before the space (e.g., "00", "01")
            print(f"Checking visibility for Control Type: {item_key}")  # Debugging line
            
            # Check visibility; default to True if not found
            visibility = self.subfunction28_visibility["subfunctions"].get(item_key, True)
            print(f"Visibility for Control Type {item_key}: {visibility}")  # Debugging line
            
            if not visibility:
                self.Control_Type.removeItem(index)
                print(f"Control Type {item_key} hidden.")  # Debugging line
            else:
                print(f"Control Type {item_key} visible.")  # Debugging line

        # Update Communication_type combo box
        for index in range(self.Communication_type.count() - 1, -1, -1):
            item_text = self.Communication_type.itemText(index)  # Get the text of the item (e.g., "01 - Normal communication")
            
            # Extract the numeric part of the item text to match the JSON keys
            item_key = item_text.split(" ")[0]  # Get the part before the space (e.g., "01", "02")
            print(f"Checking visibility for Communication Type: {item_key}")  # Debugging line
            
            # Check visibility; default to True if not found
            visibility = self.subfunction28_visibility["communication_types"].get(item_key, True)
            print(f"Visibility for Communication Type {item_key}: {visibility}")  # Debugging line
            
            if not visibility:
                self.Communication_type.removeItem(index)
                print(f"Communication Type {item_key} hidden.")  # Debugging line
            else:
                print(f"Communication Type {item_key} visible.")  # Debugging line

        # Force updates to the combo boxes
        self.Control_Type.update()
        self.Communication_type.update()
        print("ComboBox update completed.")  # Debugging line
        return   
        
    def connectFunctions(self):
        self.pushButton_Send28Req.clicked.connect(self.send28service)
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
        self.Control_Type.setCurrentIndex(0)        
        self.Communication_type.setCurrentIndex(0)
        self.checkBox_suppressposmsg.setChecked(False)
        self.update_status("Userform cleared successfully")
        gen.log_action("Button Click", "Clear Form for Service 28 window clicked. Userfields cleared successfully.")
        return
    
    def addlog(self):
        #Add the uds transaction to the log file
        gen.log_udsreport(self.logentrystring)
        self.logentrystring = ""    #Clear the log entry so that if multiple tiomes the button is clicked continuously only one entry is made.
        self.update_status(f"Log file appended with the current UDS transaction (./reports/uds_log_report.txt)")
        gen.log_action("Button Click", "Add to Log button for Service 28 window clicked.")
        return
    
    def clearlog(self):
        gen.clearudslogfile()
        self.update_status(f"Log file cleared (./reports/uds_log_report.txt)")
        gen.log_action("Button Click", "Clear Log button for Service 28 window clicked.")
        return
    
    def send28service(self):
        index_Control_type = self.Control_Type.currentIndex()
        Control_type_name = self.Control_Type.itemText(index_Control_type).split("-")[-1].strip()
        #print(Control_type_name)
        Control_type = fun.get_subfunction(Control_type_name)
        #print(Control_type)
        #Control_type_name = fun.getsubfunction_name(Control_type)
        index_Communication_type = self.Communication_type.currentIndex()
        Comm_type_name = self.Communication_type.itemText(index_Communication_type).split("-")[-1].strip()
        #print(Comm_type_name)
        Comm_type = fun.get_communication_type(Comm_type_name)
        #Comm_type_name = fun.get_communication_type_name(Comm_type)
        sprmib_flg = self.checkBox_suppressposmsg.isChecked()
        #self.lineEdit_NIN.hide()
        #session should be a valid value and not zero
        #if(Control_type==4 or Control_type==5):
        #    self.lineEdit_NIN.show()

        #Get the service Request List for Diagnostic Session Control
 

        #Send the service request and get the response 
        if(sprmib_flg == False):
            IsPosResExpected = True 
        else:
            IsPosResExpected = False 

        ###############################################################
        if(Control_type_name=="Enable Rx and Disable Tx with Address Info" or Control_type_name=="Enable Rx and Tx  with Address Info"):
        
            nin_string = self.lineEdit_NIN.text().strip().replace(" ","").replace(" ","").replace(" ","")
        #gen.log_action("Button Click", f"Send 22 request button clicked with DID[{did_string}].")


            if(False == gen.check_2Bytehexadecimal(nin_string)):
                #Show messagebox with enter valid DID value
                self.update_status("Please enter a valid NIN value. It must be 2 byte in hexadecimal format")
                gen.log_action("UDS Request Fail", "28 Request not happened due to invalid NIN format")
                return 

            self.update_status("NIN is validated.")
            service_request = fun.form_reqmsg4srv28_withNIN(Control_type,Comm_type,nin_string,sprmib_flg)
            print(f"the service request is : {service_request}")
            #Get the service Request List for Read Data By Identifier
            #service_request = fun.form_reqmsg4srv28(nin_string)

            #Send the service request        
            response = uds.sendRequest(service_request, True)
            
            self.update_status("Service 28 request is sent")
            gen.log_action("UDS Request Success", f"28 Request Successfully sent : {' '.join(hex(number) for number in service_request)}")
            ##############################################################
                
            response = uds.sendRequest(service_request, IsPosResExpected)
            
            self.update_status("Service 28 request is sent")
            gen.log_action("UDS Request Success", f"28 Request Successfully sent : {' '.join(hex(number) for number in service_request)}")

            if(response.type == "Positive Response"):


                response_html = f'''<h4><U>Positive Response Recieved</U></h4>
        <p><strong>Service ID:</strong> <I>{hex(response.resp[0]-0x40)}</I></p>
        <p><strong>Control Type:</strong> <I>{hex(response.resp[1])} {Control_type_name} {Comm_type_name}</I></p>
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
    Explaination:   Communication control Requested for control type 0x{Control_type} and communication type 0x{Comm_type} and SPRMIB flag {sprmib_flg}
    UDS Response:   [{" ".join(hex(number) for number in response.resp)}]
    Explaination:   {response_text}<------------------- LOG ENTRY END ------------------->

    '''
            return
        elif(Control_type==0 or Control_type==1 or Control_type==2 or Control_type==3):
        
            service_request = fun.form_reqmsg4srv28_withoutNIN(Control_type,Comm_type,sprmib_flg)
                        #DID is valid  
            #self.update_status("NIN is validated.")
            #Get the service Request List for Read Data By Identifier
            #service_request = fun.form_reqmsg4srv28(nin_string)

            #Send the service request        
            response = uds.sendRequest(service_request, True)
            
            self.update_status("Service 28 request is sent")
            gen.log_action("UDS Request Success", f"28 Request Successfully sent : {' '.join(hex(number) for number in service_request)}")
            ##############################################################
                
            response = uds.sendRequest(service_request, IsPosResExpected)
            
            self.update_status("Service 28 request is sent")
            gen.log_action("UDS Request Success", f"28 Request Successfully sent : {' '.join(hex(number) for number in service_request)}")

            if(response.type == "Positive Response"):
                

                response_html = f'''<h4><U>Positive Response Recieved</U></h4>
        <p><strong>Service ID:</strong> <I>{hex(response.resp[0]-0x40)}</I></p>
        <p><strong>Control Type:</strong> <I>{hex(response.resp[1])} {Control_type_name} {Comm_type_name}</I></p>
        <p><strong>Info:</strong> <I> Service 28 is successfully sent with control type {Control_type_name} and communication type {Comm_type_name}</I></p>

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
    Explaination:   Communication control Requested for control type 0x{Control_type} and communication type 0x{Comm_type} 
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
    Form_SID28 = QtWidgets.QWidget()
    ui = Ui_Service28()
    ui.setupUi(Form_SID28)
    ui.redesign_ui()
    ui.connectFunctions()
    #Initializing the CAN
    #os.system(f'sudo ip link set {conf.can_channel} up type can bitrate {conf.baudrate} dbitrate {conf.datarate} restart-ms 1000 berr-reporting on fd on')

    #conf.tx = can.interface.Bus(channel=conf.can_channel, bustype='socketcan', fd=True)
    #conf.rx = can.interface.Bus(channel=conf.can_channel, bustype='socketcan', fd=True)

    Form_SID28.show()
    sys.exit(app.exec_())
