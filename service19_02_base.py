# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\ass930085\OneDrive - Tata Technologies\Documents\PROXI GIT\reference\ProxiCan\SID_19_02.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form_SID_19_02(object):
    def setupUi(self, Form_SID_19_02):
        Form_SID_19_02.setObjectName("Form_SID_19_02")
        Form_SID_19_02.resize(838, 636)
        self.label_status = QtWidgets.QLabel(Form_SID_19_02)
        self.label_status.setGeometry(QtCore.QRect(10, 550, 821, 71))
        self.label_status.setStyleSheet("background-color: rgb(255, 255, 127);\n"
"color: rgb(85, 0, 0);\n"
"border-color: rgb(0, 0, 255);")
        self.label_status.setAlignment(QtCore.Qt.AlignCenter)
        self.label_status.setWordWrap(True)
        self.label_status.setObjectName("label_status")
        self.layoutWidget = QtWidgets.QWidget(Form_SID_19_02)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 817, 531))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout_2.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_5 = QtWidgets.QLabel(self.layoutWidget)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 7, 0, 1, 1)
        self.label_subFunction = QtWidgets.QLabel(self.layoutWidget)
        self.label_subFunction.setObjectName("label_subFunction")
        self.gridLayout_2.addWidget(self.label_subFunction, 0, 0, 1, 1)
        self.DTCStatusMask_label = QtWidgets.QLabel(self.layoutWidget)
        self.DTCStatusMask_label.setObjectName("DTCStatusMask_label")
        self.gridLayout_2.addWidget(self.DTCStatusMask_label, 3, 0, 4, 1)
        self.label_ResType = QtWidgets.QLabel(self.layoutWidget)
        self.label_ResType.setAutoFillBackground(False)
        self.label_ResType.setStyleSheet("color: rgb(0, 0, 255);")
        self.label_ResType.setAlignment(QtCore.Qt.AlignCenter)
        self.label_ResType.setObjectName("label_ResType")
        self.gridLayout_2.addWidget(self.label_ResType, 7, 1, 1, 2)
        self.pushButton_appendLog = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_appendLog.setStyleSheet("background-color: rgb(85, 255, 127);\n"
"color: rgb(85, 0, 0);")
        self.pushButton_appendLog.setObjectName("pushButton_appendLog")
        self.gridLayout_2.addWidget(self.pushButton_appendLog, 7, 4, 1, 1)
        self.comboBox_DTCStatusMask_entryType = QtWidgets.QComboBox(self.layoutWidget)
        self.comboBox_DTCStatusMask_entryType.setObjectName("comboBox_DTCStatusMask_entryType")
        self.comboBox_DTCStatusMask_entryType.addItem("")
        self.comboBox_DTCStatusMask_entryType.addItem("")
        self.gridLayout_2.addWidget(self.comboBox_DTCStatusMask_entryType, 1, 1, 1, 3)
        self.pushButton_reset = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_reset.setStyleSheet("background-color: rgb(170, 170, 0);\n"
"font: 75 8pt \"MS Shell Dlg 2\";\n"
"color: rgb(0, 85, 0);")
        self.pushButton_reset.setObjectName("pushButton_reset")
        self.gridLayout_2.addWidget(self.pushButton_reset, 10, 4, 1, 1)
        self.pushButton_clearLog = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_clearLog.setStyleSheet("background-color: rgb(85, 255, 127);\n"
"color: rgb(85, 0, 0);")
        self.pushButton_clearLog.setObjectName("pushButton_clearLog")
        self.gridLayout_2.addWidget(self.pushButton_clearLog, 7, 3, 1, 1)
        self.pushButton_Send19_02Req = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_Send19_02Req.setStyleSheet("background-color: rgb(0, 255, 255);\n"
"border-color: rgb(0, 0, 0);\n"
"color: rgb(0, 0, 0);")
        self.pushButton_Send19_02Req.setObjectName("pushButton_Send19_02Req")
        self.gridLayout_2.addWidget(self.pushButton_Send19_02Req, 0, 4, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.checkBox_statusMask_bit0 = QtWidgets.QCheckBox(self.layoutWidget)
        self.checkBox_statusMask_bit0.setObjectName("checkBox_statusMask_bit0")
        self.horizontalLayout.addWidget(self.checkBox_statusMask_bit0)
        self.checkBox_statusMask_bit1 = QtWidgets.QCheckBox(self.layoutWidget)
        self.checkBox_statusMask_bit1.setObjectName("checkBox_statusMask_bit1")
        self.horizontalLayout.addWidget(self.checkBox_statusMask_bit1)
        self.gridLayout_2.addLayout(self.horizontalLayout, 3, 1, 1, 4)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.checkBox_statusMask_bit2 = QtWidgets.QCheckBox(self.layoutWidget)
        self.checkBox_statusMask_bit2.setObjectName("checkBox_statusMask_bit2")
        self.horizontalLayout_2.addWidget(self.checkBox_statusMask_bit2)
        self.checkBox_statusMask_bit3 = QtWidgets.QCheckBox(self.layoutWidget)
        self.checkBox_statusMask_bit3.setObjectName("checkBox_statusMask_bit3")
        self.horizontalLayout_2.addWidget(self.checkBox_statusMask_bit3)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 4, 1, 1, 4)
        self.DTCStatusMask_entryType_label = QtWidgets.QLabel(self.layoutWidget)
        self.DTCStatusMask_entryType_label.setObjectName("DTCStatusMask_entryType_label")
        self.gridLayout_2.addWidget(self.DTCStatusMask_entryType_label, 1, 0, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.checkBox_statusMask_bit4 = QtWidgets.QCheckBox(self.layoutWidget)
        self.checkBox_statusMask_bit4.setObjectName("checkBox_statusMask_bit4")
        self.horizontalLayout_3.addWidget(self.checkBox_statusMask_bit4)
        self.checkBox_statusMask_bit5 = QtWidgets.QCheckBox(self.layoutWidget)
        self.checkBox_statusMask_bit5.setObjectName("checkBox_statusMask_bit5")
        self.horizontalLayout_3.addWidget(self.checkBox_statusMask_bit5)
        self.gridLayout_2.addLayout(self.horizontalLayout_3, 5, 1, 1, 4)
        self.subFunction_Name = QtWidgets.QLabel(self.layoutWidget)
        self.subFunction_Name.setObjectName("subFunction_Name")
        self.gridLayout_2.addWidget(self.subFunction_Name, 0, 1, 1, 2)
        self.checkBox_suppressposmsg = QtWidgets.QCheckBox(self.layoutWidget)
        self.checkBox_suppressposmsg.setObjectName("checkBox_suppressposmsg")
        self.gridLayout_2.addWidget(self.checkBox_suppressposmsg, 0, 3, 1, 1)
        self.textBrowser_Resp = QtWidgets.QTextBrowser(self.layoutWidget)
        self.textBrowser_Resp.setObjectName("textBrowser_Resp")
        self.gridLayout_2.addWidget(self.textBrowser_Resp, 10, 1, 1, 3)
        self.label_4 = QtWidgets.QLabel(self.layoutWidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 10, 0, 1, 1)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.checkBox_statusMask_bit6 = QtWidgets.QCheckBox(self.layoutWidget)
        self.checkBox_statusMask_bit6.setObjectName("checkBox_statusMask_bit6")
        self.horizontalLayout_4.addWidget(self.checkBox_statusMask_bit6)
        self.checkBox_statusMask_bit7 = QtWidgets.QCheckBox(self.layoutWidget)
        self.checkBox_statusMask_bit7.setObjectName("checkBox_statusMask_bit7")
        self.horizontalLayout_4.addWidget(self.checkBox_statusMask_bit7)
        self.gridLayout_2.addLayout(self.horizontalLayout_4, 6, 1, 1, 4)
        self.DTCStatusMask_label_2 = QtWidgets.QLabel(self.layoutWidget)
        self.DTCStatusMask_label_2.setObjectName("DTCStatusMask_label_2")
        self.gridLayout_2.addWidget(self.DTCStatusMask_label_2, 2, 0, 1, 1)
        self.lineEdit_DTCStatusMask = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_DTCStatusMask.setObjectName("lineEdit_DTCStatusMask")
        self.gridLayout_2.addWidget(self.lineEdit_DTCStatusMask, 2, 1, 1, 3)

        self.DTCStatusMask_label_2.hide()
        self.lineEdit_DTCStatusMask.hide()
        self.comboBox_DTCStatusMask_entryType.currentIndexChanged.connect(self.toggle_line_edit)

        self.retranslateUi(Form_SID_19_02)
        QtCore.QMetaObject.connectSlotsByName(Form_SID_19_02)


    def toggle_line_edit(self, index):
        if index == 1: # Option 2 selected (index 1)
                self.DTCStatusMask_label_2.show()
                self.lineEdit_DTCStatusMask.show()
                self.DTCStatusMask_label.hide()
                self._hide_or_show_layout_widgets(self.horizontalLayout, False)
                self._hide_or_show_layout_widgets(self.horizontalLayout_2, False)
                self._hide_or_show_layout_widgets(self.horizontalLayout_3, False)
                self._hide_or_show_layout_widgets(self.horizontalLayout_4, False)
        else : # Option 2 selected (index 1)
                 self.DTCStatusMask_label_2.hide()
                 self.lineEdit_DTCStatusMask.hide()
                 self.DTCStatusMask_label.show()
                 self._hide_or_show_layout_widgets(self.horizontalLayout, True)
                 self._hide_or_show_layout_widgets(self.horizontalLayout_2, True)
                 self._hide_or_show_layout_widgets(self.horizontalLayout_3, True)
                 self._hide_or_show_layout_widgets(self.horizontalLayout_4, True)
    def _hide_or_show_layout_widgets(self, layout, show):
        for i in range(layout.count()):
             widget = layout.itemAt(i).widget()
             if widget:  # Ensure the item is a widget
                  widget.setVisible(show)

    def retranslateUi(self, Form_SID_19_02):
        _translate = QtCore.QCoreApplication.translate
        Form_SID_19_02.setWindowTitle(_translate("Form_SID_19_02", "Report DTC By Status Mask 0x02 "))
        self.label_status.setText(_translate("Form_SID_19_02", "No Status"))
        self.label_5.setText(_translate("Form_SID_19_02", "Response Type: "))
        self.label_subFunction.setText(_translate("Form_SID_19_02", "Sub Function:"))
        self.DTCStatusMask_label.setText(_translate("Form_SID_19_02", "DTC Status Mask:"))
        self.label_ResType.setText(_translate("Form_SID_19_02", "No Response"))
        self.pushButton_appendLog.setText(_translate("Form_SID_19_02", "Add to Log"))
        self.comboBox_DTCStatusMask_entryType.setToolTip(_translate("Form_SID_19_02", "<html><head/><body><p>Select the entry method for DTC Status Mask.</p><p>\'Enable Bitwise Entry\' allows using checkboxes to set specific bits, while \'Enable Manual Entry\' allows direct hexadecimal input.</p></body></html>"))
        self.comboBox_DTCStatusMask_entryType.setItemText(0, _translate("Form_SID_19_02", "Enable Bitwise Entry"))
        self.comboBox_DTCStatusMask_entryType.setItemText(1, _translate("Form_SID_19_02", "Enable Manual Entry"))
        self.pushButton_reset.setText(_translate("Form_SID_19_02", "Reset"))
        self.pushButton_clearLog.setText(_translate("Form_SID_19_02", "Clear Log"))
        self.pushButton_Send19_02Req.setToolTip(_translate("Form_SID_19_02", "<html><head/><body><p>Sends the 19 service subfunction 02 request to ECU</p></body></html>"))
        self.pushButton_Send19_02Req.setText(_translate("Form_SID_19_02", "Send Request"))
        self.checkBox_statusMask_bit0.setToolTip(_translate("Form_SID_19_02", "Selecting this indicates the DTC test has matured as a failure, confirming the fault as present."))
        self.checkBox_statusMask_bit0.setText(_translate("Form_SID_19_02", "Test Failed"))
        self.checkBox_statusMask_bit1.setToolTip(_translate("Form_SID_19_02", "Selecting this indicates the DTC test failed during the current operation cycle."))
        self.checkBox_statusMask_bit1.setText(_translate("Form_SID_19_02", "Test Failed This Operation Cycle"))
        self.checkBox_statusMask_bit2.setToolTip(_translate("Form_SID_19_02", "Selecting this indicates the DTC has failed in the current or previous operation cycle and is pending ."))
        self.checkBox_statusMask_bit2.setText(_translate("Form_SID_19_02", "Pending DTC"))
        self.checkBox_statusMask_bit3.setToolTip(_translate("Form_SID_19_02", "<html><head/><body><p>Selecting this indicates that the fault has been continuously active for a specific monitoring routine and is matured enough in the current operation cycle so that it can be said confirmed. </p></body></html>"))
        self.checkBox_statusMask_bit3.setText(_translate("Form_SID_19_02", "Confirmed DTC"))
        self.DTCStatusMask_entryType_label.setText(_translate("Form_SID_19_02", "DTC Status Mask Entry Type:"))
        self.checkBox_statusMask_bit4.setToolTip(_translate("Form_SID_19_02", "Selecting this indicates the DTC test hasnot completed since the last DTC code clear."))
        self.checkBox_statusMask_bit4.setText(_translate("Form_SID_19_02", "Test Not Completed Since Last Clear"))
        self.checkBox_statusMask_bit5.setToolTip(_translate("Form_SID_19_02", "Selecting this indicates the DTC test has failed at least once since the last code clear."))
        self.checkBox_statusMask_bit5.setText(_translate("Form_SID_19_02", "Test Failed Since Last Clear"))
        self.subFunction_Name.setText(_translate("Form_SID_19_02", "Report DTC By Status Mask 0x02 "))
        self.checkBox_suppressposmsg.setToolTip(_translate("Form_SID_19_02", "If selected then Suppress Positive Response Message Indication bit will be set in Subfunction"))
        self.checkBox_suppressposmsg.setText(_translate("Form_SID_19_02", "SPRMIB"))
        self.label_4.setText(_translate("Form_SID_19_02", "Response : "))
        self.checkBox_statusMask_bit6.setToolTip(_translate("Form_SID_19_02", "Selecting this indicates the DTC test has not completed during this current operation cycle."))
        self.checkBox_statusMask_bit6.setText(_translate("Form_SID_19_02", "Test Not Completed This Operation Cycle"))
        self.checkBox_statusMask_bit7.setToolTip(_translate("Form_SID_19_02", "Selecting this indicates that the server is requesting the warning indicator to be active."))
        self.checkBox_statusMask_bit7.setText(_translate("Form_SID_19_02", "Warning Indicator Requested"))
        self.DTCStatusMask_label_2.setText(_translate("Form_SID_19_02", "DTC Status Mask:"))
        self.lineEdit_DTCStatusMask.setToolTip(_translate("Form_SID_19_02", "Enter the 1-byte DTC Status Mask value in hexadecimal format."))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form_SID_19_02 = QtWidgets.QWidget()
    ui = Ui_Form_SID_19_02()
    ui.setupUi(Form_SID_19_02)
    Form_SID_19_02.show()
    sys.exit(app.exec_())