from environment import *

if RUNNING_ON_RASPBERRYPI == False:
    import uds_dummy as uds     #will have to be replaced with actual uds file while testing on board
else:
    import uds
    import can
    
from service27_base import Ui_Form_SID27
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import service27_functions as fun
from securityaccesslogic import *
from bs4 import BeautifulSoup
import os
import datetime
import general as gen
import configure as conf
import os



class Ui_Service27(Ui_Form_SID27, QtWidgets.QMainWindow):
    def redesign_ui(self):
        pass 
    
    def connectFunctions(self):
        self.pushButton_Send27Req.clicked.connect(self.send27service)
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
        self.comboBox_SecurityLevel.setCurrentIndex(0)
        self.update_status("Userform cleared successfully")
        gen.log_action("Button Click", "Clear Form for Service 27 window clicked. Userfields cleared successfully.")
        return
    
    def addlog(self):
        #Add the uds transaction to the log file
        gen.log_udsreport(self.logentrystring)
        self.logentrystring = ""    #Clear the log entry so that if multiple tiomes the button is clicked continuously only one entry is made.
        self.update_status(f"Log file appended with the current UDS transaction (./reports/uds_log_report.txt)")
        gen.log_action("Button Click", "Add to Log button for Service 27 window clicked.")
        return
    
    def clearlog(self):
        gen.clearudslogfile()
        self.update_status(f"Log file cleared (./reports/uds_log_report.txt)")
        gen.log_action("Button Click", "Clear Log button for Service 27 window clicked.")
        return
    
    def send27service(self):
        index_SecurityLevel = self.comboBox_SecurityLevel.currentIndex()
        current_securitydetails = fun.getsecurityaccessdetails(index_SecurityLevel)

        #Request for Get Seed part of Security Access
        service_request_getseed = fun.form_reqmsg4srv27_getSeed(current_securitydetails["subfunction_getseed"])

        gen.IsAnyServiceActive = True   #Next request is triggered, so make True      
        while(gen.IsTesterPresentActive == True):
            self.update_status("WAIT!! Tester present (Service 3E) is currently ongoing")
            
        response_getseed = uds.sendRequest(service_request_getseed, True)
        gen.log_action("UDS Request Success", f"27 Request to get Seed Successfully sent : {' '.join(hex(number) for number in service_request_getseed)}")
        self.update_status("Service 27 request to Get Seed is sent")

        if(response_getseed.type == "Positive Response"):
            Is_ValidateKeyNeeded = True
            response_html = f'''<h4><U>Positive Response Recieved</U></h4>
    <p><strong>Service ID:</strong> <I>{hex(response_getseed.resp[0]-0x40)}</I></p>
    <p><strong>Sub Function [GET SEED]:</strong> <I>{hex(response_getseed.resp[1])}</I></p>
    <p><strong>Seed:</strong> <I>{" ".join(hex(number) for number in response_getseed.resp[2:])}</I></p>
'''
            seed = fun.bytes_to_number(response_getseed.resp[2:],'big')

        elif(response_getseed.type == "Negative Response"):
            Is_ValidateKeyNeeded = False
            response_type = response_getseed.type
            response_html = f'''<h4><U>Negative Response Recieved</U></h4>    
    <p><strong>NRC Code:</strong> <I>{hex(response_getseed.nrc)}</I></p>
    <p><strong>NRC Name:</strong> <I>{response_getseed.nrcname}</I></p>
    <p><strong>NRC Desc:</strong> <I>{response_getseed.nrcdesc}</I></p>
    <p><strong>Security Access:</strong> <I>DENIED</I></p>
'''
            
        elif(response_getseed.type == "Unknown Response Type"):
            Is_ValidateKeyNeeded = False
            response_type = response_getseed.type
            response_html = f'''<h4><U>Unidentified Response Recieved</U></h4>
    <p><strong>Response Bytes:</strong> <I>{" ".join(hex(number) for number in response_getseed.resp)}</I></p>
    <p><strong>Security Access:</strong> <I>DENIED</I></p>
'''
        elif(response_getseed.type == "No Response"):
            Is_ValidateKeyNeeded = False
            response_type = response_getseed.type
            response_html = f'''<h4><U>No Response Recieved</U></h4>    
    <p><strong>Response Bytes:</strong> <I>{" ".join(hex(number) for number in response_getseed.resp)}</I></p>
    <p><strong>Security Access:</strong> <I>DENIED</I></p>
'''
        else:
            Is_ValidateKeyNeeded = False
            response_type = "Error"
            response_html = f'''<h4><U>ERROR OCCURED</U></h4>
            <p><strong>Security Access:</strong> <I>DENIED</I></p>'''

        #Request for Validate Key part
        if(Is_ValidateKeyNeeded == True):
            #Compute the key from seed
            logicfunction = current_securitydetails["SecurityFunction"]
            #print(f"function is {logicfunction}. Seed is {seed} and key value is {globals()[logicfunction](seed)}")
            key = globals()[logicfunction](seed)

            #Request for Validate Key part of Security Access
            service_request_validatekey = fun.form_reqmsg4srv27_validateKey(current_securitydetails["subfunction_validatekey"], key, current_securitydetails["keyLength"])

            response_validatekey = uds.sendRequest(service_request_validatekey, True)
            gen.log_action("UDS Request Success", f"27 Request to Validate Key Successfully sent : {' '.join(hex(number) for number in service_request_validatekey)}")
            self.update_status("Service 27 request to Validate Key is sent")

            if(response_validatekey.type == "Positive Response"):
                response_type = response_validatekey.type
                response_html = f'''{response_html}
        <p><strong>Sub Function [VALIDATE KEY]:</strong> <I>{hex(response_validatekey.resp[1])}</I></p>
        <p><strong>Key:</strong> <I>{" ".join(hex(number) for number in service_request_validatekey[2:])}</I></p>
        <p><strong>Security Access:</strong> <I>GRANTED</I></p>
    '''

            elif(response_validatekey.type == "Negative Response"):
                response_type = response_validatekey.type
                response_html = f'''<h4><U>Negative Response Recieved</U></h4>    
        <p><strong>NRC Code:</strong> <I>{hex(response_validatekey.nrc)}</I></p>
        <p><strong>NRC Name:</strong> <I>{response_validatekey.nrcname}</I></p>
        <p><strong>NRC Desc:</strong> <I>{response_validatekey.nrcdesc}</I></p>
        <p><strong>Note:</strong> <I>Security Access Request of Get Seed functionality was successful.</I></p>
        <p><strong>Security Access:</strong> <I>DENIED</I></p>
    '''
                
            elif(response_validatekey.type == "Unknown Response Type"):
                response_type = response_validatekey.type
                response_html = f'''<h4><U>Unidentified Response Recieved</U></h4>
        <p><strong>Response Bytes:</strong> <I>{" ".join(hex(number) for number in response_validatekey.resp)}</I></p>
        <p><strong>Note:</strong> <I>Security Access Request of Get Seed functionality was successful.</I></p>
        <p><strong>Security Access:</strong> <I>DENIED</I></p>
    '''
            elif(response_validatekey.type == "No Response"):
                response_type = response_validatekey.type
                response_html = f'''<h4><U>No Response Recieved</U></h4>    
        <p><strong>Response Bytes:</strong> <I>{" ".join(hex(number) for number in response_validatekey.resp)}</I></p>
        <p><strong>Note:</strong> <I>Security Access Request of Get Seed functionality was successful.</I></p>
        <p><strong>Security Access:</strong> <I>DENIED</I></p>
    '''
            else:
                response_type = "Error"
                response_html = f'''<h4><U>ERROR OCCURED</U></h4>
                <p><strong>Security Access:</strong> <I>DENIED</I></p>'''

        #Request Response complete 
        gen.IsAnyServiceActive = False   #Next response recieved , so make False

        #Update the response data on userform
        self.label_ResType.setText(response_type)
        self.textBrowser_Resp.setHtml(response_html)

        current_user = os.getlogin()
        currenttime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        soup = BeautifulSoup(response_html, 'html.parser')
        response_text = soup.get_text()

        self.logentrystring = f'''<---- LOG ENTRY [{current_user} - {currenttime}] ---->
UDS Request for Get Seed :   [{" ".join(hex(number) for number in service_request_getseed)}]
Explaination:   Security Access (Service 27) Requested to Get seed value for Security Level {(current_securitydetails["subfunction_validatekey"]//2)} - Subfunctions {hex(current_securitydetails["subfunction_getseed"])}_{hex(current_securitydetails["subfunction_validatekey"])}
UDS Response for Get Seed:   [{" ".join(hex(number) for number in response_getseed.resp)}]'''
        if(Is_ValidateKeyNeeded == True):
            self.logentrystring = f'''{self.logentrystring}
UDS Get Seed Successful. The Seed Recieved is: {hex(seed)}. The Key computed internally is {hex(key)}
UDS Request for Validate Key :   [{" ".join(hex(number) for number in service_request_validatekey)}]
Explaination:   Security Access (Service 27) Requested to validate Key computed for Security Level {(current_securitydetails["subfunction_validatekey"]//2)} - Subfunctions {hex(current_securitydetails["subfunction_getseed"])}_{hex(current_securitydetails["subfunction_validatekey"])}
UDS Response for Validate Key:   [{" ".join(hex(number) for number in response_validatekey.resp)}]'''

        self.logentrystring = f'''{self.logentrystring}
Explaination:   {response_text}<------------------- LOG ENTRY END ------------------->

'''
        return

    def closeEvent(self, event):
        # Custom logic when the window is closed
        gen.log_action(f"Window Close", f"Service 27 Window Closed.")
        return    
        
        

    



if __name__ == "__main__":
    import sys
    #current_user = os.getlogin()
    #currenttime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #print(f"<---- LOG ENTRY [{current_user} - {currenttime}] ---->")
    app = QtWidgets.QApplication(sys.argv)
    Form_SID27 = QtWidgets.QWidget()
    ui = Ui_Service27()
    ui.setupUi(Form_SID27)
    ui.redesign_ui()
    ui.connectFunctions()
    
    #Initializing the CAN
    if RUNNING_ON_RASPBERRYPI == True:
        os.system(f'sudo ip link set {conf.can_channel} up type can bitrate {conf.baudrate} dbitrate {conf.datarate} restart-ms 1000 berr-reporting on fd on')
        conf.tx = can.interface.Bus(channel=conf.can_channel, bustype='socketcan', fd=True)
        conf.rx = can.interface.Bus(channel=conf.can_channel, bustype='socketcan', fd=True)

    Form_SID27.show()
    sys.exit(app.exec_())