import sys
import json
from PyQt5 import QtCore, QtGui, QtWidgets

class Service19Subfunc_EnDis_Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Set the window title
        self.setWindowTitle("Enabling or Disabling Service 19 Subfunctions")

        # Load JSON file
        self.load_json()

        # Create a grid layout for the buttons
        self.gridLayout_UDSServiceButtons = QtWidgets.QGridLayout(self)
        self.gridLayout_UDSServiceButtons.setContentsMargins(0, 0, 0, 0)

        # List of buttons and their labels
        self.buttons = []
        self.button_names = [
            "01", "02", "03", "04", "05", "06", "07", "08", "09", 
            "0A", "0B", "0C", "0D", "0E", "0F", "10", "11", "12", "13", "14", "15", 
            "16", "17", "18", "19", "42", "55"
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
            if self.subfunc_visibility[name]:
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
            with open('subfunctionsettings.json', 'r') as file:
                data = json.load(file)
                self.subfunc_visibility = data["Service_19_Subfunctions_Visibility"]
        except FileNotFoundError:
            print("Error: subfunctionsettings.json file not found.")
            sys.exit(1)

    def save_json(self):
        """Save the updated visibility states to the JSON file."""
        with open('subfunctionsettings.json', 'w') as file:
            json.dump({"Service_19_Subfunctions_Visibility": self.subfunc_visibility}, file, indent=4)

    def toggle_button(self, button):
        """Toggle the button color and update the corresponding JSON value."""
        button_name = button.objectName()

        # Toggle visibility state in JSON (True/False)
        self.subfunc_visibility[button_name] = not self.subfunc_visibility[button_name]
        self.save_json()  # Save the updated state to JSON

        # Toggle the button's background and text color
        if self.subfunc_visibility[button_name]:
            button.setStyleSheet("background-color: rgb(170, 255, 0);\ncolor: rgb(0, 0, 255);")
        else:
            button.setStyleSheet("background-color: rgb(255, 0, 0);\ncolor: rgb(255, 255, 255);")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    service19subfunc_enabledisable_window = Service19Subfunc_EnDis_Window()
    service19subfunc_enabledisable_window.show()
    sys.exit(app.exec_())
