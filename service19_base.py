# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SID_19.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form_SID_19(object):
    def setupUi(self, Form_SID_19):
        Form_SID_19.setObjectName("Form_SID_19")
        Form_SID_19.resize(797, 597)
        self.layoutWidget = QtWidgets.QWidget(Form_SID_19)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 771, 481))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout_2.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.Subfunction_label = QtWidgets.QLabel(self.layoutWidget)
        self.Subfunction_label.setObjectName("Subfunction_label")
        self.gridLayout_2.addWidget(self.Subfunction_label, 0, 0, 1, 1)
        self.pushButton_Send19Req = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_Send19Req.setStyleSheet("background-color: rgb(0, 255, 255);\n"
"border-color: rgb(0, 0, 0);\n"
"color: rgb(0, 0, 0);")
        self.pushButton_Send19Req.setObjectName("pushButton_Send19Req")
        self.gridLayout_2.addWidget(self.pushButton_Send19Req, 0, 2, 1, 2)
        self.DTCExtDataRecordNumber_label = QtWidgets.QLabel(self.layoutWidget)
        self.DTCExtDataRecordNumber_label.setObjectName("DTCExtDataRecordNumber_label")
        self.gridLayout_2.addWidget(self.DTCExtDataRecordNumber_label, 4, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.layoutWidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 9, 0, 1, 1)
        self.checkBox_suppressposmsg = QtWidgets.QCheckBox(self.layoutWidget)
        self.checkBox_suppressposmsg.setObjectName("checkBox_suppressposmsg")
        self.gridLayout_2.addWidget(self.checkBox_suppressposmsg, 1, 3, 1, 1)
        self.pushButton_reset = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_reset.setStyleSheet("background-color: rgb(170, 170, 0);\n"
"font: 75 8pt \"MS Shell Dlg 2\";\n"
"color: rgb(0, 85, 0);")
        self.pushButton_reset.setObjectName("pushButton_reset")
        self.gridLayout_2.addWidget(self.pushButton_reset, 9, 3, 1, 1)
        self.lineEdit_DTCStatusMask = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_DTCStatusMask.setObjectName("lineEdit_DTCStatusMask")
        self.gridLayout_2.addWidget(self.lineEdit_DTCStatusMask, 1, 1, 1, 1)
        self.lineEdit_ExtDataRecordNumber = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_ExtDataRecordNumber.setObjectName("lineEdit_ExtDataRecordNumber")
        self.gridLayout_2.addWidget(self.lineEdit_ExtDataRecordNumber, 4, 1, 1, 1)
        self.DTCSnapshotRecordNumber_label = QtWidgets.QLabel(self.layoutWidget)
        self.DTCSnapshotRecordNumber_label.setObjectName("DTCSnapshotRecordNumber_label")
        self.gridLayout_2.addWidget(self.DTCSnapshotRecordNumber_label, 3, 0, 1, 1)
        self.DTCMaskRecord_label = QtWidgets.QLabel(self.layoutWidget)
        self.DTCMaskRecord_label.setObjectName("DTCMaskRecord_label")
        self.gridLayout_2.addWidget(self.DTCMaskRecord_label, 2, 0, 1, 1)
        self.label_ResType = QtWidgets.QLabel(self.layoutWidget)
        self.label_ResType.setAutoFillBackground(False)
        self.label_ResType.setStyleSheet("color: rgb(0, 0, 255);")
        self.label_ResType.setAlignment(QtCore.Qt.AlignCenter)
        self.label_ResType.setObjectName("label_ResType")
        self.gridLayout_2.addWidget(self.label_ResType, 6, 1, 1, 1)
        self.lineEdit_DTCMaskRecord = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_DTCMaskRecord.setObjectName("lineEdit_DTCMaskRecord")
        self.gridLayout_2.addWidget(self.lineEdit_DTCMaskRecord, 2, 1, 1, 1)
        self.pushButton_clearLog = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_clearLog.setStyleSheet("background-color: rgb(85, 255, 127);\n"
"color: rgb(85, 0, 0);")
        self.pushButton_clearLog.setObjectName("pushButton_clearLog")
        self.gridLayout_2.addWidget(self.pushButton_clearLog, 6, 2, 1, 1)
        self.textBrowser_Resp = QtWidgets.QTextBrowser(self.layoutWidget)
        self.textBrowser_Resp.setObjectName("textBrowser_Resp")
        self.gridLayout_2.addWidget(self.textBrowser_Resp, 9, 1, 1, 2)
        self.lineEdit_DTCSnapshotRecordNumber = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_DTCSnapshotRecordNumber.setObjectName("lineEdit_DTCSnapshotRecordNumber")
        self.gridLayout_2.addWidget(self.lineEdit_DTCSnapshotRecordNumber, 3, 1, 1, 1)
        self.pushButton_appendLog = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_appendLog.setStyleSheet("background-color: rgb(85, 255, 127);\n"
"color: rgb(85, 0, 0);")
        self.pushButton_appendLog.setObjectName("pushButton_appendLog")
        self.gridLayout_2.addWidget(self.pushButton_appendLog, 6, 3, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.layoutWidget)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 6, 0, 1, 1)
        self.DTCStatusMask_label = QtWidgets.QLabel(self.layoutWidget)
        self.DTCStatusMask_label.setObjectName("DTCStatusMask_label")
        self.gridLayout_2.addWidget(self.DTCStatusMask_label, 1, 0, 1, 1)
        self.Subfunction = QtWidgets.QComboBox(self.layoutWidget)
        self.Subfunction.setMinimumSize(QtCore.QSize(220, 0))
        self.Subfunction.setMaximumSize(QtCore.QSize(360, 16777215))
        self.Subfunction.setObjectName("Subfunction")
        self.Subfunction.addItem("")
        self.Subfunction.addItem("")
        self.Subfunction.addItem("")
        self.Subfunction.addItem("")
        self.Subfunction.addItem("")
        self.Subfunction.addItem("")
        self.Subfunction.addItem("")
        self.Subfunction.addItem("")
        self.Subfunction.addItem("")
        self.Subfunction.addItem("")
        self.gridLayout_2.addWidget(self.Subfunction, 0, 1, 1, 1)
        self.DTCSeverityMaskRecord = QtWidgets.QLabel(self.layoutWidget)
        self.DTCSeverityMaskRecord.setObjectName("DTCSeverityMaskRecord")
        self.gridLayout_2.addWidget(self.DTCSeverityMaskRecord, 5, 0, 1, 1)
        self.lineEdit_SeverityMaskRecord = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_SeverityMaskRecord.setObjectName("lineEdit_SeverityMaskRecord")
        self.gridLayout_2.addWidget(self.lineEdit_SeverityMaskRecord, 5, 1, 1, 1)
        self.label_status = QtWidgets.QLabel(Form_SID_19)
        self.label_status.setGeometry(QtCore.QRect(10, 500, 771, 71))
        self.label_status.setStyleSheet("background-color: rgb(255, 255, 127);\n"
"color: rgb(85, 0, 0);\n"
"border-color: rgb(0, 0, 255);")
        self.label_status.setAlignment(QtCore.Qt.AlignCenter)
        self.label_status.setWordWrap(True)
        self.label_status.setObjectName("label_status")

        self.DTCMaskRecord_label.hide()
        self.lineEdit_DTCMaskRecord.hide()
        self.DTCSnapshotRecordNumber_label.hide()
        self.lineEdit_DTCSnapshotRecordNumber.hide()
        self.DTCExtDataRecordNumber_label.hide()
        self.lineEdit_ExtDataRecordNumber.hide()
        self.DTCSeverityMaskRecord.hide()
        self.lineEdit_SeverityMaskRecord.hide()
        self.retranslateUi(Form_SID_19)
        self.Subfunction.currentIndexChanged.connect(self.toggle_line_edit)
        QtCore.QMetaObject.connectSlotsByName(Form_SID_19)

    def toggle_line_edit(self, index):
        if index == 0 or index==1:  # Option 2 selected (index 1)
            self.lineEdit_DTCStatusMask.show()
            self.DTCStatusMask_label.show()
             #hide
            self.DTCMaskRecord_label.hide()
            self.lineEdit_DTCMaskRecord.hide()
            self.DTCSnapshotRecordNumber_label.hide()
            self.lineEdit_DTCSnapshotRecordNumber.hide()
            self.DTCExtDataRecordNumber_label.hide()
            self.lineEdit_ExtDataRecordNumber.hide()
            self.DTCSeverityMaskRecord.hide()
            self.lineEdit_SeverityMaskRecord.hide()        
        elif index==2:
            self.lineEdit_DTCMaskRecord.show()
            self.DTCMaskRecord_label.show()
            self.DTCSnapshotRecordNumber_label.show()
            self.lineEdit_DTCSnapshotRecordNumber.show()
            #hide
            self.lineEdit_DTCStatusMask.hide()
            self.DTCStatusMask_label.hide()     
            self.DTCExtDataRecordNumber_label.hide()
            self.lineEdit_ExtDataRecordNumber.hide()
            self.DTCSeverityMaskRecord.hide()
            self.lineEdit_SeverityMaskRecord.hide()        
        elif index==3:
            self.lineEdit_DTCMaskRecord.show()
            self.DTCMaskRecord_label.show()
            self.lineEdit_ExtDataRecordNumber.show()
            self.DTCExtDataRecordNumber_label.show()  
            #hide
            self.lineEdit_DTCStatusMask.hide()
            self.DTCStatusMask_label.hide()  
            self.DTCSnapshotRecordNumber_label.hide()
            self.lineEdit_DTCSnapshotRecordNumber.hide()
            self.DTCSeverityMaskRecord.hide()
            self.lineEdit_SeverityMaskRecord.hide()  
        elif index==4 or index==5:
            self.lineEdit_SeverityMaskRecord.show()
            self.DTCSeverityMaskRecord.show()
            #hide
            self.lineEdit_DTCStatusMask.hide()
            self.DTCStatusMask_label.hide() 
            self.DTCMaskRecord_label.hide()
            self.lineEdit_DTCMaskRecord.hide()
            self.DTCSnapshotRecordNumber_label.hide()
            self.lineEdit_DTCSnapshotRecordNumber.hide()
            self.DTCExtDataRecordNumber_label.hide()
            self.lineEdit_ExtDataRecordNumber.hide()
        elif index==6:
            self.lineEdit_DTCMaskRecord.show()
            self.DTCMaskRecord_label.show()
            #hide
            self.lineEdit_DTCStatusMask.hide()
            self.DTCStatusMask_label.hide() 
            self.DTCSnapshotRecordNumber_label.hide()
            self.lineEdit_DTCSnapshotRecordNumber.hide()
            self.DTCExtDataRecordNumber_label.hide()
            self.lineEdit_ExtDataRecordNumber.hide()
            self.DTCSeverityMaskRecord.hide()
            self.lineEdit_SeverityMaskRecord.hide() 
        else:
            self.lineEdit_DTCStatusMask.hide()
            self.DTCStatusMask_label.hide() 
            self.lineEdit_DTCMaskRecord.hide()
            self.DTCMaskRecord_label.hide()       
            self.DTCSnapshotRecordNumber_label.hide()
            self.lineEdit_DTCSnapshotRecordNumber.hide()
            self.DTCExtDataRecordNumber_label.hide()
            self.lineEdit_ExtDataRecordNumber.hide()
            self.DTCSeverityMaskRecord.hide()
            self.lineEdit_SeverityMaskRecord.hide()  

    def retranslateUi(self, Form_SID_19):
        _translate = QtCore.QCoreApplication.translate
        Form_SID_19.setWindowTitle(_translate("Form_SID_19", "Clear DTC Service 19 "))
        self.Subfunction_label.setText(_translate("Form_SID_19", "Sub Function"))
        self.pushButton_Send19Req.setToolTip(_translate("Form_SID_19", "<html><head/><body><p>Sends the 19 service request to ECU</p></body></html>"))
        self.pushButton_Send19Req.setText(_translate("Form_SID_19", "Send Request"))
        self.DTCExtDataRecordNumber_label.setText(_translate("Form_SID_19", "DTC ExtData Record Number"))
        self.label_4.setText(_translate("Form_SID_19", "Response : "))
        self.checkBox_suppressposmsg.setToolTip(_translate("Form_SID_19", "If selected then Suppress Positive Response Message Indication bit will be set in Subfunction"))
        self.checkBox_suppressposmsg.setText(_translate("Form_SID_19", "SPRMIB"))
        self.pushButton_reset.setText(_translate("Form_SID_19", "Reset"))
        self.lineEdit_DTCStatusMask.setToolTip(_translate("Form_SID_19", "<html><head/><body><p>Enter DTC Status Mask in hexadecimal format</p></body></html>"))
        self.lineEdit_ExtDataRecordNumber.setToolTip(_translate("Form_SID_19", "<html><head/><body><p>mEnter DTC External Data Record Number in hexadecimal format</p></body></html>"))
        self.DTCSnapshotRecordNumber_label.setText(_translate("Form_SID_19", "DTC Snapshot Record Number"))
        self.DTCMaskRecord_label.setText(_translate("Form_SID_19", "DTC Mask Record"))
        self.label_ResType.setText(_translate("Form_SID_19", "No Response"))
        self.lineEdit_DTCMaskRecord.setToolTip(_translate("Form_SID_19", "<html><head/><body><p>Enter DTC Mask Record in hexadecimal format</p></body></html>"))
        self.pushButton_clearLog.setText(_translate("Form_SID_19", "Clear Log"))
        self.lineEdit_DTCSnapshotRecordNumber.setToolTip(_translate("Form_SID_19", "<html><head/><body><p>Enter DTC Snapshot Record Number in hexadecimal format</p></body></html>"))
        self.pushButton_appendLog.setText(_translate("Form_SID_19", "Add to Log"))
        self.label_5.setText(_translate("Form_SID_19", "Response Type: "))
        self.DTCStatusMask_label.setText(_translate("Form_SID_19", "DTC Status Mask"))
        self.Subfunction.setToolTip(_translate("Form_SID_19", "<html><head/><body><p>Select the Sub function to which you want ECU to move. </p><p>If your sub function is not in list then contact admin</p></body></html>"))
        self.Subfunction.setItemText(0, _translate("Form_SID_19", "01 - Report Number of DTC by Status Mask"))
        self.Subfunction.setItemText(1, _translate("Form_SID_19", "02 - Report DTC by Status Mask"))
        self.Subfunction.setItemText(2, _translate("Form_SID_19", "04 - Report DTC Snapshot Record by DTC Number"))
        self.Subfunction.setItemText(3, _translate("Form_SID_19", "06 - Report DTC ExtData Record by DTC Number"))
        self.Subfunction.setItemText(4, _translate("Form_SID_19", "07 - Report Number of DTC by Severity Mask Record"))
        self.Subfunction.setItemText(5, _translate("Form_SID_19", "08 - Report DTC by Severity Mask Record"))
        self.Subfunction.setItemText(6, _translate("Form_SID_19", "09 - Report Severity Information of DTC"))
        self.Subfunction.setItemText(7, _translate("Form_SID_19", "0A - Report Supported DTC"))
        self.Subfunction.setItemText(8, _translate("Form_SID_19", "0C - Report First Confirmed DTC"))
        self.Subfunction.setItemText(9, _translate("Form_SID_19", "0E - Report Most Recent Confirmed DTC"))
        self.DTCSeverityMaskRecord.setText(_translate("Form_SID_19", "DTC Severity Mask Record"))
        self.lineEdit_SeverityMaskRecord.setToolTip(_translate("Form_SID_19", "<html><head/><body><p>Enter DTC Severity Mask Record in hexadecimal format</p></body></html>"))
        self.label_status.setText(_translate("Form_SID_19", "No Status"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form_SID_19 = QtWidgets.QDialog()
    ui = Ui_Form_SID_19()
    ui.setupUi(Form_SID_19)
    Form_SID_19.show()
    sys.exit(app.exec_())
