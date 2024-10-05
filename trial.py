import json
import time
import os

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
