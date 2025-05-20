import sys
import json
from PyQt5 import QtCore, QtGui, QtWidgets

class Service19Subfunc_EnDis_Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Set the window title
        self.setWindowTitle("Service 19 Subfunctions Manager")
        self.resize(600, 500)

        # Load JSON file
        self.load_json()

        # Main layout
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # Header label
        header_label = QtWidgets.QLabel("Enable or Disable Service 19 Subfunctions")
        font = QtGui.QFont("Lucida Console", 12, QtGui.QFont.Bold)
        header_label.setFont(font)
        header_label.setAlignment(QtCore.Qt.AlignCenter)
        main_layout.addWidget(header_label)

        # Create a grid layout for the buttons
        grid_layout = QtWidgets.QGridLayout()
        grid_layout.setSpacing(10)

        # Add buttons for Service 19 subfunctions
        self.buttons = []
        self.button_names = [
            "01", "02", "03", "04", "05", "06", "07", "08", "09",
            "0A", "0B", "0C", "0D", "0E", "0F", "10", "11", "12", 
            "13", "14", "15", "16", "17", "18", "19", "42", "55"
        ]

        for i, name in enumerate(self.button_names):
            button = QtWidgets.QPushButton(f"Subfunction {name}")
            button.setMinimumSize(QtCore.QSize(120, 50))  # Slightly increased button size
            font = QtGui.QFont()
            font.setFamily("Lucida Console")
            font.setPointSize(10)
            button.setFont(font)

            # Set the initial color based on the current state in JSON
            if self.subfunc_visibility.get(name, True):  # Default to True if not in JSON
                button.setStyleSheet("background-color: rgb(0, 200, 0); color: blue;")  # Green for enabled
            else:
                button.setStyleSheet("background-color: rgb(200, 0, 0); color: white;")  # Red for disabled

            button.setObjectName(f"{name}")
            grid_layout.addWidget(button, i // 3, i % 3)  # Arrange in grid, 3 buttons per row
            button.clicked.connect(lambda _, b=button: self.toggle_button(b))  # Connect click event
            self.buttons.append(button)

        main_layout.addLayout(grid_layout)

        # Add status label
        self.status_label = QtWidgets.QLabel("Select a subfunction to enable/disable.")
        self.status_label.setAlignment(QtCore.Qt.AlignCenter)
        main_layout.addWidget(self.status_label)

    def load_json(self):
        """Load the JSON file that contains the visibility states."""
        try:
            with open('service19_subfunctionsettings.json', 'r') as file:
                data = json.load(file)
                self.subfunc_visibility = data.get("Service_19_Subfunctions_Visibility", {})
        except FileNotFoundError:
            print("Error: service19_subfunctionsettings.json file not found.")
            self.subfunc_visibility = {}

    def save_json(self):
        """Save the updated visibility states to the JSON file."""
        with open('service19_subfunctionsettings.json', 'w') as file:
            json.dump({"Service_19_Subfunctions_Visibility": self.subfunc_visibility}, file, indent=4)

    def toggle_button(self, button):
        """Toggle the button color and update the corresponding JSON value."""
        button_name = button.objectName()

        # Toggle visibility state in JSON (True/False)
        self.subfunc_visibility[button_name] = not self.subfunc_visibility.get(button_name, True)
        self.save_json()  # Save the updated state to JSON

        # Toggle the button's background color
        if self.subfunc_visibility[button_name]:
            button.setStyleSheet("background-color: rgb(0, 200, 0); color: blue;")  # Green for enabled
            self.status_label.setText(f"Subfunction {button_name} enabled.")
        else:
            button.setStyleSheet("background-color: rgb(200, 0, 0); color: white;")  # Red for disabled
            self.status_label.setText(f"Subfunction {button_name} disabled.")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    service19subfunc_enabledisable_window = Service19Subfunc_EnDis_Window()
    service19subfunc_enabledisable_window.show()
    sys.exit(app.exec_())
