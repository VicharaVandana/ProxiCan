from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QTextEdit, QVBoxLayout, QWidget
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Initialize your form fields here
        self.lineEdit_SubFn_Seed = QLineEdit()
        self.lineEdit_SubFn_Key = QLineEdit()
        self.lineEdit_SeedLengthBytes = QLineEdit()
        self.lineEdit_KeyLengthBytes = QLineEdit()
        self.lineEdit_SecurityFuncName = QLineEdit()
        self.lineEdit_sampleseed = QLineEdit()
        self.lineEdit_samplekey = QLineEdit()
        self.textEdit_SecuFnDef = QTextEdit()
        
        # Store the initial values
        self.inputwidgets = [
            self.lineEdit_SubFn_Seed,
            self.lineEdit_SubFn_Key,
            self.lineEdit_SeedLengthBytes,
            self.lineEdit_KeyLengthBytes,
            self.lineEdit_SecurityFuncName,
            self.lineEdit_sampleseed,
            self.lineEdit_samplekey,
            self.textEdit_SecuFnDef
        ]
        
        # Populate initial values from data (example values)
        self.populate_inputwidgets({
            "subfunction_getseed": "01",
            "subfunction_validatekey": "02",
            "seedLength": "2",
            "keyLength": "2",
            "SecurityFunction": "getKey4mSeed_SecuLvl_01",
            "SampleSeed": "123",
            "SampleKey": "456",
            "SecurityFunctionDefinition": "def getKey4mSeed_SecuLvl_01(seed):\n    return seed * 2"
        })
        
        # Connect signals for checking edits
        for widget in self.inputwidgets.keys():
            widget.installEventFilter(self)
        
        # Set up the layout
        layout = QVBoxLayout()
        layout.addWidget(self.lineEdit_SubFn_Seed)
        layout.addWidget(self.lineEdit_SubFn_Key)
        layout.addWidget(self.lineEdit_SeedLengthBytes)
        layout.addWidget(self.lineEdit_KeyLengthBytes)
        layout.addWidget(self.lineEdit_SecurityFuncName)
        layout.addWidget(self.lineEdit_sampleseed)
        layout.addWidget(self.lineEdit_samplekey)
        layout.addWidget(self.textEdit_SecuFnDef)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def populate_inputwidgets(self, config_data):
        """ Populate and store initial values from configuration """
        self.lineEdit_SubFn_Seed.setText(config_data["subfunction_getseed"])
        self.lineEdit_SubFn_Key.setText(config_data["subfunction_validatekey"])
        self.lineEdit_SeedLengthBytes.setText(config_data["seedLength"])
        self.lineEdit_KeyLengthBytes.setText(config_data["keyLength"])
        self.lineEdit_SecurityFuncName.setText(config_data["SecurityFunction"])
        self.lineEdit_sampleseed.setText(config_data["SampleSeed"])
        self.lineEdit_samplekey.setText(config_data["SampleKey"])
        self.textEdit_SecuFnDef.setPlainText(config_data["SecurityFunctionDefinition"])
        
        # Store initial values for comparison
        self.inputwidgets[self.lineEdit_SubFn_Seed] = config_data["subfunction_getseed"]
        self.inputwidgets[self.lineEdit_SubFn_Key] = config_data["subfunction_validatekey"]
        self.inputwidgets[self.lineEdit_SeedLengthBytes] = config_data["seedLength"]
        self.inputwidgets[self.lineEdit_KeyLengthBytes] = config_data["keyLength"]
        self.inputwidgets[self.lineEdit_SecurityFuncName] = config_data["SecurityFunction"]
        self.inputwidgets[self.lineEdit_sampleseed] = config_data["SampleSeed"]
        self.inputwidgets[self.lineEdit_samplekey] = config_data["SampleKey"]
        self.inputwidgets[self.textEdit_SecuFnDef] = config_data["SecurityFunctionDefinition"]
    
    def eventFilter(self, widget, event):
        """ Event filter to handle focus out event for all fields """
        if event.type() == event.FocusOut:
            if widget in self.inputwidgets:
                current_value = widget.text() if isinstance(widget, QLineEdit) else widget.toPlainText()
                initial_value = self.inputwidgets[widget]
                
                # Check if value changed, update background color
                if current_value != initial_value:
                    widget.setStyleSheet("background-color: lightyellow; color: black;")
                else:
                    widget.setStyleSheet("background-color: white; color: black;")
        return super().eventFilter(widget, event)

# Initialize the application and run the form
app = QApplication([])
window = MyWindow()
window.show()
app.exec_()
