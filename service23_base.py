# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SID_23.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form_SID_23(object):
    def setupUi(self, Form_SID_23):
        Form_SID_23.setObjectName("Form_SID_23")
        Form_SID_23.resize(866, 567)
        self.label_status = QtWidgets.QLabel(Form_SID_23)
        self.label_status.setGeometry(QtCore.QRect(80, 480, 591, 51))
        self.label_status.setStyleSheet("background-color: rgb(255, 255, 127);\n"
"color: rgb(85, 0, 0);\n"
"border-color: rgb(0, 0, 255);")
        self.label_status.setAlignment(QtCore.Qt.AlignCenter)
        self.label_status.setWordWrap(True)
        self.label_status.setObjectName("label_status")
        self.layoutWidget = QtWidgets.QWidget(Form_SID_23)
        self.layoutWidget.setGeometry(QtCore.QRect(80, 70, 591, 401))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout_2.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_5 = QtWidgets.QLabel(self.layoutWidget)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 3, 0, 1, 1)
        self.pushButton_appendLog_2 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_appendLog_2.setStyleSheet("background-color: rgb(85, 255, 127);\n"
"color: rgb(85, 0, 0);")
        self.pushButton_appendLog_2.setObjectName("pushButton_appendLog_2")
        self.gridLayout_2.addWidget(self.pushButton_appendLog_2, 3, 3, 1, 1)
        self.pushButton_Send23Req_2 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_Send23Req_2.setStyleSheet("background-color: rgb(0, 255, 255);\n"
"border-color: rgb(0, 0, 0);\n"
"color: rgb(0, 0, 0);")
        self.pushButton_Send23Req_2.setObjectName("pushButton_Send23Req_2")
        self.gridLayout_2.addWidget(self.pushButton_Send23Req_2, 0, 2, 1, 2)
        self.label_4 = QtWidgets.QLabel(self.layoutWidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 6, 0, 1, 1)
        self.lineEdit_ALFID = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_ALFID.setObjectName("lineEdit_ALFID")
        self.gridLayout_2.addWidget(self.lineEdit_ALFID, 0, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.layoutWidget)
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 0, 0, 1, 1)
        self.lineEdit_Mem_address = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_Mem_address.setObjectName("lineEdit_Mem_address")
        self.gridLayout_2.addWidget(self.lineEdit_Mem_address, 1, 1, 1, 1)
        self.label_ResType_2 = QtWidgets.QLabel(self.layoutWidget)
        self.label_ResType_2.setAutoFillBackground(False)
        self.label_ResType_2.setStyleSheet("color: rgb(0, 0, 255);")
        self.label_ResType_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_ResType_2.setObjectName("label_ResType_2")
        self.gridLayout_2.addWidget(self.label_ResType_2, 3, 1, 1, 1)
        self.pushButton_reset_2 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_reset_2.setStyleSheet("background-color: rgb(170, 170, 0);\n"
"font: 75 8pt \"MS Shell Dlg 2\";\n"
"color: rgb(0, 85, 0);")
        self.pushButton_reset_2.setObjectName("pushButton_reset_2")
        self.gridLayout_2.addWidget(self.pushButton_reset_2, 6, 3, 1, 1)
        self.pushButton_clearLog_2 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_clearLog_2.setStyleSheet("background-color: rgb(85, 255, 127);\n"
"color: rgb(85, 0, 0);")
        self.pushButton_clearLog_2.setObjectName("pushButton_clearLog_2")
        self.gridLayout_2.addWidget(self.pushButton_clearLog_2, 3, 2, 1, 1)
        self.textBrowser_Resp_2 = QtWidgets.QTextBrowser(self.layoutWidget)
        self.textBrowser_Resp_2.setObjectName("textBrowser_Resp_2")
        self.gridLayout_2.addWidget(self.textBrowser_Resp_2, 6, 1, 1, 2)
        self.lineEdit_Mem_size = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_Mem_size.setObjectName("lineEdit_Mem_size")
        self.gridLayout_2.addWidget(self.lineEdit_Mem_size, 2, 1, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.layoutWidget)
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 2, 0, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.layoutWidget)
        self.label_8.setObjectName("label_8")
        self.gridLayout_2.addWidget(self.label_8, 1, 0, 1, 1)

        self.retranslateUi(Form_SID_23)
        QtCore.QMetaObject.connectSlotsByName(Form_SID_23)

    def retranslateUi(self, Form_SID_23):
        _translate = QtCore.QCoreApplication.translate
        Form_SID_23.setWindowTitle(_translate("Form_SID_23", "Dialog"))
        self.label_status.setText(_translate("Form_SID_23", "No Status"))
        self.label_5.setText(_translate("Form_SID_23", "Response Type: "))
        self.pushButton_appendLog_2.setText(_translate("Form_SID_23", "Add to Log"))
        self.pushButton_Send23Req_2.setToolTip(_translate("Form_SID_23", "Sends the 22 service request to ECU"))
        self.pushButton_Send23Req_2.setText(_translate("Form_SID_23", "Send Request"))
        self.label_4.setText(_translate("Form_SID_23", "Response : "))
        self.label_6.setText(_translate("Form_SID_23", "ALFID"))
        self.label_ResType_2.setText(_translate("Form_SID_23", "No Response"))
        self.pushButton_reset_2.setText(_translate("Form_SID_23", "Reset"))
        self.pushButton_clearLog_2.setText(_translate("Form_SID_23", "Clear Log"))
        self.label_7.setText(_translate("Form_SID_23", "Memory size"))
        self.label_8.setText(_translate("Form_SID_23", "Memory address"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form_SID_23 = QtWidgets.QDialog()
    ui = Ui_Form_SID_23()
    ui.setupUi(Form_SID_23)
    Form_SID_23.show()
    sys.exit(app.exec_())