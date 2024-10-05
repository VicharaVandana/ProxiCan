from service27_base import Ui_Form_SID27
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import service27_functions as fun
from bs4 import BeautifulSoup
import os
import datetime
import general as gen
import uds_dummy as uds     #will have to be replaced with actual uds file while testing on board
#pc#import uds
import configure as conf
import os
#pc#import can


class Ui_Service27(Ui_Form_SID27):
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
        pass
    



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
    #os.system(f'sudo ip link set {conf.can_channel} up type can bitrate {conf.baudrate} dbitrate {conf.datarate} restart-ms 1000 berr-reporting on fd on')

    #conf.tx = can.interface.Bus(channel=conf.can_channel, bustype='socketcan', fd=True)
    #conf.rx = can.interface.Bus(channel=conf.can_channel, bustype='socketcan', fd=True)

    Form_SID27.show()
    sys.exit(app.exec_())