import general as gen

CLR_NOCHECK = "white"
CLR_INVALID = "lightpink"
CLR_VALID = "lightgreen"

def validate_inputFields(uf):
    Is_InputFieldsValid = True #Initially assume the fields are valid
    errormsg = ""

    # Get Seed Subfunction field 
    # It must not be empty and should have a one byte hexadecimal value and an odd number
    str_getSeedSF = uf.lineEdit_SubFn_Seed.text().strip() 
    if(str_getSeedSF == ""):    #empty field
        Is_getSeedSF_valid = False
        errormsg = f"{errormsg}<Get Seed SubFn> field cannot be empty. "
        uf.lineEdit_SubFn_Seed.setStyleSheet(f"background-color: {CLR_INVALID};")
    elif (gen.check_nBytehexadecimal(str_getSeedSF,1) == False): #not one byte hexadecimal number
        Is_getSeedSF_valid = False
        errormsg = f"{errormsg}<Get Seed SubFn> must contain 1 byte hexadecimal value. "
        uf.lineEdit_SubFn_Seed.setStyleSheet(f"background-color: {CLR_INVALID};")
    else:
        val_getSeedSF = gen.is_valid_hex(str_getSeedSF,0,0xFF)
        if(val_getSeedSF % 2 == 0): #get seed subfunction cannot be even number
            Is_getSeedSF_valid = False
            errormsg = f"{errormsg}<Get Seed SubFn> must be a odd number. "
            uf.lineEdit_SubFn_Seed.setStyleSheet(f"background-color: {CLR_INVALID};")
        else:
            uf.lineEdit_SubFn_Seed.setStyleSheet(f"background-color: {CLR_VALID};")
            Is_getSeedSF_valid = True
    
    # Validate Key Subfunction field 
    # It must not be empty and should have a one byte hexadecimal value and an even number and must be one more than get seed subfunction
    str_validateKeySF = uf.lineEdit_SubFn_Key.text().strip() 
    if(str_validateKeySF == ""):    #empty field
        Is_validateKeySF_valid = False
        errormsg = f"{errormsg}<Validate Key SubFn> field cannot be empty. "
        uf.lineEdit_SubFn_Key.setStyleSheet(f"background-color: {CLR_INVALID};")
    elif (gen.check_nBytehexadecimal(str_validateKeySF,1) == False): #not one byte hexadecimal number
        Is_validateKeySF_valid = False
        errormsg = f"{errormsg}<Validate Key SubFn> must contain 1 byte hexadecimal value. "
        uf.lineEdit_SubFn_Key.setStyleSheet(f"background-color: {CLR_INVALID};")
    else:
        val_validateKeyF = gen.is_valid_hex(str_validateKeySF,0,0xFF)
        if((val_validateKeyF % 2 == 1) or (val_validateKeyF == 0)): #validate key subfunction cannot be odd number
            Is_validateKeySF_valid = False
            errormsg = f"{errormsg}<Validate Key SubFn> must be a non zero even number. "
            uf.lineEdit_SubFn_Key.setStyleSheet(f"background-color: {CLR_INVALID};")
        elif((Is_getSeedSF_valid == True) and (val_validateKeyF - val_getSeedSF != 1)): 
            Is_validateKeySF_valid = False
            errormsg = f"{errormsg}<Validate Key SubFn> must be a one value more than <Get Seed SubFn>. "
            uf.lineEdit_SubFn_Key.setStyleSheet(f"background-color: {CLR_INVALID};")
        else:
            uf.lineEdit_SubFn_Key.setStyleSheet(f"background-color: {CLR_VALID};")
            Is_validateKeySF_valid = True

    # Validate Seed Length field 
    # It must not be empty and should have a numerical value
    str_seedLength = uf.lineEdit_SeedLengthBytes.text().strip()
    if(str_seedLength == ""):    #empty field
        Is_SeedLength_valid = False
        errormsg = f"{errormsg}<Seed Length> field cannot be empty. "
        uf.lineEdit_SeedLengthBytes.setStyleSheet(f"background-color: {CLR_INVALID};")
    elif(gen.is_positive_integer(str_seedLength) == False):
        Is_SeedLength_valid = False
        errormsg = f"{errormsg}<Seed Length> must be a positive integer. "
        uf.lineEdit_SeedLengthBytes.setStyleSheet(f"background-color: {CLR_INVALID};")
    else:
        uf.lineEdit_SeedLengthBytes.setStyleSheet(f"background-color: {CLR_VALID};")
        seedLength = int(str_seedLength)
        Is_SeedLength_valid = True

    # Validate Key Length field 
    # It must not be empty and should have a numerical value
    str_keyLength = uf.lineEdit_KeyLengthBytes.text().strip()
    if(str_keyLength == ""):    #empty field
        Is_KeyLength_valid = False
        errormsg = f"{errormsg}<Key Length> field cannot be empty. "
        uf.lineEdit_KeyLengthBytes.setStyleSheet(f"background-color: {CLR_INVALID};")
    elif(gen.is_positive_integer(str_keyLength) == False):
        Is_KeyLength_valid = False
        errormsg = f"{errormsg}<Key Length> must be a positive integer. "
        uf.lineEdit_KeyLengthBytes.setStyleSheet(f"background-color: {CLR_INVALID};")
    else:
        uf.lineEdit_KeyLengthBytes.setStyleSheet(f"background-color: {CLR_VALID};")
        keyLength = int(str_keyLength)
        Is_KeyLength_valid = True

    # Validate Sample Seed Value field 
    # It must not be empty and should have hexadecimal number of length mentioned in seed length
    str_sampleSeed = uf.lineEdit_sampleseed.text().strip()
    if(str_sampleSeed == ""):    #empty field
        Is_sampleSeed_valid = False
        errormsg = f"{errormsg}<Sample Seed Val> field cannot be empty. "
        uf.lineEdit_sampleseed.setStyleSheet(f"background-color: {CLR_INVALID};")
    elif(gen.check_nBytehexadecimal(str_sampleSeed,seedLength) == False):
        Is_sampleSeed_valid = False
        errormsg = f"{errormsg}<Sample Seed Val> must contain {seedLength} byte hexadecimal value.  "
        uf.lineEdit_sampleseed.setStyleSheet(f"background-color: {CLR_INVALID};")
    else:
        uf.lineEdit_sampleseed.setStyleSheet(f"background-color: {CLR_VALID};")
        sample_seed = int(str_sampleSeed,16)
        Is_sampleSeed_valid = True

    # Validate Sample Key Value field 
    # It must not be empty and should have hexadecimal number of length mentioned in Key length
    str_sampleKey = uf.lineEdit_samplekey.text().strip()
    if(str_sampleKey == ""):    #empty field
        Is_sampleKey_valid = False
        errormsg = f"{errormsg}<Sample Key Val> field cannot be empty. "
        uf.lineEdit_samplekey.setStyleSheet(f"background-color: {CLR_INVALID};")
    elif(gen.check_nBytehexadecimal(str_sampleKey,keyLength) == False):
        Is_sampleKey_valid = False
        errormsg = f"{errormsg}<Sample Key Val> must contain {keyLength} byte hexadecimal value.  "
        uf.lineEdit_samplekey.setStyleSheet(f"background-color: {CLR_INVALID};")
    else:
        uf.lineEdit_samplekey.setStyleSheet(f"background-color: {CLR_VALID};")
        sample_key = int(str_sampleKey,16)
        Is_sampleKey_valid = True

    # Validate Security Function Name field 
    # It must not be empty 
    str_securityFunction = uf.lineEdit_SecurityFuncName.text().strip()
    if(str_securityFunction == ""):    #empty field
        Is_secuFuncName_valid = False
        errormsg = f"{errormsg}<Security Function Name> field cannot be empty. "
        uf.lineEdit_SecurityFuncName.setStyleSheet(f"background-color: {CLR_INVALID};")
    else:
        uf.lineEdit_SecurityFuncName.setStyleSheet(f"background-color: {CLR_VALID};")
        Is_secuFuncName_valid = True

    # Validate Function Definition field 
    # It must not be empty and should be a python function and logic must be proper for given sample seed and sample key
    str_function_code = uf.textEdit_SecuFnDef.toPlainText().strip()
    if(str_function_code == ""):    #empty field
        Is_FunctionDef_valid = False
        errormsg = f"{errormsg}<Function Definition> field cannot be empty. "
        uf.textEdit_SecuFnDef.setStyleSheet(f"background-color: {CLR_INVALID};")
    else:
        #Check for valid python code
        try:
            # Attempt to execute the string as Python code
            exec(str_function_code)
            
            # Call the function dynamically using eval
            seed = sample_seed  # Example seed value
            key = eval(str_securityFunction)(seed)
            if(key == sample_key):
            #print(f"Seed: {hex(seed)}, Key: {hex(key)}")
                uf.textEdit_SecuFnDef.setStyleSheet(f"background-color: {CLR_VALID};")
                Is_FunctionDef_valid = True
            else:
                errormsg = f"{errormsg}<Function Definition> As per the current logic the Sample key[{hex(sample_key)}] doesnt match the Key computed[{hex(key)}] from sample seed[{hex(seed)}]. "
                uf.textEdit_SecuFnDef.setStyleSheet(f"background-color: {CLR_INVALID};")
                Is_FunctionDef_valid = False

        except SyntaxError as e:    #Function definition is not valid
            #print(f"Syntax Error in code: {e}")
            errormsg = f"{errormsg}<Function Definition> Syntax Error in code: {e}. "
            uf.textEdit_SecuFnDef.setStyleSheet(f"background-color: {CLR_INVALID};")
            Is_FunctionDef_valid = False
        except Exception as e:  #Function definition is not valid
            #print(f"Error during execution: {e}")
            errormsg = f"{errormsg}<Function Definition> Error during execution: {e}. "
            uf.textEdit_SecuFnDef.setStyleSheet(f"background-color: {CLR_INVALID};")
            Is_FunctionDef_valid = False

    Is_InputFieldsValid = Is_getSeedSF_valid and Is_validateKeySF_valid and Is_SeedLength_valid and Is_KeyLength_valid and Is_sampleSeed_valid and Is_sampleKey_valid and Is_secuFuncName_valid and Is_FunctionDef_valid
    return(Is_InputFieldsValid,errormsg)

    
