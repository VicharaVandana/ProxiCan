import sys
import json
from PyQt5 import QtCore, QtGui, QtWidgets

class UDSservice_EnDis_Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Set the window title
        self.setWindowTitle("Enabling or Disabling UDS Services")

        # Load JSON file
        self.load_json()

        # Create a grid layout for the buttons
        self.gridLayout_UDSServiceButtons = QtWidgets.QGridLayout(self)
        self.gridLayout_UDSServiceButtons.setContentsMargins(0, 0, 0, 0)

        # List of buttons and their labels
        self.buttons = []
        self.button_names = [
            "10", "22", "2E", "11", "27", "28", "14", "19", "85", 
            "23", "2A", "2C", "31", "34", "35", "36", "37", "38", "2F", "86", "83"
        ]

        # Add buttons to the grid and store references in the list
        for i, name in enumerate(self.button_names):
            button = QtWidgets.QPushButton(f"{name}")
            button.setMinimumSize(QtCore.QSize(51, 31))
            font = QtGui.QFont()
            font.setFamily("Lucida Console")
            font.setPointSize(10)
            button.setFont(font)
            
            # Set the initial color based on the current state in JSON
            if self.uds_visibility[name]:
                button.setStyleSheet("background-color: rgb(170, 255, 0);\ncolor: rgb(0, 0, 255);")
            else:
                button.setStyleSheet("background-color: rgb(255, 0, 0);\ncolor: rgb(255, 255, 255);")
                
            button.setObjectName(f"{name}")
            self.gridLayout_UDSServiceButtons.addWidget(button, i // 3, i % 3)  # Arrange in grid
            button.clicked.connect(lambda _, b=button: self.toggle_button(b))  # Connect click event
            self.buttons.append(button)

    def load_json(self):
        """Load the JSON file that contains the visibility states."""
        try:
            with open('windowsettings.json', 'r') as file:
                data = json.load(file)
                self.uds_visibility = data["UDS_BUTTONS_VISIBILITY"]
        except FileNotFoundError:
            print("Error: windowssettings.json file not found.")
            sys.exit(1)

    def save_json(self):
        """Save the updated visibility states to the JSON file."""
        with open('windowsettings.json', 'w') as file:
            json.dump({"UDS_BUTTONS_VISIBILITY": self.uds_visibility}, file, indent=4)

    def toggle_button(self, button):
        """Toggle the button color and update the corresponding JSON value."""
        button_name = button.objectName()

        # Toggle visibility state in JSON (True/False)
        self.uds_visibility[button_name] = not self.uds_visibility[button_name]
        self.save_json()  # Save the updated state to JSON

        # Toggle the button's background and text color
        if self.uds_visibility[button_name]:
            button.setStyleSheet("background-color: rgb(170, 255, 0);\ncolor: rgb(0, 0, 255);")
        else:
            button.setStyleSheet("background-color: rgb(255, 0, 0);\ncolor: rgb(255, 255, 255);")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    udsservice_enabledisable_window = UDSservice_EnDis_Window()
    udsservice_enabledisable_window.show()
    sys.exit(app.exec_())
