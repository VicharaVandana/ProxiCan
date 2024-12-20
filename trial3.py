import sys
import json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QCheckBox, QPushButton,
    QFileDialog, QLineEdit, QLabel, QMessageBox, QScrollArea, QGroupBox
)

JSON_FILE_PATH = "securityLvl_config.json"


class JsonExportTool(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("JSON Export Tool")
        self.setGeometry(300, 100, 500, 600)
        self.selected_items = {}
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Instruction Label
        self.label_instruction = QLabel("Select elements to export:")
        layout.addWidget(self.label_instruction)

        # Scrollable Area for Checkboxes
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.checkbox_group = QGroupBox()
        self.checkbox_layout = QVBoxLayout()

        # Load JSON and populate checkboxes
        self.load_json_data()

        self.checkbox_group.setLayout(self.checkbox_layout)
        self.scroll_area.setWidget(self.checkbox_group)
        layout.addWidget(self.scroll_area)

        # LineEdit for file path and Browse Button
        self.line_edit_path = QLineEdit(self)
        self.line_edit_path.setPlaceholderText("Enter or browse the file path to export...")
        layout.addWidget(self.line_edit_path)

        self.button_browse = QPushButton("Browse")
        self.button_browse.clicked.connect(self.browse_file)
        layout.addWidget(self.button_browse)

        # Export Button
        self.button_export = QPushButton("Export")
        self.button_export.clicked.connect(self.export_selected_items)
        layout.addWidget(self.button_export)

        self.setLayout(layout)

    def load_json_data(self):
        try:
            with open(JSON_FILE_PATH, 'r') as json_file:
                self.json_data = json.load(json_file)

                # Create a checkbox for each key in the JSON file, excluding "New_SecurityLevel" and empty keys
                for key in self.json_data.keys():
                    if key and key != "New_SecurityLevel":  # Exclude empty and "New_SecurityLevel"
                        checkbox = QCheckBox(key)
                        checkbox.stateChanged.connect(lambda state, k=key: self.update_selected_items(state, k))
                        self.checkbox_layout.addWidget(checkbox)

        except FileNotFoundError:
            QMessageBox.critical(self, "Error", f"JSON file '{JSON_FILE_PATH}' not found.")
            self.json_data = {}
        except json.JSONDecodeError:
            QMessageBox.critical(self, "Error", "Failed to decode JSON file. Check the file format.")
            self.json_data = {}

    def update_selected_items(self, state, key):
        if state == 2:  # Checked
            self.selected_items[key] = self.json_data[key]
        elif key in self.selected_items:
            del self.selected_items[key]

    def browse_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_path, _ = QFileDialog.getSaveFileName(self, "Choose Export File", "", "JSON Files (*.json);;All Files (*)", options=options)
        if file_path:
            self.line_edit_path.setText(file_path)

    def export_selected_items(self):
        file_path = self.line_edit_path.text()

        if not file_path:
            QMessageBox.warning(self, "Warning", "Please specify a file path to export.")
            return

        if not self.selected_items:
            QMessageBox.warning(self, "Warning", "No items selected for export.")
            return

        try:
            with open(file_path, 'w') as export_file:
                json.dump(self.selected_items, export_file, indent=4)
            QMessageBox.information(self, "Success", f"Selected items successfully exported to {file_path}.")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to export items: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = JsonExportTool()
    window.show()
    sys.exit(app.exec_())
