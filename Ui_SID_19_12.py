# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\ass930085\OneDrive - Tata Technologies\Documents\PROXI GIT\reference\ProxiCan\SID_19_12.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form_SID_19_12(object):
    def setupUi(self, Form_SID_19_12):
        Form_SID_19_12.setObjectName("Form_SID_19_12")
        Form_SID_19_12.resize(842, 636)
        self.label_status = QtWidgets.QLabel(Form_SID_19_12)
        self.label_status.setGeometry(QtCore.QRect(10, 550, 821, 71))
        self.label_status.setStyleSheet("background-color: rgb(255, 255, 127);\n"
"color: rgb(85, 0, 0);\n"
"border-color: rgb(0, 0, 255);")
        self.label_status.setAlignment(QtCore.Qt.AlignCenter)
        self.label_status.setWordWrap(True)
        self.label_status.setObjectName("label_status")
        self.layoutWidget = QtWidgets.QWidget(Form_SID_19_12)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 821, 531))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout_2.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.textBrowser_Resp = QtWidgets.QTextBrowser(self.layoutWidget)
        self.textBrowser_Resp.setObjectName("textBrowser_Resp")
        self.gridLayout_2.addWidget(self.textBrowser_Resp, 8, 1, 1, 3)
        self.pushButton_appendLog = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_appendLog.setStyleSheet("background-color: rgb(85, 255, 127);\n"
"color: rgb(85, 0, 0);")
        self.pushButton_appendLog.setObjectName("pushButton_appendLog")
        self.gridLayout_2.addWidget(self.pushButton_appendLog, 5, 4, 1, 1)
        self.pushButton_clearLog = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_clearLog.setStyleSheet("background-color: rgb(85, 255, 127);\n"
"color: rgb(85, 0, 0);")
        self.pushButton_clearLog.setObjectName("pushButton_clearLog")
        self.gridLayout_2.addWidget(self.pushButton_clearLog, 5, 3, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.layoutWidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 8, 0, 1, 1)
        self.pushButton_reset = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_reset.setStyleSheet("background-color: rgb(170, 170, 0);\n"
"font: 75 8pt \"MS Shell Dlg 2\";\n"
"color: rgb(0, 85, 0);")
        self.pushButton_reset.setObjectName("pushButton_reset")
        self.gridLayout_2.addWidget(self.pushButton_reset, 8, 4, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.layoutWidget)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 5, 0, 1, 1)
        self.label_subFunction = QtWidgets.QLabel(self.layoutWidget)
        self.label_subFunction.setObjectName("label_subFunction")
        self.gridLayout_2.addWidget(self.label_subFunction, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.checkBox_statusMask_bit0 = QtWidgets.QCheckBox(self.layoutWidget)
        self.checkBox_statusMask_bit0.setObjectName("checkBox_statusMask_bit0")
        self.horizontalLayout.addWidget(self.checkBox_statusMask_bit0)
        self.checkBox_statusMask_bit1 = QtWidgets.QCheckBox(self.layoutWidget)
        self.checkBox_statusMask_bit1.setObjectName("checkBox_statusMask_bit1")
        self.horizontalLayout.addWidget(self.checkBox_statusMask_bit1)
        self.gridLayout_2.addLayout(self.horizontalLayout, 1, 1, 1, 4)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.checkBox_statusMask_bit2 = QtWidgets.QCheckBox(self.layoutWidget)
        self.checkBox_statusMask_bit2.setObjectName("checkBox_statusMask_bit2")
        self.horizontalLayout_3.addWidget(self.checkBox_statusMask_bit2)
        self.checkBox_statusMask_bit3 = QtWidgets.QCheckBox(self.layoutWidget)
        self.checkBox_statusMask_bit3.setObjectName("checkBox_statusMask_bit3")
        self.horizontalLayout_3.addWidget(self.checkBox_statusMask_bit3)
        self.gridLayout_2.addLayout(self.horizontalLayout_3, 2, 1, 1, 4)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.checkBox_statusMask_bit4 = QtWidgets.QCheckBox(self.layoutWidget)
        self.checkBox_statusMask_bit4.setObjectName("checkBox_statusMask_bit4")
        self.horizontalLayout_4.addWidget(self.checkBox_statusMask_bit4)
        self.checkBox_statusMask_bit5 = QtWidgets.QCheckBox(self.layoutWidget)
        self.checkBox_statusMask_bit5.setObjectName("checkBox_statusMask_bit5")
        self.horizontalLayout_4.addWidget(self.checkBox_statusMask_bit5)
        self.gridLayout_2.addLayout(self.horizontalLayout_4, 3, 1, 1, 4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.checkBox_statusMask_bit6 = QtWidgets.QCheckBox(self.layoutWidget)
        self.checkBox_statusMask_bit6.setObjectName("checkBox_statusMask_bit6")
        self.horizontalLayout_5.addWidget(self.checkBox_statusMask_bit6)
        self.checkBox_statusMask_bit7 = QtWidgets.QCheckBox(self.layoutWidget)
        self.checkBox_statusMask_bit7.setObjectName("checkBox_statusMask_bit7")
        self.horizontalLayout_5.addWidget(self.checkBox_statusMask_bit7)
        self.gridLayout_2.addLayout(self.horizontalLayout_5, 4, 1, 1, 4)
        self.label_ResType = QtWidgets.QLabel(self.layoutWidget)
        self.label_ResType.setAutoFillBackground(False)
        self.label_ResType.setStyleSheet("color: rgb(0, 0, 255);")
        self.label_ResType.setAlignment(QtCore.Qt.AlignCenter)
        self.label_ResType.setObjectName("label_ResType")
        self.gridLayout_2.addWidget(self.label_ResType, 5, 1, 1, 2)
        self.pushButton_Send19_12Req = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_Send19_12Req.setStyleSheet("background-color: rgb(0, 255, 255);\n"
"border-color: rgb(0, 0, 0);\n"
"color: rgb(0, 0, 0);")
        self.pushButton_Send19_12Req.setObjectName("pushButton_Send19_12Req")
        self.gridLayout_2.addWidget(self.pushButton_Send19_12Req, 0, 4, 1, 1)
        self.checkBox_suppressposmsg = QtWidgets.QCheckBox(self.layoutWidget)
        self.checkBox_suppressposmsg.setObjectName("checkBox_suppressposmsg")
        self.gridLayout_2.addWidget(self.checkBox_suppressposmsg, 0, 3, 1, 1)
        self.subFunction_Name = QtWidgets.QLabel(self.layoutWidget)
        self.subFunction_Name.setObjectName("subFunction_Name")
        self.gridLayout_2.addWidget(self.subFunction_Name, 0, 1, 1, 2)
        self.DTCStatusMask_label = QtWidgets.QLabel(self.layoutWidget)
        self.DTCStatusMask_label.setObjectName("DTCStatusMask_label")
        self.gridLayout_2.addWidget(self.DTCStatusMask_label, 1, 0, 4, 1)

        self.retranslateUi(Form_SID_19_12)
        QtCore.QMetaObject.connectSlotsByName(Form_SID_19_12)

    def retranslateUi(self, Form_SID_19_12):
        _translate = QtCore.QCoreApplication.translate
        Form_SID_19_12.setWindowTitle(_translate("Form_SID_19_12", "Report Number Of Emissions OBDDTC By Status Mask 0x12 "))
        self.label_status.setText(_translate("Form_SID_19_12", "No Status"))
        self.pushButton_appendLog.setText(_translate("Form_SID_19_12", "Add to Log"))
        self.pushButton_clearLog.setText(_translate("Form_SID_19_12", "Clear Log"))
        self.label_4.setText(_translate("Form_SID_19_12", "Response : "))
        self.pushButton_reset.setText(_translate("Form_SID_19_12", "Reset"))
        self.label_5.setText(_translate("Form_SID_19_12", "Response Type: "))
        self.label_subFunction.setText(_translate("Form_SID_19_12", "Sub Function:"))
        self.checkBox_statusMask_bit0.setToolTip(_translate("Form_SID_19_12", "<html><head/><body><p><span style=\" font-family:\'ui-sans-serif\',\'-apple-system\',\'system-ui\',\'Segoe UI\',\'Helvetica\',\'Apple Color Emoji\',\'Arial\',\'sans-serif\',\'Segoe UI Emoji\',\'Segoe UI Symbol\'; font-size:16px; color:#0d0d0d; background-color:#ffffff;\">Selecting this indicates the </span><span style=\" font-family:\'ui-sans-serif\',\'-apple-system\',\'system-ui\',\'Segoe UI\',\'Helvetica\',\'Apple Color Emoji\',\'Arial\',\'sans-serif\',\'Segoe UI Emoji\',\'Segoe UI Symbol\'; font-size:16px; font-weight:600; color:#0d0d0d; background-color:#ffffff;\">DTC test </span><span style=\" font-family:\'ui-sans-serif\',\'-apple-system\',\'system-ui\',\'Segoe UI\',\'Helvetica\',\'Apple Color Emoji\',\'Arial\',\'sans-serif\',\'Segoe UI Emoji\',\'Segoe UI Symbol\'; font-size:16px; color:#0d0d0d; background-color:#ffffff;\">has </span><span style=\" font-family:\'ui-sans-serif\',\'-apple-system\',\'system-ui\',\'Segoe UI\',\'Helvetica\',\'Apple Color Emoji\',\'Arial\',\'sans-serif\',\'Segoe UI Emoji\',\'Segoe UI Symbol\'; font-size:16px; font-weight:600; color:#0d0d0d; background-color:#ffffff;\">matured as a failure</span><span style=\" font-family:\'ui-sans-serif\',\'-apple-system\',\'system-ui\',\'Segoe UI\',\'Helvetica\',\'Apple Color Emoji\',\'Arial\',\'sans-serif\',\'Segoe UI Emoji\',\'Segoe UI Symbol\'; font-size:16px; color:#0d0d0d; background-color:#ffffff;\">, confirming the fault as present.</span></p></body></html>"))
        self.checkBox_statusMask_bit0.setText(_translate("Form_SID_19_12", "Test Failed"))
        self.checkBox_statusMask_bit1.setToolTip(_translate("Form_SID_19_12", "<html><head/><body><p><span style=\" font-family:\'ui-sans-serif\',\'-apple-system\',\'system-ui\',\'Segoe UI\',\'Helvetica\',\'Apple Color Emoji\',\'Arial\',\'sans-serif\',\'Segoe UI Emoji\',\'Segoe UI Symbol\'; font-size:16px; color:#0d0d0d; background-color:#ffffff;\">Selecting this indicates the </span><span style=\" font-family:\'ui-sans-serif\',\'-apple-system\',\'system-ui\',\'Segoe UI\',\'Helvetica\',\'Apple Color Emoji\',\'Arial\',\'sans-serif\',\'Segoe UI Emoji\',\'Segoe UI Symbol\'; font-size:16px; font-weight:600; font-style:italic; color:#0d0d0d; background-color:#ffffff;\">DTC test failed  </span><span style=\" font-family:\'ui-sans-serif\',\'-apple-system\',\'system-ui\',\'Segoe UI\',\'Helvetica\',\'Apple Color Emoji\',\'Arial\',\'sans-serif\',\'Segoe UI Emoji\',\'Segoe UI Symbol\'; font-size:16px; color:#0d0d0d; background-color:#ffffff;\">during the </span><span style=\" font-family:\'ui-sans-serif\',\'-apple-system\',\'system-ui\',\'Segoe UI\',\'Helvetica\',\'Apple Color Emoji\',\'Arial\',\'sans-serif\',\'Segoe UI Emoji\',\'Segoe UI Symbol\'; font-size:16px; font-weight:600; color:#0d0d0d; background-color:#ffffff;\">current operation cycle</span><span style=\" font-family:\'ui-sans-serif\',\'-apple-system\',\'system-ui\',\'Segoe UI\',\'Helvetica\',\'Apple Color Emoji\',\'Arial\',\'sans-serif\',\'Segoe UI Emoji\',\'Segoe UI Symbol\'; font-size:16px; color:#0d0d0d; background-color:#ffffff;\">.</span></p></body></html>"))
        self.checkBox_statusMask_bit1.setText(_translate("Form_SID_19_12", "Test Failed This Operation Cycle"))
        self.checkBox_statusMask_bit2.setToolTip(_translate("Form_SID_19_12", "<html><head/><body><p><span style=\" font-family:\'ui-sans-serif\',\'-apple-system\',\'system-ui\',\'Segoe UI\',\'Helvetica\',\'Apple Color Emoji\',\'Arial\',\'sans-serif\',\'Segoe UI Emoji\',\'Segoe UI Symbol\'; font-size:16px; color:#0d0d0d; background-color:#ffffff;\">Selecting this indicates the DTC has failed in the current or previous operation cycle and is </span><span style=\" font-family:\'ui-sans-serif\',\'-apple-system\',\'system-ui\',\'Segoe UI\',\'Helvetica\',\'Apple Color Emoji\',\'Arial\',\'sans-serif\',\'Segoe UI Emoji\',\'Segoe UI Symbol\'; font-size:16px; font-weight:600; font-style:italic; color:#0d0d0d; background-color:#ffffff;\">pending  .</span></p></body></html>"))
        self.checkBox_statusMask_bit2.setText(_translate("Form_SID_19_12", "Pending DTC"))
        self.checkBox_statusMask_bit3.setToolTip(_translate("Form_SID_19_12", "<html><head/><body><p align=\"justify\"><span style=\" font-family:\'ui-sans-serif\',\'-apple-system\',\'system-ui\',\'Segoe UI\',\'Helvetica\',\'Apple Color Emoji\',\'Arial\',\'sans-serif\',\'Segoe UI Emoji\',\'Segoe UI Symbol\'; font-size:16px; color:#0d0d0d; background-color:#ffffff;\">Selecting this indicates that the fault has been continuously active for a specific monitoring routine and is matured enough in the current operation cycle so that it can be said confirmed. </span></p></body></html>"))
        self.checkBox_statusMask_bit3.setText(_translate("Form_SID_19_12", "Confirmed DTC"))
        self.checkBox_statusMask_bit4.setToolTip(_translate("Form_SID_19_12", "<html><head/><body><p><span style=\" font-family:\'ui-sans-serif\',\'-apple-system\',\'system-ui\',\'Segoe UI\',\'Helvetica\',\'Apple Color Emoji\',\'Arial\',\'sans-serif\',\'Segoe UI Emoji\',\'Segoe UI Symbol\'; font-size:16px; color:#0d0d0d; background-color:#ffffff;\">Selecting this indicates the DTC test has</span><span style=\" font-family:\'ui-sans-serif\',\'-apple-system\',\'system-ui\',\'Segoe UI\',\'Helvetica\',\'Apple Color Emoji\',\'Arial\',\'sans-serif\',\'Segoe UI Emoji\',\'Segoe UI Symbol\'; font-size:16px; font-style:italic; color:#0d0d0d; background-color:#ffffff;\"/><span style=\" font-family:\'ui-sans-serif\',\'-apple-system\',\'system-ui\',\'Segoe UI\',\'Helvetica\',\'Apple Color Emoji\',\'Arial\',\'sans-serif\',\'Segoe UI Emoji\',\'Segoe UI Symbol\'; font-size:16px; font-weight:600; font-style:italic; color:#0d0d0d; background-color:#ffffff;\">not completed </span><span style=\" font-family:\'ui-sans-serif\',\'-apple-system\',\'system-ui\',\'Segoe UI\',\'Helvetica\',\'Apple Color Emoji\',\'Arial\',\'sans-serif\',\'Segoe UI Emoji\',\'Segoe UI Symbol\'; font-size:16px; font-style:italic; color:#0d0d0d; background-color:#ffffff;\">since the last DTC code clear</span><span style=\" font-family:\'ui-sans-serif\',\'-apple-system\',\'system-ui\',\'Segoe UI\',\'Helvetica\',\'Apple Color Emoji\',\'Arial\',\'sans-serif\',\'Segoe UI Emoji\',\'Segoe UI Symbol\'; font-size:16px; color:#0d0d0d; background-color:#ffffff;\">.</span></p></body></html>"))
        self.checkBox_statusMask_bit4.setText(_translate("Form_SID_19_12", "Test Not Completed Since Last Clear"))
        self.checkBox_statusMask_bit5.setToolTip(_translate("Form_SID_19_12", "<html><head/><body><p><span style=\" font-family:\'ui-sans-serif\',\'-apple-system\',\'system-ui\',\'Segoe UI\',\'Helvetica\',\'Apple Color Emoji\',\'Arial\',\'sans-serif\',\'Segoe UI Emoji\',\'Segoe UI Symbol\'; font-size:16px; color:#0d0d0d; background-color:#ffffff;\">Selecting this indicates the DTC test</span><span style=\" font-family:\'ui-sans-serif\',\'-apple-system\',\'system-ui\',\'Segoe UI\',\'Helvetica\',\'Apple Color Emoji\',\'Arial\',\'sans-serif\',\'Segoe UI Emoji\',\'Segoe UI Symbol\'; font-size:16px; font-style:italic; color:#0d0d0d; background-color:#ffffff;\"> has </span><span style=\" font-family:\'ui-sans-serif\',\'-apple-system\',\'system-ui\',\'Segoe UI\',\'Helvetica\',\'Apple Color Emoji\',\'Arial\',\'sans-serif\',\'Segoe UI Emoji\',\'Segoe UI Symbol\'; font-size:16px; font-weight:600; font-style:italic; color:#0d0d0d; background-color:#ffffff;\">failed </span><span style=\" font-family:\'ui-sans-serif\',\'-apple-system\',\'system-ui\',\'Segoe UI\',\'Helvetica\',\'Apple Color Emoji\',\'Arial\',\'sans-serif\',\'Segoe UI Emoji\',\'Segoe UI Symbol\'; font-size:16px; font-style:italic; color:#0d0d0d; background-color:#ffffff;\">at least once since the last code clear.</span></p></body></html>"))
        self.checkBox_statusMask_bit5.setText(_translate("Form_SID_19_12", "Test Failed Since Last Clear"))
        self.checkBox_statusMask_bit6.setToolTip(_translate("Form_SID_19_12", "<html><head/><body><p><span style=\" font-family:\'ui-sans-serif\',\'-apple-system\',\'system-ui\',\'Segoe UI\',\'Helvetica\',\'Apple Color Emoji\',\'Arial\',\'sans-serif\',\'Segoe UI Emoji\',\'Segoe UI Symbol\'; font-size:16px; color:#0d0d0d; background-color:#ffffff;\">Selecting this indicates the DTC test has </span><span style=\" font-family:\'ui-sans-serif\',\'-apple-system\',\'system-ui\',\'Segoe UI\',\'Helvetica\',\'Apple Color Emoji\',\'Arial\',\'sans-serif\',\'Segoe UI Emoji\',\'Segoe UI Symbol\'; font-size:16px; font-weight:600; font-style:italic; color:#0d0d0d; background-color:#ffffff;\">not completed </span><span style=\" font-family:\'ui-sans-serif\',\'-apple-system\',\'system-ui\',\'Segoe UI\',\'Helvetica\',\'Apple Color Emoji\',\'Arial\',\'sans-serif\',\'Segoe UI Emoji\',\'Segoe UI Symbol\'; font-size:16px; font-style:italic; color:#0d0d0d; background-color:#ffffff;\">during this  current operation cycle.</span></p></body></html>"))
        self.checkBox_statusMask_bit6.setText(_translate("Form_SID_19_12", "Test Not Completed This Operation Cycle"))
        self.checkBox_statusMask_bit7.setToolTip(_translate("Form_SID_19_12", "<html><head/><body><p><span style=\" font-family:\'ui-sans-serif\',\'-apple-system\',\'system-ui\',\'Segoe UI\',\'Helvetica\',\'Apple Color Emoji\',\'Arial\',\'sans-serif\',\'Segoe UI Emoji\',\'Segoe UI Symbol\'; font-size:16px; color:#0d0d0d; background-color:#ffffff;\">Selecting this indicates that the server is requesting the </span><span style=\" font-family:\'ui-sans-serif\',\'-apple-system\',\'system-ui\',\'Segoe UI\',\'Helvetica\',\'Apple Color Emoji\',\'Arial\',\'sans-serif\',\'Segoe UI Emoji\',\'Segoe UI Symbol\'; font-size:16px; font-weight:600; font-style:italic; color:#0d0d0d; background-color:#ffffff;\">warning indicator </span><span style=\" font-family:\'ui-sans-serif\',\'-apple-system\',\'system-ui\',\'Segoe UI\',\'Helvetica\',\'Apple Color Emoji\',\'Arial\',\'sans-serif\',\'Segoe UI Emoji\',\'Segoe UI Symbol\'; font-size:16px; font-style:italic; color:#0d0d0d; background-color:#ffffff;\"> to be active.</span></p></body></html>"))
        self.checkBox_statusMask_bit7.setText(_translate("Form_SID_19_12", "Warning Indicator Requested"))
        self.label_ResType.setText(_translate("Form_SID_19_12", "No Response"))
        self.pushButton_Send19_12Req.setToolTip(_translate("Form_SID_19_12", "<html><head/><body><p>Sends the 19 service subfunction 12 request to ECU</p></body></html>"))
        self.pushButton_Send19_12Req.setText(_translate("Form_SID_19_12", "Send Request"))
        self.checkBox_suppressposmsg.setToolTip(_translate("Form_SID_19_12", "If selected then Suppress Positive Response Message Indication bit will be set in Subfunction"))
        self.checkBox_suppressposmsg.setText(_translate("Form_SID_19_12", "SPRMIB"))
        self.subFunction_Name.setText(_translate("Form_SID_19_12", "Report Number Of Emissions OBDDTC By Status Mask 0x12 "))
        self.DTCStatusMask_label.setText(_translate("Form_SID_19_12", "DTC Status Mask:"))