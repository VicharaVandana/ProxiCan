from PyQt5 import QtCore, QtGui, QtWidgets
 
class Ui_Form_SID2E(object):
    def setupUi(self, Form_SID2E):
        Form_SID2E.setObjectName("Form_SID2E")
        Form_SID2E.setWindowTitle("Write Data By Identifier Service 2E")
        Form_SID2E.resize(650, 520)
 
        self.label_status = QtWidgets.QLabel(Form_SID2E)
        self.label_status.setGeometry(QtCore.QRect(10, 440, 630, 60))
        self.label_status.setStyleSheet("background-color: rgb(255, 255, 127); color: rgb(85, 0, 0);")
        self.label_status.setAlignment(QtCore.Qt.AlignCenter)
        self.label_status.setWordWrap(True)
        self.label_status.setObjectName("label_status")
 
        self.layoutWidget = QtWidgets.QWidget(Form_SID2E)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 621, 421))
        self.layoutWidget.setObjectName("layoutWidget")
 
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
 
        # Entry type dropdown
        self.label_entryType = QtWidgets.QLabel(self.layoutWidget)
        self.label_entryType.setText("DID Entry Type:")
        self.gridLayout.addWidget(self.label_entryType, 0, 0)
 
        self.comboBox_entryType = QtWidgets.QComboBox(self.layoutWidget)
        self.comboBox_entryType.addItems(["Enable Manual Entry", "Enable Dropdown Entry"])
        self.comboBox_entryType.setToolTip("Choose manual input or select DID from dropdown list.")
        self.gridLayout.addWidget(self.comboBox_entryType, 0, 1)
 
        # Manual Entry
        self.label_manualDID = QtWidgets.QLabel(self.layoutWidget)
        self.label_manualDID.setText("DID:")
        self.gridLayout.addWidget(self.label_manualDID, 1, 0)
 
        self.lineEdit_manualDID = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_manualDID.setPlaceholderText("e.g., F190")
        self.gridLayout.addWidget(self.lineEdit_manualDID, 1, 1, 1, 2)
 
        # Dropdown DID
        self.label_dropdownDID = QtWidgets.QLabel(self.layoutWidget)
        self.label_dropdownDID.setText("DID:")
        self.gridLayout.addWidget(self.label_dropdownDID, 2, 0)
 
        self.comboBox_DID = QtWidgets.QComboBox(self.layoutWidget)
        self.comboBox_DID.addItems(["0xF190", "0x1234", "0xABCD"])  # Add your actual DIDs here
        self.gridLayout.addWidget(self.comboBox_DID, 2, 1, 1, 2)
 
        # Data Value
        self.label_data = QtWidgets.QLabel(self.layoutWidget)
        self.label_data.setText("Data Value:")
        self.gridLayout.addWidget(self.label_data, 3, 0)
 
        self.textEdit_datavalue = QtWidgets.QTextEdit(self.layoutWidget)
        self.gridLayout.addWidget(self.textEdit_datavalue, 3, 1, 1, 2)
 
        # Response type and send button
        self.label_responseType = QtWidgets.QLabel(self.layoutWidget)
        self.label_responseType.setText("Response Type:")
        self.gridLayout.addWidget(self.label_responseType, 4, 0)
 
        self.label_ResType = QtWidgets.QLabel(self.layoutWidget)
        self.label_ResType.setText("No Response")
        self.label_ResType.setAlignment(QtCore.Qt.AlignCenter)
        self.label_ResType.setStyleSheet("color: blue;")
        self.gridLayout.addWidget(self.label_ResType, 4, 1)
 
        self.pushButton_Send2EReq = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_Send2EReq.setText("Send Request")
        self.pushButton_Send2EReq.setStyleSheet("background-color: cyan;")
        self.gridLayout.addWidget(self.pushButton_Send2EReq, 4, 2)
 
        # Response output
        self.label_response = QtWidgets.QLabel(self.layoutWidget)
        self.label_response.setText("Response:")
        self.gridLayout.addWidget(self.label_response, 5, 0)
 
        self.textBrowser_Resp = QtWidgets.QTextBrowser(self.layoutWidget)
        self.gridLayout.addWidget(self.textBrowser_Resp, 5, 1, 1, 2)
 
        # Buttons
        self.pushButton_clearLog = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_clearLog.setText("Clear Log")
        self.pushButton_clearLog.setStyleSheet("background-color: lightgreen;")
        self.gridLayout.addWidget(self.pushButton_clearLog, 6, 1)
 
        self.pushButton_appendLog = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_appendLog.setText("Add to Log")
        self.pushButton_appendLog.setStyleSheet("background-color: lightgreen;")
        self.gridLayout.addWidget(self.pushButton_appendLog, 6, 2)
 
        self.pushButton_reset = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_reset.setText("Reset")
        self.pushButton_reset.setStyleSheet("background-color: khaki; color: darkgreen;")
        self.gridLayout.addWidget(self.pushButton_reset, 6, 0)
 
        # Status
        self.label_status.setText("No Status")
 
        # Connect dropdown toggle
        self.comboBox_entryType.currentTextChanged.connect(self.updateEntryMode)
        self.updateEntryMode("Enable Manual Entry")  # Default mode
 
        QtCore.QMetaObject.connectSlotsByName(Form_SID2E)
 
    def updateEntryMode(self, mode):
        if mode == "Enable Manual Entry":
            self.lineEdit_manualDID.setVisible(True)
            self.label_manualDID.setVisible(True)
            self.comboBox_DID.setVisible(False)
            self.label_dropdownDID.setVisible(False)
        else:
            self.lineEdit_manualDID.setVisible(False)
            self.label_manualDID.setVisible(False)
            self.comboBox_DID.setVisible(True)
            self.label_dropdownDID.setVisible(True)
 
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form_SID2E = QtWidgets.QWidget()
    ui = Ui_Form_SID2E()
    ui.setupUi(Form_SID2E)
    Form_SID2E.show()
    sys.exit(app.exec_())