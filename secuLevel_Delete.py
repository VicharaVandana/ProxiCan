import sys
import json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QCheckBox, QFileDialog, QMessageBox, QLabel, QScrollArea, QFrame
)

# File path to the JSON file
JSON_FILE_PATH = "securityLvl_config.json"

class SecuLvlDeleteTool(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Delete Security Levels")
        self.setGeometry(300, 100, 600, 400)
        self.checkboxes = []
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Select All / Deselect All Buttons
        select_deselect_layout = QHBoxLayout()
        self.button_select_all = QPushButton("Select All")
        self.button_select_all.clicked.connect(self.select_all_checkboxes)
        select_deselect_layout.addWidget(self.button_select_all)

        self.button_deselect_all = QPushButton("Deselect All")
        self.button_deselect_all.clicked.connect(self.deselect_all_checkboxes)
        select_deselect_layout.addWidget(self.button_deselect_all)

        layout.addLayout(select_deselect_layout)

        # Label for instructions
        layout.addWidget(QLabel("Select the security levels to delete:"))

        # Scrollable area for checkboxes
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        self.checkbox_layout = QVBoxLayout(scroll_content)
        self.load_checkboxes()
        scroll_area.setWidget(scroll_content)
        layout.addWidget(scroll_area)

        # Delete Button
        self.button_delete = QPushButton("Delete Selected Levels")
        self.button_delete.clicked.connect(self.delete_selected_levels)
        layout.addWidget(self.button_delete)

        self.setLayout(layout)

    def load_checkboxes(self):
        """Load security levels from the JSON file and create checkboxes."""
        try:
            with open(JSON_FILE_PATH, 'r') as json_file:
                data = json.load(json_file)

            # Filter out "New_SecurityLevel" and empty elements
            valid_security_levels = [
                secu_level for secu_level in data.keys()
                if secu_level and secu_level != "New_SecurityLevel"
            ]

            # Create checkboxes
            for secu_level in valid_security_levels:
                checkbox = QCheckBox(secu_level)
                self.checkbox_layout.addWidget(checkbox)
                self.checkboxes.append(checkbox)

        except FileNotFoundError:
            QMessageBox.critical(self, "Error", f"JSON file '{JSON_FILE_PATH}' not found.")
        except json.JSONDecodeError:
            QMessageBox.critical(self, "Error", "Failed to decode JSON file. Check the file format.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {e}")

    def select_all_checkboxes(self):
        """Select all checkboxes."""
        for checkbox in self.checkboxes:
            checkbox.setChecked(True)

    def deselect_all_checkboxes(self):
        """Deselect all checkboxes."""
        for checkbox in self.checkboxes:
            checkbox.setChecked(False)

    def delete_selected_levels(self):
        """Delete the selected security levels."""
        try:
            # Load existing JSON data
            with open(JSON_FILE_PATH, 'r') as json_file:
                data = json.load(json_file)

            # Collect selected security levels
            selected_levels = [
                checkbox.text() for checkbox in self.checkboxes if checkbox.isChecked()
            ]

            if not selected_levels:
                QMessageBox.warning(self, "No Selection", "No security levels selected for deletion.")
                return

            # Confirmation dialog
            reply = QMessageBox.question(
                self, "Confirm Deletion",
                f"Are you sure you want to delete the selected security levels?\n\n{', '.join(selected_levels)}",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )

            if reply == QMessageBox.Yes:
                # Remove selected levels
                for level in selected_levels:
                    data.pop(level, None)

                # Write updated JSON back to the file
                with open(JSON_FILE_PATH, 'w') as json_file:
                    json.dump(data, json_file, indent=4)

                QMessageBox.information(self, "Success", "Selected security levels deleted successfully.")

                # Reload checkboxes
                for checkbox in self.checkboxes:
                    self.checkbox_layout.removeWidget(checkbox)
                    checkbox.deleteLater()
                self.checkboxes.clear()
                self.load_checkboxes()

        except FileNotFoundError:
            QMessageBox.critical(self, "Error", f"JSON file '{JSON_FILE_PATH}' not found.")
        except json.JSONDecodeError:
            QMessageBox.critical(self, "Error", "Failed to decode JSON file. Check the file format.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SecuLvlDeleteTool()
    window.show()
    sys.exit(app.exec_())
