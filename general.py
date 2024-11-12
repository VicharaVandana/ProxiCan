import time
import re
import os
import json

#Global Variables
IsAnyServiceActive = False  #Assume initially no service is active

IsTesterPresentActive = False

# Path to JSON file
JSON_FILE_PATH = "windowsettings.json"

# Load log file paths from JSON
def load_log_file_paths():
    try:
        with open(JSON_FILE_PATH, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Return default paths if JSON file not found or corrupted
        return {
            "ACTIONLOG_FULLPATH": "./reports/can_actionlog_report.txt",
            "CANTRAFFICLOG_FULLPATH": "./reports/cantraffic_log_report.txt",
            "CANTPLOG_FULLPATH": "./reports/tp_log_report.txt",
            "UDSLOG_FULLPATH": "./reports/uds_log_report.txt"
        }

# Logging functions with paths read from the JSON file

def tp_log(log_type, message):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    tp_log_file = load_log_file_paths().get("CANTPLOG_FULLPATH", "./reports/tp_log_report.txt")
    with open(tp_log_file, "a") as log_file:
        log_file.write(f"[{timestamp}] {log_type}: {message}\n")
    return

def cleartp_log():
    tp_log_file = load_log_file_paths().get("CANTPLOG_FULLPATH", "./reports/tp_log_report.txt")
    with open(tp_log_file, 'w') as file:
        # Opening the file in 'w' mode automatically clears its contents
        pass

def log_udsreport(log_snippet):
    uds_log_file = load_log_file_paths().get("UDSLOG_FULLPATH", "./reports/uds_log_report.txt")
    with open(uds_log_file, "a") as log_file:
        log_file.write(log_snippet)
    return

def clearudslogfile():
    uds_log_file = load_log_file_paths().get("UDSLOG_FULLPATH", "./reports/uds_log_report.txt")
    with open(uds_log_file, 'w') as file:
        pass

def logcantraffic(direction, timestamp, id, dlc, databytes):
    cantraffic_log_file = load_log_file_paths().get("CANTRAFFICLOG_FULLPATH", "./reports/cantraffic_log_report.txt")
    with open(cantraffic_log_file, "a") as log_file:
        log_file.write(f"[{timestamp}] {direction}: ID: {hex(id)}\t{dlc}\t[{' '.join(hex(number) for number in databytes)}]\n")
    return

def clearcantrafficlogfile():
    cantraffic_log_file = load_log_file_paths().get("CANTRAFFICLOG_FULLPATH", "./reports/cantraffic_log_report.txt")
    with open(cantraffic_log_file, 'w') as file:
        pass

def log_action(action_type, action):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    action_log_file = load_log_file_paths().get("ACTIONLOG_FULLPATH", "./reports/can_actionlog_report.txt")
    with open(action_log_file, "a") as log_file:
        log_file.write(f"<{os.getlogin()}>[{timestamp}] {action_type}: {action}\n")
    return

def clearActionfile():
    action_log_file = load_log_file_paths().get("ACTIONLOG_FULLPATH", "./reports/can_actionlog_report.txt")
    with open(action_log_file, 'w') as file:
        pass


def is_validfloat(str, min_value, max_value):
    """
    Check if the input string can be converted to a floating-point number.

    :param str: The input string to check
    :param min_value: The minimum value (inclusive) for the float number
    :param max_value: The maximum value (inclusive) for the float number
    :return: floating value if the string represents a valid float, otherwise False
    """
    try:
        # Attempt to convert the string to a float
        value = float(str)
        # Check if the value is within the specified range
        if (min_value <= value <= max_value):
            return value
        else:
            return False
    except ValueError:
        # Conversion failed, so the string is not a valid float
        return False
    
def is_valid_hex(hex_str, min_value, max_value):
    """
    Check if the input string is a hexadecimal number and falls between the given min and max values.

    :param hex_str: The input string to check
    :param min_value: The minimum value (inclusive) for the hexadecimal number
    :param max_value: The maximum value (inclusive) for the hexadecimal number
    :return: True if the input is a valid hexadecimal number within the range, otherwise False
    """
    hexstr_withoutspaces = re.sub(r"\s+", "", hex_str)
    try:
        # Check if the input string is a valid hexadecimal number
        value = int(hexstr_withoutspaces, 16)
    except ValueError:
        # Input is not a valid hexadecimal number
        return False

    # Check if the value is within the specified range
    if (min_value <= value <= max_value):
        return value
    else:
        return False

def check_2Bytehexadecimal(data):
        # Retrieve text from QLineEdit
        text = data
        # Regular expression for 2-byte hexadecimal value
        hex_pattern = re.compile(r'^[0-9A-Fa-f]{4}$')

        # Validate and update the result label
        if hex_pattern.match(text):
            return True
        else:
            return False

def check_3Bytehexadecimal(data):
        # Retrieve text from QLineEdit
        text = data
        # Regular expression for 2-byte hexadecimal value
        hex_pattern = re.compile(r'^[0-9A-Fa-f]{6}$')

        # Validate and update the result label
        if hex_pattern.match(text):
            return True
        else:
            return False   
          
def check_1Bytehexadecimal(data):
        # Retrieve text from QLineEdit
        text = data
        # Regular expression for 2-byte hexadecimal value
        hex_pattern = re.compile(r'^[0-9A-Fa-f]{2}$')

        # Validate and update the result label
        if hex_pattern.match(text):
            return True
        else:
            return False
        
def check_hexadecimal(data):
        # Retrieve text from QLineEdit
        text = data
        # Regular expression for 2-byte hexadecimal value
        hex_pattern = re.compile(r'^[0-9A-Fa-f]+$')

        # Validate and update the result label
        if hex_pattern.match(text):
            return True
        else:
            return False

def check_min1Bytehexadecimal(data):
        # Retrieve text from QLineEdit
        text = data
        # Regular expression for 2-byte hexadecimal value
        hex_pattern = re.compile(r'^([0-9A-Fa-f]{2})(\s?[0-9A-Fa-f]{2})*$')

        # Validate and update the result label
        if hex_pattern.match(text):
            return True
        else:
            return False
        

if __name__ == "__main__":
    print(check_min1Bytehexadecimal("33f4"))


