from environment import *

if RUNNING_ON_RASPBERRYPI == False:
    import uds_dummy as uds  # will have to be replaced with actual uds file while testing on board
else:
    import uds
    import can
from service34_main import Ui_Form_SID34
from service36_base import Ui_Ui_form_sid36
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QFileDialog
import service36_functions as fun
from bs4 import BeautifulSoup
import os
import datetime
import general as gen
import configure as conf
import os
import data_trans_variable as DTV


class Ui_Service36(Ui_Ui_form_sid36):
    def redesign_ui(self):
        pass

    def connectFunctions(self):
        self.pushButton_reset_2.clicked.connect(self.clearform)
        self.pushButton_appendLog_2.clicked.connect(self.addlog)
        self.pushButton_clearLog_2.clicked.connect(self.clearlog)
        return

    def update_status(self, msg):
        # Create a QMessageBox instance
        self.label_status.setText(msg)
        return

    def clearform(self):
        # Clears all the fields for entering new service request
        self.logentrystring = ""
        self.label_ResType_2.setText("No Response")
        self.textBrowser_Resp_2.clear()

        self.update_status("Userform cleared successfully")
        gen.log_action(
            "Button Click", "Clear Form for Service 36 window clicked. Userfields cleared successfully."
        )
        return

    def addlog(self):
        # Add the UDS transaction to the log file
        gen.log_udsreport(self.logentrystring)
        self.logentrystring = ""  # Clear the log entry so that if multiple times the button is clicked continuously, only one entry is made.
        self.update_status(
            f"Log file appended with the current UDS transaction (./reports/uds_log_report.txt)"
        )
        gen.log_action("Button Click", "Add to Log button for Service 36 window clicked.")
        return

    def clearlog(self):
        gen.clearudslogfile()
        self.update_status(f"Log file cleared (./reports/uds_log_report.txt)")
        gen.log_action("Button Click", "Clear Log button for Service 36 window clicked.")
        return

    def send36service(self, ex_data=None, blocksize_hex_values=None, blocks=None, decimal_blocksize=None):
        # Dynamically use provided parameters or fallback to global variables
        ex_data = DTV.ex_data
        blocksize_hex_values = DTV.blocksize_hex_values
        blocks = DTV.blocks
        decimal_blocksize = DTV.decimal_blocksize
        print(blocksize_hex_values)

        # Send the service request
        while blocks>1:
            for i in range(blocks):
                service_request = fun.first_data_transfer(ex_data, blocksize_hex_values, blocks, decimal_blocksize)
                response = uds.sendRequest(service_request)
                if(response.type)=="Positive Response":
                    for i in range(65):  #for 4096 bytes 65 consecutive frames has to be sent
                        service_request=fun.consecutive_data_transfer(ex_data, blocksize_hex_values, blocks, decimal_blocksize)
                        response=uds.sendRequest(service_request)
                        if(response.type)=="Positive Response":
                            blocks-=1
                            break


        # self.update_status("Service 36 request is sent")
        # gen.log_action(
        #     "UDS Request Success",
        #     f"36 Request Successfully sent : {' '.join(hex(number) for number in service_request)}",
        # )
        # print("SUCCESS")

        # Process the response

        return


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form_SID36 = QtWidgets.QWidget()
    ui = Ui_Service36()
    ui.setupUi(Form_SID36)
    ui.redesign_ui()
    ui.connectFunctions()

    Form_SID36.show()
    sys.exit(app.exec_())
