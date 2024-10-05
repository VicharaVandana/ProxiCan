import sys
import json
import os
from PyQt5 import QtWidgets, QtCore
import general as gen

class LogFileSelector(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Log File Selector')
        # Get the screen geometry
        screen = QtWidgets.QApplication.primaryScreen().availableGeometry()
        screen_width = screen.width()

        # Set window size slightly less than screen width (e.g., 90% of screen width)
        window_width = int(screen_width * 0.9)
        window_height = 400  # You can adjust the height as needed

        # Set the window geometry (centered horizontally)
        self.setGeometry(
            (screen.width() - window_width) // 2,  # Center the window horizontally
            100,                                  # Set Y position
            window_width,
            window_height
        )


        # Load current paths from JSON
        self.settings_file = 'windowsettings.json'
        self.settings = self.load_settings()

        # Create UI elements
        self.create_ui()

        

    def create_ui(self):
        layout = QtWidgets.QVBoxLayout(self)

        # Dictionary for QLineEdit (single line text fields) and buttons
        self.log_paths = {
            'ACTIONLOG_FULLPATH': QtWidgets.QLineEdit(),
            'CANTRAFFICLOG_FULLPATH': QtWidgets.QLineEdit(),
            'CANTPLOG_FULLPATH': QtWidgets.QLineEdit(),
            'UDSLOG_FULLPATH': QtWidgets.QLineEdit()
        }

        self.buttons = {
            'ACTIONLOG_FULLPATH': QtWidgets.QPushButton('Browse Action Log'),
            'CANTRAFFICLOG_FULLPATH': QtWidgets.QPushButton('Browse CAN Traffic Log'),
            'CANTPLOG_FULLPATH': QtWidgets.QPushButton('Browse CAN TP Log'),
            'UDSLOG_FULLPATH': QtWidgets.QPushButton('Browse UDS Log')
        }

        # Load current paths into the line edits
        self.update_line_edits()

        # Add QLineEdit and QPushButton for each log path in a horizontal layout
        for log_type, line_edit in self.log_paths.items():
            h_layout = QtWidgets.QHBoxLayout()  # Horizontal layout
            h_layout.addWidget(line_edit)
            h_layout.addWidget(self.buttons[log_type])
            layout.addLayout(h_layout)
            self.buttons[log_type].clicked.connect(lambda _, lt=log_type: self.select_log_file(lt))

        # Save button at the bottom
        self.save_button = QtWidgets.QPushButton('Save Log Paths')
        self.save_button.clicked.connect(self.save_settings)
        layout.addWidget(self.save_button)

    def update_line_edits(self):
        """Load paths from JSON file into the QLineEdit widgets."""
        for log_type, line_edit in self.log_paths.items():
            line_edit.setText(self.settings.get(log_type, ""))
            line_edit.setReadOnly(True)  # Make the line edit read-only, user updates via file dialog

    def select_log_file(self, log_type):
        """Open a file dialog to select a log file and update the corresponding QLineEdit."""
        gen.log_action("Button Click", f"In Log File Selector Window, the button <{self.buttons[log_type].text()}> is clicked")
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog

        # Setting the dialog box title according to the log type
        dialog_title = f"Select {self.get_log_label(log_type)}"

        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, dialog_title, "", "Log Files (*.txt);;All Files (*)", options=options)
        
        if file_path:
            self.log_paths[log_type].setText(file_path)
            gen.log_action("Log Path Change", f"In Log File Selector Window, the {log_type} path changed <{file_path}> is clicked")
        

    def get_log_label(self, log_type):
        """Return the appropriate label for each log type."""
        labels = {
            'ACTIONLOG_FULLPATH': 'Action Log File',
            'CANTRAFFICLOG_FULLPATH': 'CAN Traffic Log File',
            'CANTPLOG_FULLPATH': 'CAN TP Log File',
            'UDSLOG_FULLPATH': 'UDS Log File'
        }
        return labels.get(log_type, 'Log File')

    def save_settings(self):
        """Save the updated log file paths to the JSON file."""
        gen.log_action("Button Click", f"In Log File Selector Window, the button <Save Log Paths> is clicked")
        # Only update the log paths, avoid touching UDS_BUTTONS_VISIBILITY
        for log_type, line_edit in self.log_paths.items():
            self.settings[log_type] = line_edit.text()

        self.write_settings()

    def load_settings(self):
        """Load settings from the JSON file."""
        if os.path.exists(self.settings_file):
            with open(self.settings_file, 'r') as file:
                return json.load(file)
        else:
            # Default settings if the file doesn't exist
            return {
                "ACTIONLOG_FULLPATH": "",
                "CANTRAFFICLOG_FULLPATH": "",
                "CANTPLOG_FULLPATH": "",
                "UDSLOG_FULLPATH": "",
                "UDS_BUTTONS_VISIBILITY": {
                    "10": True, "22": True, "2E": True, "11": False, "27": True, 
                    "28": False, "14": True, "19": False, "85": False, "23": True, 
                    "2A": True, "2C": True, "31": True, "34": False, "35": False, 
                    "36": False, "37": False, "38": False, "2F": True, "83": True, 
                    "86": False
                }
            }

    def write_settings(self):
        """Write the updated settings to the JSON file."""
        # Load existing JSON data to avoid modifying 'UDS_BUTTONS_VISIBILITY'
        with open(self.settings_file, 'r') as file:
            json_data = json.load(file)
        
        # Only update log file paths in the JSON
        for log_type in self.log_paths.keys():
            json_data[log_type] = self.settings[log_type]

        # Write back the updated JSON
        with open(self.settings_file, 'w') as file:
            json.dump(json_data, file, indent=4)

        QtWidgets.QMessageBox.information(self, 'Success', 'Log paths saved successfully!')
        gen.log_action("Log Paths Update", f"Log paths saved successfully! in settings")
        

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = LogFileSelector()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
