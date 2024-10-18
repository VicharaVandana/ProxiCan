from mainwindow_base import Ui_MainWindow
from windowsettings import UDSservice_EnDis_Window
from logfile_selector import LogFileSelector
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow
import json

import mainfunctions as fun
import configure as conf
import general as gen

#Import service modules
import service22_main as rdbi
import service2e_main as wdbi
import service10_main as dsc
import service27_main as secuacc
import service11_main as er
import service85_main as cdtcs
import service28_main as commctr 

Is_CanConnected = False

#Create a child class of the mainwindow
class mainwindow(Ui_MainWindow, QtWidgets.QMainWindow, QtWidgets.QWidget):
    def redesign_ui(self):
        self.lbl_statusbar.setWordWrap(True)
        self.udsbuttons = []
        #Create the list of all uds services buttons
        self.udsbuttons.append(self.pushButton_10)
        self.udsbuttons.append(self.pushButton_22)
        self.udsbuttons.append(self.pushButton_2E)
        self.udsbuttons.append(self.pushButton_11)
        self.udsbuttons.append(self.pushButton_27)
        self.udsbuttons.append(self.pushButton_28)
        self.udsbuttons.append(self.pushButton_14)
        self.udsbuttons.append(self.pushButton_19)
        self.udsbuttons.append(self.pushButton_85)
        self.udsbuttons.append(self.pushButton_23)
        self.udsbuttons.append(self.pushButton_2A)
        self.udsbuttons.append(self.pushButton_2C)
        self.udsbuttons.append(self.pushButton_31)
        self.udsbuttons.append(self.pushButton_34)
        self.udsbuttons.append(self.pushButton_35)
        self.udsbuttons.append(self.pushButton_36)
        self.udsbuttons.append(self.pushButton_37)
        self.udsbuttons.append(self.pushButton_38)
        self.udsbuttons.append(self.pushButton_2F)
        self.udsbuttons.append(self.pushButton_86)
        self.udsbuttons.append(self.pushButton_83)
        #self.udsbuttons.append(self.pushButton_)
        #self.udsbuttons.clear()
        

        # Call the method to update button visibility based on JSON
        self.load_json()
        self.update_button_visibility() 
        self.rearrange_buttons()
        
        #Hide the functionality of elements till its functionality is implemented
        self.checkBox_EnableTesterPresent.hide()
        self.label_testerpresentinterval.hide()
        self.lineEdit_testerpresent_interval.hide()

        #Hide Data rate element untill CAN FD is selected
        self.label_datarate.hide()
        self.cmb_datarate.hide()

    def load_json(self):
        """Load the visibility settings from the JSON file"""
        try:
            with open('windowsettings.json', 'r') as file:
                data = json.load(file)
                self.uds_visibility = data["UDS_BUTTONS_VISIBILITY"]
        except FileNotFoundError:
            print("Error: windowssettings.json file not found.")
            sys.exit(1)
        
        return
    
    def update_button_visibility(self):
        """Show or hide buttons based on JSON values"""
        self.visible_buttons = []
        for button_name, visibility in self.uds_visibility.items():
            # Create the dynamic button name, e.g., 'pushButton_22'
            button_object_name = f"pushButton_{button_name}"

            # Use getattr to dynamically access the button object
            button_object = getattr(self, button_object_name, None)

            if button_object:
                # Show or hide the button based on the visibility value
                if visibility:
                    button_object.show()
                    button_object.setVisible(True)
                    self.visible_buttons.append(button_object)
                else:
                    button_object.hide()
                    button_object.setVisible(False)
        return
    
    
    def rearrange_buttons(self):
        """ Rearrange visible buttons within the existing grid layout """
        # Rearrange the buttons in the same grid positions (row, col)
        for idx, button in enumerate(self.visible_buttons):
            row = idx // 3  # Keeping 3 buttons per row
            col = idx % 3
            self.gridLayout_UDSserviceButtons.addWidget(button, row, col)

        # Ensure the layout is updated
        self.gridLayout_UDSserviceButtons.update()
        return
    
    def connectFunctions(self):

        #Connect Menu options 
        self.actionSettings.triggered.connect(self.open_settings)
        self.actionLog_Files_Location.triggered.connect(self.open_log_selector)

        #Connect and Disconnect buttons
        self.pushButton_connect.clicked.connect(self.connectcan)
        self.pushButton_disconnect.clicked.connect(self.disconnectcan)
        self.pushButton_exportconfig.clicked.connect(self.exportcanconfigfile)
        self.pushButton_importconfig.clicked.connect(self.importcanconfigfile)

        self.radiobtn_fdftype_can.clicked.connect(self.on_radiobutton_fdf_clicked)
        self.radiobtn_fdftype_canfd.clicked.connect(self.on_radiobutton_fdf_clicked)

        #Services Buttons
        self.pushButton_22.clicked.connect(self.openservice22)
        self.pushButton_2E.clicked.connect(self.openservice2E)
        self.pushButton_10.clicked.connect(self.openservice10)
        self.pushButton_27.clicked.connect(self.openservice27)
        self.pushButton_11.clicked.connect(self.openservice11)
        self.pushButton_85.clicked.connect(self.openservice85)
        self.pushButton_28.clicked.connect(self.openservice28)
        return
    
    def on_radiobutton_fdf_clicked(self):
        # Determine which radio button was clicked and execute code
        if self.radiobtn_fdftype_can.isChecked():
            # Data rate is not needed for CAN
            self.label_datarate.hide()
            self.cmb_datarate.hide()
        elif self.radiobtn_fdftype_canfd.isChecked():
            # Data rate is needed for CAN FD
            self.label_datarate.show()
            self.cmb_datarate.show()
        return
    
    def open_settings(self):
        self.udsservice_window = UDSservice_EnDis_Window()  # Create an instance of UDSservice_EnDis_Window
        self.udsservice_window.show()  # Show the window
        gen.log_action("Menu Option Click", "<UDS Service Settings> Option Selected")
        return
    
    def open_log_selector(self):
        # Create an instance of the LogFileSelector window and show it
        self.log_selector_window = LogFileSelector()
        self.log_selector_window.show()
        gen.log_action("Menu Option Click", "<Log File Location> Option Selected")
        return


    def openservice10(self):
        if(Is_CanConnected == True):
            self.window10 = QMainWindow()
            self.ui10 = dsc.Ui_Service10()
            self.ui10.setupUi(self.window10)
            self.ui10.redesign_ui()
            self.ui10.connectFunctions()
            self.window10.show()  # Display the new window
            self.update_status(f"10 Button clicked. Diagnostic Session Control service window opened")
            gen.log_action("Button Click", "Service 10 Window Opened")
        else:
            self.update_status(f"10 Button clicked. But unable to open the service window as CAN is not connected")
        return

    def openservice11(self):
        if(Is_CanConnected == True):
            self.window11 = QMainWindow()
            self.ui11 = er.Ui_Service11()
            self.ui11.setupUi(self.window11)
            self.ui11.redesign_ui()
            self.ui11.connectFunctions()
            self.window11.show()  # Display the new window
            self.update_status(f"11 Button clicked. ECU Reset service window opened")
            gen.log_action("Button Click", "Service 11 Window Opened")
        else:
            self.update_status(f"11 Button clicked. But unable to open the service window as CAN is not connected")
        return
        
    def openservice85(self):
        if(Is_CanConnected == True):
            self.window85 = QMainWindow()
            self.ui85 = cdtcs.Ui_Service85()
            self.ui85.setupUi(self.window85)
            self.ui85.redesign_ui()
            self.ui85.connectFunctions()
            self.window85.show()  #Display the new window
            self.update_status(f"85 Button clicked. Control DTC Settings service window opened")
            gen.log_action("Button Click", "Service 85 Window Opened")
        else:
            self.update_status(f"85 Button clicked. But unable to open the service window as CAN is not connected")
        return
    
    def openservice27(self):
        if(Is_CanConnected == True):
            self.window27 = QMainWindow()
            self.ui27 = secuacc.Ui_Service27()
            self.ui27.setupUi(self.window27)
            self.ui27.redesign_ui()
            self.ui27.connectFunctions()
            self.window27.show()  # Display the new window
            self.update_status(f"27 Button clicked. Security Access service window opened")
            gen.log_action("Button Click", "Service 27 Window Opened")
        else:
            self.update_status(f"27 Button clicked. But unable to open the service window as CAN is not connected")
        return
    
    def openservice22(self):
        if(Is_CanConnected == True):
            self.window22 = QMainWindow()
            self.ui22 = rdbi.Ui_Service22()
            self.ui22.setupUi(self.window22)
            self.ui22.redesign_ui()
            self.ui22.connectFunctions()
            self.window22.show()  # Display the new window
            self.update_status(f"22 Button clicked. Read Data By Identifier service window opened")
            gen.log_action("Button Click", "Service 22 Window Opened")
        else:
            self.update_status(f"22 Button clicked. But unable to open the service window as CAN is not connected")
        return
    
    def openservice2E(self):
        if(Is_CanConnected == True):
            self.window2E = QMainWindow()
            self.ui2E = wdbi.Ui_Service2E()
            self.ui2E.setupUi(self.window2E)
            self.ui2E.redesign_ui()
            self.ui2E.connectFunctions()
            self.window2E.show()  # Display the new window
            self.update_status(f"2E Button clicked. Write Data By Identifier service window opened")
            gen.log_action("Button Click", "Service 2E Window Opened")
        else:
            self.update_status(f"2E Button clicked. But unable to open the service window as CAN is not connected")
        return
    
    def openservice28(self):
        if(Is_CanConnected == True):
            self.window28 = QMainWindow()
            self.ui28 = commctr.Ui_Service28()
            self.ui28.setupUi(self.window28)
            self.ui28.redesign_ui()
            self.ui28.connectFunctions()
            self.window28.show() #Display the new window
            self.update_status(f"28 Button clicked. Communication control service window opened")
            gen.log_action("Button Click", "Service 28 Window Opened")
        else:
            self.update_status(f"28 Button clicked. But unable to open the service window as CAN is not connected")
        return
    
    def update_status(self, msg):
        # Create a QMessageBox instance
        self.lbl_statusbar.setText(f'''<html><head></head><body>
            <p>{msg}.</p>
            </body></html>''')
        return
    
    def importcanconfigfile(self):

        gen.log_action("Button Click", "Import pxi button clicked")

        # Step 1: Open a file dialog for selecting the .pxi file
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog

        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open Config File", "", "ProxiCan Config files (*.pxi)", options=options)

        # Step 2: If a file path is selected, read the file
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    # Step 3: Load JSON content from the file
                    data = json.load(file)
                
                # Step 4: Create a new CanConfig object and populate it with the data
                canconfig = fun.CanConfig()
                canconfig.ReqCanId = data.get('ReqCanId', None)
                canconfig.RespCanId = data.get('RespCanId', None)
                canconfig.channel = data.get('channel', None)
                canconfig.idtype = data.get('idtype', None)
                canconfig.bitrate = data.get('bitrate', None)
                canconfig.fdftype = data.get('fdftype', None)
                canconfig.brsrate = data.get('brsrate', None)
                canconfig.samplepoint = data.get('samplepoint', None)
                canconfig.FlowCtrlTimeout = data.get('FlowCtrlTimeout', 2)  # Default 2 seconds

                # Step 5: Update the UI fields with the loaded data
                self.cmb_CanChannel.setCurrentText(canconfig.channel)  # Set CAN channel

                # Set CAN Type (CAN/CANFD)
                if canconfig.fdftype == 'CAN':
                    self.radiobtn_fdftype_can.setChecked(True)
                    # Data rate is not needed for CAN
                    self.label_datarate.hide()
                    self.cmb_datarate.hide()
                    
                elif canconfig.fdftype == 'CANFD':
                    self.radiobtn_fdftype_canfd.setChecked(True)
                    self.label_datarate.show()
                    self.cmb_datarate.show()

                # Set CAN ID Type (STANDARD/EXTENDED)
                if canconfig.idtype == 'STANDARD':
                    self.radiobtn_idtype_standard.setChecked(True)
                elif canconfig.idtype == 'EXTENDED':
                    self.radiobtn_idtype_extended.setChecked(True)

                # Set Request and Response CAN IDs
                self.lineEdit_reqmsgid.setText(str(hex(canconfig.ReqCanId)).replace("0x",""))
                self.lineEdit_resmsgid.setText(str(hex(canconfig.RespCanId)).replace("0x",""))

                # Set baudrate
                if (canconfig.bitrate == 125000):
                    self.cmb_baudrate.setCurrentText("125kbps")
                elif (canconfig.bitrate == 250000):
                    self.cmb_baudrate.setCurrentText("250kbps")
                elif (canconfig.bitrate == 500000):
                    self.cmb_baudrate.setCurrentText("500kbps")
                elif (canconfig.bitrate == 1000000):
                    self.cmb_baudrate.setCurrentText("1mbps")
                else:
                    self.cmb_baudrate.setCurrentText("125kbps")

                # Set data rate
                if (canconfig.brsrate == 125000):
                    self.cmb_datarate.setCurrentText("125kbps")
                elif (canconfig.brsrate == 250000):
                    self.cmb_datarate.setCurrentText("250kbps")
                elif (canconfig.brsrate == 500000):
                    self.cmb_datarate.setCurrentText("500kbps")
                elif (canconfig.brsrate == 1000000):
                    self.cmb_datarate.setCurrentText("1mbps")
                elif (canconfig.brsrate == 2000000):
                    self.cmb_datarate.setCurrentText("2mbps")
                elif (canconfig.brsrate == 5000000):
                    self.cmb_datarate.setCurrentText("5mbps")
                else:
                    self.cmb_datarate.setCurrentText("125kbps")

                # Set sample point
                self.lineEdit_samplepoint.setText(str(canconfig.samplepoint))

                # Update status
                self.update_status(f"Config File {file_path} successfully imported.")
                self.file_path_label.setText(f"Config File imported from: {file_path}")
                gen.log_action("Config File Import Success", f"Config File Loaded successfully from: {file_path}")

            except Exception as e:
                QtWidgets.QMessageBox.critical(self, 'Error', f"Could not import config file: {e}")
        else:
            self.update_status('No file selected.')
            self.file_path_label.setText('No file selected.')
            gen.log_action("Config File Import Failed", f"Config File not loaded as the file path: [{file_path}] is invalid.")

        return True

    def exportcanconfigfile(self):
        result = fun.verifyandPopulateConfigFields(self)
        sts = result[1]
        gen.log_action("Button Click", "Export pxi button clicked")
        if (sts != "Success"):
            self.update_status(f"Export config Failed!! Config Field Error: {sts}")
            return False
        
        # If it reached here it means that all configuration fields are proper.
        canconfig = result[0]

        # Step 2: Open a file dialog for saving the file
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog

        # Open the save file dialog
        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save File", "", "ProxiCan Config files (*.pxi)", options=options)

        # Step 3: If a file path is selected, ensure the extension is correct
        if file_path:
            if not file_path.endswith('.pxi'):
                file_path += '.pxi'  # Append the .pxi extension if not provided

            try:
                # Write the data to the file in JSON format
                with open(file_path, 'w') as file:
                    file.write(canconfig.to_json())

                # Show the file path in the label
                self.file_path_label.setText(f"Config File saved at: {file_path}")
                gen.log_action("Config File Export Success", f"Config File saved at: {file_path}")

            except Exception as e:
                QtWidgets.QMessageBox.critical(self, 'Error', f"Could not save config file: {e}")
        else:
            self.file_path_label.setText('No file selected.')
            gen.log_action("Config File Export Failed", f"Config File not saved as the file path: [{file_path}] is invalid.")

        return True

    
    def connectcan(self):
        global Is_CanConnected
        result = fun.verifyandPopulateConfigFields(self)
        sts = result[1]
        gen.log_action("Button Click", "Connect CAN button clicked")
        if (sts != "Success"):
            self.update_status(f"Connect Failed!! Config Field Error: {sts}")
            self.label_connectionstatus.setStyleSheet("background-color: rgb(85, 85, 255);")
            Is_CanConnected = False
            return False
        #If it reached here it means that all configuration fields are proper.
        canconfig = result[0]
        res = conf.connectCAN(canconfig)
        if (res == True):
            #Since can is connected make the light green
            self.label_connectionstatus.setStyleSheet("background-color: rgb(20, 250, 10);")
            self.update_status(f"Connect Button Clicked: CAN Connect successful on channel {canconfig.channel}")
            gen.log_action(f"CAN Connection", f"CAN {canconfig.channel} connected with baudrate {canconfig.bitrate} and fdf type {canconfig.fdftype}")
            Is_CanConnected = True
            return True
        else:
            self.update_status(f"Connect Failed!! {res}")
            self.label_connectionstatus.setStyleSheet("background-color: rgb(85, 85, 255);")
            gen.log_action(f"CAN Connection", f"CAN {canconfig.channel} failed to connect with baudrate {canconfig.bitrate} and fdf type {canconfig.fdftype}")
            Is_CanConnected = False
            return False
        
    def disconnectcan(self):
        global Is_CanConnected
        gen.log_action("Button Click", "Disonnect CAN button clicked")
        conf.disconnectCAN()
        self.label_connectionstatus.setStyleSheet("background-color: rgb(250, 10, 10);")
        self.update_status(f"Disconnect Button Clicked: CAN Disconnected successfully")
        gen.log_action(f"CAN Connection", f"CAN disconnected successfully.")
        Is_CanConnected = False
        return
    







if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = mainwindow()
    ui.setupUi(MainWindow)
    ui.redesign_ui()
    ui.connectFunctions()
    #Clearing the log files
    gen.cleartp_log()
    gen.clearcantrafficlogfile()
    gen.clearActionfile()

    MainWindow.show()
    sys.exit(app.exec_())
