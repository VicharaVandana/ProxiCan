class abcd:
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
