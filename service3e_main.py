from environment import *

if RUNNING_ON_RASPBERRYPI == False:
    import uds_dummy as uds  # will have to be replaced with actual uds file while testing on board
else:
    import uds
    import can

from service3e_base import Ui_Form_SID3E
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import service3e_functions as fun
from bs4 import BeautifulSoup
import os
import datetime
import general as gen
import configure as conf


class Ui_Service3E(Ui_Form_SID3E):
    def redesign_ui(self):
        pass

    def connectFunctions(self):
        self.pushButton_Send3EReq.clicked.connect(self.send3Eservice)
        self.pushButton_Stop3EReq.clicked.connect(self.stop_sending)
        self.pushButton_reset.clicked.connect(self.clearform)
        self.pushButton_appendLog.clicked.connect(self.addlog)
        self.pushButton_clearLog.clicked.connect(self.clearlog)
        return

    def update_status(self, msg):
        # Create a QMessageBox instance
        self.label_status.setText(msg)
        return

    def clearform(self):
        # Clears all the fields for entering new service request
        self.logentrystring = ""
        self.label_ResType.setText("No Response")
        self.textBrowser_Resp.clear()
        self.lineEdit_testerpresent_interval.clear()
        self.checkBox_suppressposmsg.setChecked(False)
        self.update_status("Userform cleared successfully")
        gen.log_action("Button Click", "Clear Form for Service 3E window clicked. Userfields cleared successfully.")
        return

    def addlog(self):
        # Add the uds transaction to the log file
        gen.log_udsreport(self.logentrystring)
        self.logentrystring = ""  # Clear the log entry so that if multiple times the button is clicked continuously, only one entry is made.
        self.update_status(f"Log file appended with the current UDS transaction (./reports/uds_log_report.txt)")
        gen.log_action("Button Click", "Add to Log button for Service 3E window clicked.")
        return

    def clearlog(self):
        gen.clearudslogfile()
        self.update_status(f"Log file cleared (./reports/uds_log_report.txt)")
        gen.log_action("Button Click", "Clear Log button for Service 3E window clicked.")
        return

    def send3Eservice(self):
        # Retrieve suppress positive response message flag
        sprmib_flg = self.checkBox_suppressposmsg.isChecked()
        try:
            # Parse the interval input and validate
            interval_text = self.lineEdit_testerpresent_interval.text().strip()
            interval = int(interval_text)

            # Ensure the interval is greater than 0
            if interval <= 0:
                raise ValueError("Interval must be greater than 0.")
        except ValueError:
            # Handle invalid input (non-numeric or <= 0)
            self.update_status("Please enter a valid positive integer for the tester present interval.")
            gen.log_action("UDS Request Fail", f"3E Request failed due to invalid tester present interval: [{self.lineEdit_testerpresent_interval.text().strip()}]")
            return

        # Send the service request and get the response
        if sprmib_flg == False:
            IsPosResExpected = True
        else:
            IsPosResExpected = False

        gen.IsAnyServiceActive = False
        self.start_timer(interval)  # Start the timer

    def send_periodic_requests(self):
        service_request = fun.form_reqmsg4srv3E(self.checkBox_suppressposmsg.isChecked())  # Move request generation here to ensure it's called each time

        # Check if service_request is None or empty (ensure it is valid)
        if not service_request:
            self.update_status("Failed to form service request.")
            gen.log_action("UDS Request Fail", "3E Request not formed correctly.")
            return

        gen.IsTesterPresentActive = True
        print(gen.IsTesterPresentActive)
        print(gen.IsAnyServiceActive)

        response = uds.sendRequest(service_request, not self.checkBox_suppressposmsg.isChecked())
        #from service3e_thread import run_check
        #run_check(self)  # Now call run_check with the current `self` (which is the `Ui_Service3E` instance)

        gen.IsAnyServiceActive = False  # Next response received, so make False
        gen.IsTesterPresentActive = False  # Set to False after receiving any response
        self.update_status("Service 3E request is sent")
        gen.log_action("UDS Request Success", f"3E Request Successfully sent: {' '.join(hex(number) for number in service_request)}")

        if response.type == "Positive Response":
            response_html = f'''<h4><U>Positive Response Received</U></h4>
            <p><strong>Service ID:</strong> <I>{hex(response.resp[0]-0x40)}</I></p>
            <p><strong>Subfunction:</strong> <I>{hex(response.resp[1])}</I></p>
            <p><strong>Suppress Positive Message Request:</strong> <I>{self.checkBox_suppressposmsg.isChecked()}</I></p>
            '''
        elif response.type == "Negative Response":
            response_html = f'''<h4><U>Negative Response Received</U></h4>    
            <p><strong>Suppress Positive Message Request:</strong> <I>{self.checkBox_suppressposmsg.isChecked()}</I></p>
            <p><strong>NRC Code:</strong> <I>{hex(response.nrc)}</I></p>
            <p><strong>NRC Name:</strong> <I>{response.nrcname}</I></p>
            <p><strong>NRC Desc:</strong> <I>{response.nrcdesc}</I></p>
            '''
        elif response.type == "Unknown Response Type":
            response_html = f'''<h4><U>Unidentified Response Received</U></h4>
                <p><strong>Response Bytes:</strong> <I>{" ".join(hex(number) for number in response.resp)}</I></p>
            '''
        elif response.type == "No Response":
            response_html = f'''<h4><U>No Response Received</U></h4>    
                <p><strong>Suppress Positive Message Request:</strong> <I>{self.checkBox_suppressposmsg.isChecked()}</I></p>
                <p><strong>Response Bytes:</strong> <I>{" ".join(hex(number) for number in response.resp)}</I></p>
            '''
        elif response.type == "Positive Response" and self.checkBox_suppressposmsg.isChecked():
            response_html = f'''<h4><U>Positive Response Received after a Response Pending (0x78)</U></h4>
                <p><strong>Service ID:</strong> <I>{hex(response.resp[0]-0x40)}</I></p>
                <p><strong>Subfunction:</strong> <I>{hex(response.resp[1])}</I></p>
                <p><strong>Positive Response Pending count:</strong> <I>{response.positiveResponsePending_count}</I></p>
                <p><strong>Suppress Positive Message Request:</strong> <I>{self.checkBox_suppressposmsg.isChecked()}</I></p>
            '''
        else:
            response_html = f'''<h4><U>ERROR OCCURRED</U></h4>'''

        # Update the response data on the user form
        self.label_ResType.setText(response.type)
        self.textBrowser_Resp.setHtml(response_html)

        current_user = os.getlogin()
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        soup = BeautifulSoup(response_html, 'html.parser')
        response_text = soup.get_text()

        self.logentrystring = f'''<---- LOG ENTRY [{current_user} - {current_time}] ---->
UDS Request :   [{" ".join(hex(number) for number in service_request)}]
Explanation:   Tester Present (Service 3E) Requested and SPRMIB flag {self.checkBox_suppressposmsg.isChecked()}
UDS Response:   [{" ".join(hex(number) for number in response.resp)}]
Explanation:   {response_text}
<------------------- LOG ENTRY END ------------------->

# '''
        gen.log_udsreport(self.logentrystring)
        self.logentrystring = ""  # Clear the log entry for the next iteration

    def start_timer(self, interval):
        if not hasattr(self, 'timer') or not self.timer.isActive():
            self.timer = QtCore.QTimer()
            self.timer.timeout.connect(self.send_periodic_requests)  # Now correctly connects to send_periodic_requests
            self.timer.start(interval * 1000)  # Start timer with given interval in seconds
            print(f"Timer started with interval: {interval} seconds.")
            self.update_status("Timer started.")
        else:
            print("Timer is already active.")

    def stop_timer(self):
        if hasattr(self, 'timer') and self.timer.isActive():
            self.timer.stop()
            print("Timer stopped.")
            self.update_status("Timer stopped.")
        else:
            print("Timer is not active.")

    def reset_timer(self, interval):
        print("Resetting timer...")
        self.stop_timer()
        self.start_timer(interval)
        print(f"Timer reset with interval: {interval} seconds.")
        self.update_status("Timer reset.")

    def stop_sending(self):
        # Stop sending requests
        self.stop_timer()  # Stop the timer
        gen.IsTesterPresentActive = False
        self.update_status("Periodic tester present request sending stopped.")
        gen.log_action("Button Click", "Stop Sending button clicked. Request sending stopped.")
        print("Request stopped.")
        return
    
    def monitor_service_active(self):
        previous_state = gen.IsAnyServiceActive
        while True:
            if gen.IsAnyServiceActive != previous_state:
                if gen.IsAnyServiceActive:
                    interval = int(self.lineEdit_testerpresent_interval.text().strip())
                    self.reset_timer(interval)
                else:
                    self.stop_timer()
                previous_state = gen.IsAnyServiceActive

    def closeEvent(self, event):
        if hasattr(self, 'timer'):
            self.timer.stop()  # Ensure the timer is stopped on window close
        if hasattr(self, 'monitor'):
            self.monitor.stop()  # Stop the TimerMonitor thread
        gen.IsTesterPresentActive = False
        gen.log_action(f"Window Close", f"Service 3E Window Closed.")
        event.accept()  # Make sure to accept the event to close the window

    def get_timer(self):
        return getattr(self, 'timer', None)  # Return the timer if it exists


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form_SID3E = QtWidgets.QWidget()
    ui = Ui_Service3E()
    ui.setupUi(Form_SID3E)
    ui.redesign_ui()
    ui.connectFunctions()

    # Initializing the CAN
    if RUNNING_ON_RASPBERRYPI == True:
        os.system(f'sudo ip link set {conf.can_channel} up type can bitrate {conf.baudrate} dbitrate {conf.datarate} restart-ms 1000 berr-reporting on fd on')
        conf.tx = can.interface.Bus(channel=conf.can_channel, bustype='socketcan', fd=True)
        conf.rx = can.interface.Bus(channel=conf.can_channel, bustype='socketcan', fd=True)

    Form_SID3E.show()
    #from service3e_thread import TimerMonitor
    #monitor = TimerMonitor(ui)
    #monitor.start()

    #from service3e_thread import start_monitoring
    #start_monitoring(ui) 

    monitoring_thread = QtCore.QThread()
    monitoring_thread.run = ui.monitor_service_active
    monitoring_thread.start()

    
    sys.exit(app.exec_())