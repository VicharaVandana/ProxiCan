from PyQt5 import QtGui, QtWidgets
import json
import re
from PyQt5.QtWidgets import QMessageBox
import SecurityLevelConfigSettings_fun as fun
from SecurityLevelConfigSettings_base import Ui_Form_SID27Settings
import general as gen

SECURITY_FUNCDEF_TEMPLATE = """def SecurityFunction(seed):
    # Logic to compute key from seed in python
    # START OF LOGIC 
    #Enter your python code here
    key = seed  #to be replaced with actual logic
    # END OF LOGIC
    return key
"""
JSON_FILE_PATH = "securityLvl_config.json"

class Ui_SecurityLevel_Settings(Ui_Form_SID27Settings, QtWidgets.QMainWindow):
    def redesign_ui(self):
        pass
    
    def connectFunctions(self):
        #Connecting the buttons
        self.pushButton_Reset.clicked.connect(self.clearform)
        self.pushButton_Delete.clicked.connect(self.delete_security_level)
        

        #Connecting the other signals
        self.lineEdit_SecurityFuncName.editingFinished.connect(self.update_secufuncname_infuncdef)
        self.comboBox_SecurityLevel.currentIndexChanged.connect(self.on_SecurityLevel_change)
        return
    
    def initialise_ui(self):
        #FOR Security Level combobox
        #load the configurations from json
        with open(JSON_FILE_PATH, 'r') as SecuLvlCfgFile:
            SecuLvl_ConfigDatas = json.load(SecuLvlCfgFile)
        
        # Clear the combobox
        self.comboBox_SecurityLevel.clear()

        # Populate the combobox with keys from the parsed JSON
        for key in SecuLvl_ConfigDatas.keys():
            if(key != ""):
                self.comboBox_SecurityLevel.addItem(key)
        
        self.comboBox_SecurityLevel.setCurrentIndex(-1)         #Deselect all the items
        self.comboBox_SecurityLevel.setEditable(False)       # Set combobox as uneditable by default

        #FOR Security Level Logic Function definition
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(6)
        self.textEdit_SecuFnDef.clear() 
        self.textEdit_SecuFnDef.setFont(font)     
        self.textEdit_SecuFnDef.setStyleSheet("background-color: white; color: black;")        
        #self.textEdit_SecuFnDef.setPlainText(SECURITY_FUNCDEF_TEMPLATE)

        #FOR the Buttons
        #initially hide the Update and Delete Buttons and also Add Button
        self.pushButton_Update.hide() 
        self.pushButton_Delete.hide() 
        self.pushButton_AddSecuLvl.hide() 
        return
    
    def update_status(self, msg):
        # Create a QMessageBox instance
        self.label_status.setText(msg)
        return
    
    def fetchSecuLvlCfgstoGUI(self, selected_SecuLvl):
        #load the configurations from json and get config data of security level selected
        with open(JSON_FILE_PATH, 'r') as SecuLvlCfgFile:
            SecuLvl_ConfigDatas = json.load(SecuLvlCfgFile)
            SecuLvl_ConfigData = SecuLvl_ConfigDatas[selected_SecuLvl]
        #update the fields with configuration data
        self.lineEdit_SubFn_Seed.setText(SecuLvl_ConfigData["subfunction_getseed"])
        self.lineEdit_SubFn_Key.setText(SecuLvl_ConfigData["subfunction_validatekey"])
        self.lineEdit_SeedLengthBytes.setText(SecuLvl_ConfigData["seedLength"])
        self.lineEdit_KeyLengthBytes.setText(SecuLvl_ConfigData["keyLength"])
        self.lineEdit_SecurityFuncName.setText(SecuLvl_ConfigData["SecurityFunction"])
        self.lineEdit_sampleseed.setText(SecuLvl_ConfigData["SampleSeed"])
        self.lineEdit_samplekey.setText(SecuLvl_ConfigData["SampleKey"])
        self.textEdit_SecuFnDef.setPlainText(SecuLvl_ConfigData["SecurityFunctionDefinition"])
        return
    
    def delete_security_level(self):
        """Prompts the user for confirmation and deletes the selected security level."""
        selected_level = self.comboBox_SecurityLevel.currentText()

        if not selected_level:
            QMessageBox.warning(self, "Warning", "No security level selected!")
            return

        # Confirmation dialog
        reply = QMessageBox.question(
            self, "Confirm Delete Security Level",
            f"Are you sure you want to delete Security Level: '{selected_level}' from configurations?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            # Remove the selected level from data
            with open(JSON_FILE_PATH, 'r') as SecuLvlCfgFile_r:
                SecuLvl_ConfigDatas = json.load(SecuLvlCfgFile_r)

            del SecuLvl_ConfigDatas[selected_level]

            with open(JSON_FILE_PATH, "w") as SecuLvlCfgFile_w:
                json.dump(SecuLvl_ConfigDatas, SecuLvlCfgFile_w, indent=4)

            # Update the combo box
            self.clearform()
            return
    
    def clearform(self):
        #Clears all the fields for entering new service request
        self.initialise_ui()

        self.lineEdit_SubFn_Seed.clear()
        self.lineEdit_SubFn_Seed.setStyleSheet("background-color: white;")
        
        self.lineEdit_SeedLengthBytes.clear()
        self.lineEdit_SeedLengthBytes.setStyleSheet("background-color: white;")

        self.lineEdit_SubFn_Key.clear()
        self.lineEdit_SubFn_Key.setStyleSheet("background-color: white;")

        self.lineEdit_KeyLengthBytes.clear()
        self.lineEdit_KeyLengthBytes.setStyleSheet("background-color: white;")

        self.lineEdit_SecurityFuncName.clear()
        self.lineEdit_SecurityFuncName.setStyleSheet("background-color: white;")

        self.lineEdit_sampleseed.clear()
        self.lineEdit_sampleseed.setStyleSheet("background-color: white;")

        self.lineEdit_samplekey.clear()
        self.lineEdit_samplekey.setStyleSheet("background-color: white;")
        
        self.update_status("Userform cleared successfully")
        gen.log_action("Button Click", "Clear Form for Service 27 Security Level Configurations window clicked. Userfields cleared successfully.")
        return
    
    def update_secufuncname_infuncdef(self):
        #get the current content of the function definition
        newFuncName = self.lineEdit_SecurityFuncName.text().strip() 

        #get the new security function name
        current_funcDef = self.textEdit_SecuFnDef.toPlainText()
        if (current_funcDef.strip() == ""):
            current_funcDef = SECURITY_FUNCDEF_TEMPLATE

        #fetch the string which has to be replaced and replace and compute new function definition
        pattern = r"(def\s+)(\w+)(\s*\(seed\))" # Regular expression to find the function definition
        # Search for the pattern in the code string
        match = re.search(pattern, current_funcDef)
        if match:
            # Extract the function name (second capture group)
            oldFuncName = match.group(2)
        else:
            oldFuncName = "SecurityFunction"
        
        if (newFuncName == ""):
            newFuncName = "SecurityFunction"
            self.update_status("No Security function name provided. Default name updated in definition.")
        elif (newFuncName.isalnum() == False):
            newFuncName = oldFuncName
            self.lineEdit_SecurityFuncName.setText(newFuncName)
            self.update_status("New Function name is not valid. so old name retained.")
        else:
            self.update_status("New Security function name provided. updated in definition as well.")

        new_funcDef = re.sub(pattern, r"\1" + newFuncName + r"\3", current_funcDef)        

        #write the string into function definition text edit
        self.textEdit_SecuFnDef.clear() 
        self.textEdit_SecuFnDef.setStyleSheet("background-color: white; color: black;")        
        self.textEdit_SecuFnDef.setPlainText(new_funcDef)
        self.textEdit_SecuFnDef.clearFocus()
        return
    
    def on_SecurityLevel_change(self, index):
        selected_item = self.comboBox_SecurityLevel.currentText()
        self.fetchSecuLvlCfgstoGUI(selected_item)
        
        # Enable editing if "New_SecurityLevel" is selected, otherwise make it uneditable
        if selected_item == "New_SecurityLevel":
            self.comboBox_SecurityLevel.setEditable(True)
            # Hide the buttons "update" and "delete" when new security level to be added. 
            # Hide "add" button also as it must be visible only after security level is validated
            self.pushButton_Update.hide() 
            self.pushButton_Delete.hide() 
            self.pushButton_AddSecuLvl.hide()
        else:
            self.comboBox_SecurityLevel.setEditable(False)
            # Show the buttons update and delete when existing security is selected. 
            # Hide add button as no new addition possible
            self.pushButton_Update.show() 
            self.pushButton_Delete.show() 
            self.pushButton_AddSecuLvl.hide()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form_SecuLvConfig = QtWidgets.QWidget()
    ui = Ui_SecurityLevel_Settings()
    ui.setupUi(Form_SecuLvConfig)
    ui.redesign_ui()
    ui.connectFunctions()
    ui.initialise_ui()

    Form_SecuLvConfig.show()
    sys.exit(app.exec_())
