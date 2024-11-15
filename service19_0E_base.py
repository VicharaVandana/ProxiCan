# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\ass930085\OneDrive - Tata Technologies\Documents\PROXI GIT\reference\ProxiCan\SID_19_0E.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form_SID_19_0E(object):
    def setupUi(self, Form_SID_19_0E):
        Form_SID_19_0E.setObjectName("Form_SID_19_0E")
        Form_SID_19_0E.resize(848, 638)
        self.layoutWidget = QtWidgets.QWidget(Form_SID_19_0E)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 821, 531))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout_2.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_subFunction = QtWidgets.QLabel(self.layoutWidget)
        self.label_subFunction.setObjectName("label_subFunction")
        self.gridLayout_2.addWidget(self.label_subFunction, 0, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.layoutWidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 5, 0, 1, 1)
        self.textBrowser_Resp = QtWidgets.QTextBrowser(self.layoutWidget)
        self.textBrowser_Resp.setObjectName("textBrowser_Resp")
        self.gridLayout_2.addWidget(self.textBrowser_Resp, 5, 1, 1, 4)
        self.pushButton_clearLog = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_clearLog.setStyleSheet("background-color: rgb(85, 255, 127);\n"
"color: rgb(85, 0, 0);")
        self.pushButton_clearLog.setObjectName("pushButton_clearLog")
        self.gridLayout_2.addWidget(self.pushButton_clearLog, 1, 2, 1, 1)
        self.pushButton_Send19_0EReq = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_Send19_0EReq.setStyleSheet("background-color: rgb(0, 255, 255);\n"
"border-color: rgb(0, 0, 0);\n"
"color: rgb(0, 0, 0);")
        self.pushButton_Send19_0EReq.setObjectName("pushButton_Send19_0EReq")
        self.gridLayout_2.addWidget(self.pushButton_Send19_0EReq, 1, 1, 1, 1)
        self.pushButton_reset = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_reset.setStyleSheet("background-color: rgb(170, 170, 0);\n"
"font: 75 8pt \"MS Shell Dlg 2\";\n"
"color: rgb(0, 85, 0);")
        self.pushButton_reset.setObjectName("pushButton_reset")
        self.gridLayout_2.addWidget(self.pushButton_reset, 1, 4, 1, 1)
        self.pushButton_appendLog = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_appendLog.setStyleSheet("background-color: rgb(85, 255, 127);\n"
"color: rgb(85, 0, 0);")
        self.pushButton_appendLog.setObjectName("pushButton_appendLog")
        self.gridLayout_2.addWidget(self.pushButton_appendLog, 1, 3, 1, 1)
        self.checkBox_suppressposmsg = QtWidgets.QCheckBox(self.layoutWidget)
        self.checkBox_suppressposmsg.setObjectName("checkBox_suppressposmsg")
        self.gridLayout_2.addWidget(self.checkBox_suppressposmsg, 0, 4, 1, 1)
        self.subFunction_Name = QtWidgets.QLabel(self.layoutWidget)
        self.subFunction_Name.setObjectName("subFunction_Name")
        self.gridLayout_2.addWidget(self.subFunction_Name, 0, 1, 1, 3)
        self.label_5 = QtWidgets.QLabel(self.layoutWidget)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 2, 0, 3, 1)
        self.label_ResType = QtWidgets.QLabel(self.layoutWidget)
        self.label_ResType.setAutoFillBackground(False)
        self.label_ResType.setStyleSheet("color: rgb(0, 0, 255);")
        self.label_ResType.setAlignment(QtCore.Qt.AlignCenter)
        self.label_ResType.setObjectName("label_ResType")
        self.gridLayout_2.addWidget(self.label_ResType, 2, 1, 3, 4)
        self.label_status = QtWidgets.QLabel(Form_SID_19_0E)
        self.label_status.setGeometry(QtCore.QRect(10, 550, 821, 71))
        self.label_status.setStyleSheet("background-color: rgb(255, 255, 127);\n"
"color: rgb(85, 0, 0);\n"
"border-color: rgb(0, 0, 255);")
        self.label_status.setAlignment(QtCore.Qt.AlignCenter)
        self.label_status.setWordWrap(True)
        self.label_status.setObjectName("label_status")

        self.retranslateUi(Form_SID_19_0E)
        QtCore.QMetaObject.connectSlotsByName(Form_SID_19_0E)

    def retranslateUi(self, Form_SID_19_0E):
        _translate = QtCore.QCoreApplication.translate
        Form_SID_19_0E.setWindowTitle(_translate("Form_SID_19_0E", "Report Most Recent Confirmed DTC"))
        self.label_subFunction.setText(_translate("Form_SID_19_0E", "Sub Function:"))
        self.label_4.setText(_translate("Form_SID_19_0E", "          Response : "))
        self.pushButton_clearLog.setText(_translate("Form_SID_19_0E", "Clear Log"))
        self.pushButton_Send19_0EReq.setToolTip(_translate("Form_SID_19_0E", "<html><head/><body><p>Sends the 19 service subfunction 0E request to ECU</p></body></html>"))
        self.pushButton_Send19_0EReq.setText(_translate("Form_SID_19_0E", "Send Request"))
        self.pushButton_reset.setText(_translate("Form_SID_19_0E", "Reset"))
        self.pushButton_appendLog.setText(_translate("Form_SID_19_0E", "Add to Log"))
        self.checkBox_suppressposmsg.setToolTip(_translate("Form_SID_19_0E", "If selected then Suppress Positive Response Message Indication bit will be set in Subfunction"))
        self.checkBox_suppressposmsg.setText(_translate("Form_SID_19_0E", "SPRMIB"))
        self.subFunction_Name.setText(_translate("Form_SID_19_0E", "Report Most Recent Confirmed DTC 0x0E"))
        self.label_5.setText(_translate("Form_SID_19_0E", "Response Type: "))
        self.label_ResType.setText(_translate("Form_SID_19_0E", "No Response"))
        self.label_status.setText(_translate("Form_SID_19_0E", "No Status"))
