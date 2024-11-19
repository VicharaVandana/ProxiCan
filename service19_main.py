from service19_base import Ui_Form_Subfun_SID19
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow
import json


import configure as conf
import general as gen

#Import service modules
import service19_01_main as RNODTCBSM
import service19_04_main as RDTCSSBDTC
import mainwindow as mw

Is_CanConnected = False

#Create a child class of the mainwindow
class Ui_Service19 (Ui_Form_Subfun_SID19, QtWidgets.QMainWindow, QtWidgets.QWidget):
    def redesign_ui(self):
        self.label_status.setWordWrap(True)
        self.subfunction19button = []
        #Create the list of all uds services buttons
        self.subfunction19button.append(self.pushButton_01)
        self.subfunction19button.append(self.pushButton_02)
        self.subfunction19button.append(self.pushButton_03)
        self.subfunction19button.append(self.pushButton_04)
        self.subfunction19button.append(self.pushButton_05)
        self.subfunction19button.append(self.pushButton_06)
        self.subfunction19button.append(self.pushButton_07)
        self.subfunction19button.append(self.pushButton_08)
        self.subfunction19button.append(self.pushButton_09)
        self.subfunction19button.append(self.pushButton_0A)
        self.subfunction19button.append(self.pushButton_0B)
        self.subfunction19button.append(self.pushButton_0C)
        self.subfunction19button.append(self.pushButton_0D)
        self.subfunction19button.append(self.pushButton_0E)
        self.subfunction19button.append(self.pushButton_0F)
        self.subfunction19button.append(self.pushButton_10)
        self.subfunction19button.append(self.pushButton_11)
        self.subfunction19button.append(self.pushButton_12)
        self.subfunction19button.append(self.pushButton_13)
        self.subfunction19button.append(self.pushButton_14)
        self.subfunction19button.append(self.pushButton_15)
        self.subfunction19button.append(self.pushButton_16)
        self.subfunction19button.append(self.pushButton_17)
        self.subfunction19button.append(self.pushButton_18)
        self.subfunction19button.append(self.pushButton_19)
        self.subfunction19button.append(self.pushButton_42)
        self.subfunction19button.append(self.pushButton_55)

        #self.udsbuttons.append(self.pushButton_)
        #self.udsbuttons.clear()
        

        # Call the method to update button visibility based on JSON
        self.load_json()
        self.update_button_visibility() 
        self.rearrange_buttons()
        
        

    def load_json(self):
        """Load the visibility settings from the JSON file"""
        try:
            with open('windowsettings.json', 'r') as file:
                data = json.load(file)
                self.subfunction19_visibility = data["Service_19_Subfunctions_Visibility"]
        except FileNotFoundError:
            print("Error: windowssettings.json file not found.")
            sys.exit(1)
        
        return
    
    def update_button_visibility(self):
        """Show or hide buttons based on JSON values"""
        self.visible_buttons = []
        for button_name, visibility in self.subfunction19_visibility.items():
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
            self.gridLayout.addWidget(button, row, col)

        # Ensure the layout is updated
        self.gridLayout.update()
        return
    
 
    
    def connectFunctions(self):
        #Service19 subfunction Buttons
        self.pushButton_01.clicked.connect(self.openservice19_01)
        self.pushButton_04.clicked.connect(self.openservice19_04)
        return
    


    def openservice19_01(self):
        if(Is_CanConnected == False):
            self.window19_01 = QMainWindow()
            self.ui19_01 = RNODTCBSM.Ui_Service19_01()
            self.ui19_01.setupUi(self.window19_01)
            self.ui19_01.redesign_ui()
            self.ui19_01.connectFunctions()
            self.window19_01.show()  # Display the new window
            self.update_status(f"19 subfunction 01 Button clicked. Report Number Of DTC By Status Mask subfunction window opened")
            gen.log_action("Button Click", "Service 19 subfunction 01 Window Opened")
        else:
            self.update_status(f"19 subfunction 01 Button clicked. But unable to open the service window as CAN is not connected")
        return

    def openservice19_04(self):
        if(Is_CanConnected == False):
            self.window19_04 = QMainWindow()
            self.ui19_04 = RDTCSSBDTC.Ui_Service19_04()
            self.ui19_04.setupUi(self.window19_04)
            self.ui19_04.redesign_ui()
            self.ui19_04.connectFunctions()
            self.window19_04.show()  # Display the new window
            self.update_status(f"19 subfunction 04 Button clicked. Report DTC Snapshot Record By DTC Number subfunction window opened")
            gen.log_action("Button Click", "Service 19 subfunction 04 Window Opened")
        else:
            self.update_status(f"19 subfunction 04 Button clicked. But unable to open the service window as CAN is not connected")
        return

    def update_status(self, msg):
        # Create a QMessageBox instance
        self.label_status.setText(f'''<html><head></head><body>
            <p>{msg}.</p>
            </body></html>''')
        return








if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow19 = QtWidgets.QMainWindow()
    ui = Ui_Service19()
    ui.setupUi(MainWindow19)
    ui.redesign_ui()
    ui.connectFunctions()
    #Clearing the log files
    gen.cleartp_log()
    gen.clearcantrafficlogfile()
    gen.clearActionfile()

    MainWindow19.show()
    sys.exit(app.exec_())
