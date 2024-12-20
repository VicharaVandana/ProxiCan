import sys
import json
from cryptography.fernet import Fernet
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QFileDialog, QLineEdit, QLabel, QMessageBox
)

# File paths
JSON_FILE_PATH = "securityLvl_config.json"
KEY_FILE_PATH = "encryption.key"  # File to store the encryption key

class SecuLvlImportTool(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("JSON Import Tool")
        self.setGeometry(300, 100, 500, 300)
        self.cipher_suite = self.load_key()
        self.init_ui()

    def load_key(self):
        """Load the encryption key."""
        try:
            with open(KEY_FILE_PATH, 'rb') as key_file:
                key = key_file.read()
            return Fernet(key)
        except FileNotFoundError:
            QMessageBox.critical(self, "Error", f"Key file '{KEY_FILE_PATH}' not found.")
            sys.exit()

    def init_ui(self):
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Import Configuration"))
        self.line_edit_import_path = QLineEdit(self)
        self.line_edit_import_path.setPlaceholderText("Enter or browse the file path to import...")
        layout.addWidget(self.line_edit_import_path)

        self.button_browse_import = QPushButton("Browse Import Path")
        self.button_browse_import.clicked.connect(self.browse_import_file)
        layout.addWidget(self.button_browse_import)

        self.button_import = QPushButton("Import and Merge")
        self.button_import.clicked.connect(self.import_and_merge)
        layout.addWidget(self.button_import)

        self.setLayout(layout)

    def browse_import_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Choose Import File", "", "Encoded Files (*.enc);;All Files (*)")
        if file_path:
            self.line_edit_import_path.setText(file_path)

    def import_and_merge(self):
        file_path = self.line_edit_import_path.text()

        if not file_path:
            QMessageBox.warning(self, "Warning", "Please specify a file path to import.")
            return

        try:
            # Read and decode the data
            with open(file_path, 'rb') as import_file:
                encoded_data = import_file.read()

            decoded_data = self.cipher_suite.decrypt(encoded_data).decode()
            imported_data = json.loads(decoded_data)

            # Read the existing JSON file
            with open(JSON_FILE_PATH, 'r') as json_file:
                existing_data = json.load(json_file)

            # Perform checks
            for secu_level, config_data in imported_data.items():
                if secu_level in existing_data:
                    QMessageBox.warning(
                        self, "Conflict Detected",
                        f"Security level '{secu_level}' already exists in the base JSON file. Import aborted."
                    )
                    return

                imported_getseed = config_data.get("subfunction_getseed")
                for existing_secu_level, existing_config in existing_data.items():
                    if existing_config.get("subfunction_getseed") == imported_getseed:
                        QMessageBox.warning(
                            self, "Conflict Detected",
                            f"Subfunction getseed value '{imported_getseed}' is already used by security level '{existing_secu_level}'. Import aborted."
                        )
                        return

            # Merge data if no conflicts
            existing_data.update(imported_data)

            with open(JSON_FILE_PATH, 'w') as json_file:
                json.dump(existing_data, json_file, indent=4)

            QMessageBox.information(self, "Success", "Imported data successfully merged with the existing JSON file.")

        except FileNotFoundError:
            QMessageBox.critical(self, "Error", f"Base JSON file '{JSON_FILE_PATH}' not found.")
        except json.JSONDecodeError:
            QMessageBox.critical(self, "Error", "Failed to decode JSON file or imported data. Check the file format.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SecuLvlImportTool()
    window.show()
    sys.exit(app.exec_())
