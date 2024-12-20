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

Is_SecurityLevelValid = False

class Ui_SecurityLevel_Settings(Ui_Form_SID27Settings, QtWidgets.QMainWindow):
    def redesign_ui(self):
        pass
    
    def connectFunctions(self):
        #Connecting the buttons
        self.pushButton_Reset.clicked.connect(self.clearform)
        self.pushButton_Delete.clicked.connect(self.delete_security_level)
        self.pushButton_ValidateSecuLvlConfig.clicked.connect(self.validateSecuLvlConfig)
        self.pushButton_AddSecuLvl.clicked.connect(self.add_security_level)
        self.pushButton_Update.clicked.connect(self.update_security_level)        
        

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
        #initially hide the Update and Delete and Validate Buttons and also Add Button
        self.pushButton_ValidateSecuLvlConfig.hide() 
        self.pushButton_Update.hide() 
        self.pushButton_Delete.hide() 
        self.pushButton_AddSecuLvl.hide() 
        return
    
    def update_status(self, msg):
        # Create a QMessageBox instance
        self.label_status.setText(msg)
        return
    
    def validateSecuLvlConfig(self):
        #Validate input fields
        global Is_SecurityLevelValid
        result = fun.validate_inputFields(self)
        Is_SecurityLevelValid = result[0]
        gen.log_action("Button Click", f"Validate Security level details clicked in Security Level Configurations window. Validation result : {Is_SecurityLevelValid}")
        if (Is_SecurityLevelValid == False):    #Invalid input fields
            self.update_status(result[1])
            self.pushButton_AddSecuLvl.hide()
            return
        else: #input fields are valid
            self.update_status("Input fields are validated.")
            if self.comboBox_SecurityLevel.currentIndex() == 0:
                self.pushButton_AddSecuLvl.show()      
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
    
    def update_security_level(self):
        '''Updates the existing security level configuration in the JSON file'''
        gen.log_action("Button Click", "Update Security Level for Service 27 in Security Level Configurations window clicked.")
        try:
            # Retrieve the security level ID from the comboBox
            selected_SecuLvl = self.comboBox_SecurityLevel.currentText()
            if not selected_SecuLvl:
                self.update_status("Security level ID cannot be empty for update operation.")
                gen.log_action("Update Function Failed", "Update Security Level for Service 27 Failed as security level name was empty.")
                return
            if selected_SecuLvl == "New_SecurityLevel":
                self.update_status("Security level ID cannot be 'New_SecurityLevel'. Select an existing security level to update.")
                gen.log_action("Update Function Failed", "Update Security Level for Service 27 Failed as no valid security level was selected.")
                return

            # Collect data from the form fields
            updated_subfunction_getseed = self.lineEdit_SubFn_Seed.text()
            updated_SecuLvl_ConfigData = {
                "subfunction_getseed": updated_subfunction_getseed,
                "subfunction_validatekey": self.lineEdit_SubFn_Key.text(),
                "seedLength": self.lineEdit_SeedLengthBytes.text(),
                "keyLength": self.lineEdit_KeyLengthBytes.text(),
                "SampleSeed": self.lineEdit_sampleseed.text(),
                "SampleKey": self.lineEdit_samplekey.text(),
                "SecurityFunction": self.lineEdit_SecurityFuncName.text(),
                "SecurityFunctionDefinition": self.textEdit_SecuFnDef.toPlainText(),
            }

            # Load existing JSON data
            try:
                with open(JSON_FILE_PATH, 'r') as SecuLvlCfgFile:
                    SecuLvl_ConfigDatas = json.load(SecuLvlCfgFile)

                    # Check if the security level exists
                    if selected_SecuLvl not in SecuLvl_ConfigDatas:
                        self.update_status(f"Security level '{selected_SecuLvl}' does not exist. Cannot update.")
                        gen.log_action("Update Function Failed", f"Security level '{selected_SecuLvl}' does not exist.")
                        return

                    # Check if subfunction_getseed is unique (excluding the current security level)
                    for secu_level, config_data in SecuLvl_ConfigDatas.items():
                        if secu_level != selected_SecuLvl and config_data.get("subfunction_getseed") == updated_subfunction_getseed:
                            self.update_status(f"The subfunction_getseed value '{updated_subfunction_getseed}' is already used by security level '{secu_level}'.")
                            gen.log_action("Update Function Failed", f"The subfunction_getseed value '{updated_subfunction_getseed}' is already used by security level '{secu_level}'.")
                            return

            except FileNotFoundError:
                self.update_status("Configuration file not found. Update operation failed.")
                gen.log_action("Update Function Failed", "Configuration file not found.")
                return
            except json.JSONDecodeError:
                self.update_status("Failed to decode JSON file. Check the file format.")
                gen.log_action("Update Function Failed", "JSONDecodeError: Invalid file format.")
                return

            # Update the security level data
            SecuLvl_ConfigDatas[selected_SecuLvl] = updated_SecuLvl_ConfigData

            # Write back to the JSON file
            with open(JSON_FILE_PATH, 'w') as SecuLvlCfgFile:
                json.dump(SecuLvl_ConfigDatas, SecuLvlCfgFile, indent=4)

            gen.log_action("Update Function Success", f"Security level '{selected_SecuLvl}' successfully updated.")
            self.update_status(f"Security level '{selected_SecuLvl}' successfully updated.")

        except ValueError as ve:
            self.update_status(f"Update Security Level - ValueError: {ve}")
            gen.log_action("Update Function Failed", f"ValueError: {ve}")
        except Exception as e:
            self.update_status(f"Update Security Level - Unexpected error: {e}")
            gen.log_action("Update Function Failed", f"Unexpected Error: {e}")
        return
    
    def add_security_level(self):
        '''Adds the current security level to the Json file'''
        gen.log_action("Button Click", "Add new Security Level for Service 27 in Security Level Configurations window clicked.")
        try:
            # Retrieve the security level ID from the comboBox
            selected_SecuLvl = self.comboBox_SecurityLevel.currentText()
            if not selected_SecuLvl:
                self.update_status("Security level ID cannot be empty for add operation.")
                gen.log_action("Add Function Failed", "Add new Security Level for Service 27 Failed as security level name was empty.")
                return
            if selected_SecuLvl == "New_SecurityLevel":
                self.update_status("Security level ID cannot be New_SecurityLevel. Change it to some other name.")
                gen.log_action("Add Function Failed", "Add new Security Level for Service 27 Failed as security level name not updated.")
                return

            # Collect data from the form fields
            new_SecuLvl_ConfigData = {
                "subfunction_getseed": self.lineEdit_SubFn_Seed.text(),
                "subfunction_validatekey": self.lineEdit_SubFn_Key.text(),
                "seedLength": self.lineEdit_SeedLengthBytes.text(),
                "keyLength": self.lineEdit_KeyLengthBytes.text(),
                "SampleSeed": self.lineEdit_sampleseed.text(),
                "SampleKey": self.lineEdit_samplekey.text(),
                "SecurityFunction": self.lineEdit_SecurityFuncName.text(),
                "SecurityFunctionDefinition": self.textEdit_SecuFnDef.toPlainText(),
            }

            # Load existing JSON data
            try:
                with open(JSON_FILE_PATH, 'r') as SecuLvlCfgFile:
                    SecuLvl_ConfigDatas = json.load(SecuLvlCfgFile)
                    #check if the security level and the get seed subfunction already exist
                    #If security level name already exists then it cannot be added again
                    # Check if the security level already exists
                    if selected_SecuLvl in SecuLvl_ConfigDatas:
                        self.update_status(f"Security level with name {selected_SecuLvl} already exists. Change the name to add new security level.")
                        gen.log_action("Add Function Failed", f"Add new Security Level for Service 27 Failed as security level name {selected_SecuLvl} given already exists.")
                        return
                    
                    # Check if subfunction_getseed is unique
                    new_subfunction_getseed = self.lineEdit_SubFn_Seed.text()
                    for secu_level, config_data in SecuLvl_ConfigDatas.items():
                        if config_data.get("subfunction_getseed") == new_subfunction_getseed: 
                            self.update_status(f"The subfunction_getseed value '{new_subfunction_getseed}' is already used by security level '{secu_level}'.")
                            gen.log_action("Add Function Failed", f"Add new Security Level for Service 27 Failed as the subfunction_getseed value '{new_subfunction_getseed}' is already used by security level '{secu_level}'.")
                            return
                            
            except FileNotFoundError:
                # Initialize if file doesn't exist
                SecuLvl_ConfigDatas = {}

            # Add or update the new security level in the JSON data
            SecuLvl_ConfigDatas[selected_SecuLvl] = new_SecuLvl_ConfigData

            # Write back to the JSON file
            with open(JSON_FILE_PATH, 'w') as SecuLvlCfgFile:
                json.dump(SecuLvl_ConfigDatas, SecuLvlCfgFile, indent=4)
            gen.log_action("Add Function Success", f"Add new Security Level for Service 27 Successful for security level: {selected_SecuLvl}.")
            self.update_status(f"Security level '{selected_SecuLvl}' successfully added.")

        except ValueError as ve:
            self.update_status(f"Add Security level - ValueError: {ve}")
        except json.JSONDecodeError:
            self.update_status("Add Security level - Error: Failed to decode JSON file. Check the file format.")
        except Exception as e:
            self.update_status(f"Add Security level - Unexpected error: {e}")
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
        inputwidgets = [
            self.lineEdit_SubFn_Seed,
            self.lineEdit_SubFn_Key,
            self.lineEdit_SeedLengthBytes,
            self.lineEdit_KeyLengthBytes,
            self.lineEdit_SecurityFuncName,
            self.lineEdit_sampleseed,
            self.lineEdit_samplekey,
            self.textEdit_SecuFnDef
        ]
        #Clear the colouring
        for widget in inputwidgets:
            widget.setStyleSheet(f"background-color: {fun.CLR_NOCHECK}; color: black;") 
            
        # Enable editing if "New_SecurityLevel" is selected, otherwise make it uneditable
        if selected_item == "New_SecurityLevel":
            self.comboBox_SecurityLevel.setEditable(True)
            # Hide the buttons "update" and "delete" and show "Validate" when new security level to be added. 
            # Hide "add" button also as it must be visible only after security level is validated
            self.pushButton_ValidateSecuLvlConfig.show() 
            self.pushButton_Update.hide() 
            self.pushButton_Delete.hide() 
            self.pushButton_AddSecuLvl.hide()
        else:
            self.comboBox_SecurityLevel.setEditable(False)
            # Show the buttons update and delete when existing security is selected. 
            # Hide add button as no new addition possible
            self.pushButton_ValidateSecuLvlConfig.show() 
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
