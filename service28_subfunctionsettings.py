import sys
import json
from PyQt5 import QtCore, QtGui, QtWidgets

class Service28Subfunc_CommType_EnDis_Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Set the window title
        self.setWindowTitle("Service 28 Subfunctions & Communication Types Manager")
        self.resize(400, 400)

        # Load JSON file
        self.load_json()

        # Main layout
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # Header label
        header_label = QtWidgets.QLabel("Enable or Disable Service 28 Subfunctions and Communication Types")
        font = QtGui.QFont("Lucida Console", 12, QtGui.QFont.Bold)
        header_label.setFont(font)
        header_label.setAlignment(QtCore.Qt.AlignCenter)
        main_layout.addWidget(header_label)

        # Add a label for Subfunction Buttons
        subfunc_label = QtWidgets.QLabel("Enable or Disable Subfunctions")
        subfunc_label.setAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont("Lucida Console", 10, QtGui.QFont.Bold)
        subfunc_label.setFont(font)
        main_layout.addWidget(subfunc_label)

        # Create a grid layout for the subfunction buttons
        grid_layout = QtWidgets.QGridLayout()
        grid_layout.setSpacing(10)

        # Add subfunction buttons for Service 28 (00 to 05)
        self.buttons = []
        self.subfunction_names = ["00", "01", "02", "03", "04", "05"]  # Subfunctions 00 to 05

        for i, name in enumerate(self.subfunction_names):
            button = QtWidgets.QPushButton(f"Subfunction {name}")
            button.setMinimumSize(QtCore.QSize(100, 40))
            font = QtGui.QFont()
            font.setFamily("Lucida Console")
            font.setPointSize(10)
            button.setFont(font)

            # Set the initial color based on the current state in JSON
            if self.subfunc_visibility["subfunctions"][name]:
                button.setStyleSheet("background-color: rgb(0, 200, 0); color: blue;")  # Green for enabled
            else:
                button.setStyleSheet("background-color: rgb(200, 0, 0); color: white;")  # Red for disabled

            button.setObjectName(f"{name}")
            grid_layout.addWidget(button, i // 3, i % 3)  # Arrange in grid
            button.clicked.connect(lambda _, b=button: self.toggle_subfunction_button(b))  # Connect click event
            self.buttons.append(button)

        main_layout.addLayout(grid_layout)

        # Add a label for Communication Type Buttons
        commtype_label = QtWidgets.QLabel("Enable or Disable Communication Types")
        commtype_label.setAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont("Lucida Console", 10, QtGui.QFont.Bold)
        commtype_label.setFont(font)
        main_layout.addWidget(commtype_label)

        # Create a new grid layout for the communication type buttons
        comm_grid_layout = QtWidgets.QGridLayout()
        comm_grid_layout.setSpacing(10)

        # Add communication type buttons for Service 28 (01, 02, 03)
        self.comm_buttons = []
        self.comm_type_names = ["01", "02", "03"]

        for i, name in enumerate(self.comm_type_names):
            button = QtWidgets.QPushButton(f"Comm Type {name}")
            button.setMinimumSize(QtCore.QSize(100, 40))
            font = QtGui.QFont()
            font.setFamily("Lucida Console")
            font.setPointSize(10)
            button.setFont(font)

            # Set the initial color based on the current state in JSON
            if self.subfunc_visibility["communication_types"][name]:
                button.setStyleSheet("background-color: rgb(0, 200, 0); color: blue;")  # Green for enabled
            else:
                button.setStyleSheet("background-color: rgb(200, 0, 0); color: white;")  # Red for disabled

            button.setObjectName(f"{name}")
            comm_grid_layout.addWidget(button, i // 3, i % 3)  # Arrange in grid
            button.clicked.connect(lambda _, b=button: self.toggle_commtype_button(b))  # Connect click event
            self.comm_buttons.append(button)

        main_layout.addLayout(comm_grid_layout)

        # Add status label
        self.status_label = QtWidgets.QLabel("Select a subfunction or communication type to enable/disable.")
        self.status_label.setAlignment(QtCore.Qt.AlignCenter)
        main_layout.addWidget(self.status_label)

    def load_json(self):
        """Load the JSON file that contains the visibility states."""
        try:
            with open('service28_subfunctionsettings.json', 'r') as file:
                data = json.load(file)
                self.subfunc_visibility = data["Service_28_Subfunctions_Visibility"]
        except FileNotFoundError:
            print("Error: service28_subfunctionsettings.json file not found.")
            sys.exit(1)

    def save_json(self):
        """Save the updated visibility states to the JSON file."""
        with open('service28_subfunctionsettings.json', 'w') as file:
            json.dump({
                "Service_28_Subfunctions_Visibility": self.subfunc_visibility
            }, file, indent=4)

    def toggle_subfunction_button(self, button):
        """Toggle the subfunction button color and update the corresponding JSON value."""
        button_name = button.objectName()

        # Toggle visibility state in JSON (True/False)
        self.subfunc_visibility["subfunctions"][button_name] = not self.subfunc_visibility["subfunctions"][button_name]
        self.save_json()  # Save the updated state to JSON

        # Toggle the button's background color
        if self.subfunc_visibility["subfunctions"][button_name]:
            button.setStyleSheet("background-color: rgb(0, 200, 0); color: blue;")  # Green for enabled
            self.status_label.setText(f"Subfunction {button_name} enabled.")
        else:
            button.setStyleSheet("background-color: rgb(200, 0, 0); color: white;")  # Red for disabled
            self.status_label.setText(f"Subfunction {button_name} disabled.")

    def toggle_commtype_button(self, button):
        """Toggle the communication type button color and update the corresponding JSON value."""
        button_name = button.objectName()

        # Toggle visibility state in JSON (True/False)
        self.subfunc_visibility["communication_types"][button_name] = not self.subfunc_visibility["communication_types"][button_name]
        self.save_json()  # Save the updated state to JSON

        # Toggle the button's background color
        if self.subfunc_visibility["communication_types"][button_name]:
            button.setStyleSheet("background-color: rgb(0, 200, 0); color: blue;")  # Green for enabled
            self.status_label.setText(f"Comm Type {button_name} enabled.")
        else:
            button.setStyleSheet("background-color: rgb(200, 0, 0); color: white;")  # Red for disabled
            self.status_label.setText(f"Comm Type {button_name} disabled.")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    service28subfunc_commtype_enabledisable_window = Service28Subfunc_CommType_EnDis_Window()
    service28subfunc_commtype_enabledisable_window.show()
    sys.exit(app.exec_())
