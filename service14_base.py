# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\ass930085\OneDrive - Tata Technologies\Documents\PROXI GIT\reference\ProxiCan\SID_14.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form_SID14(object):
    def setupUi(self, Form_SID14):
        Form_SID14.setObjectName("Form_SID14")
        Form_SID14.resize(743, 458)
        self.layoutWidget = QtWidgets.QWidget(Form_SID14)
        self.layoutWidget.setGeometry(QtCore.QRect(22, 21, 701, 331))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton_appendLog = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_appendLog.setStyleSheet("background-color: rgb(85, 255, 127);\n"
"color: rgb(85, 0, 0);")
        self.pushButton_appendLog.setObjectName("pushButton_appendLog")
        self.gridLayout.addWidget(self.pushButton_appendLog, 3, 3, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.layoutWidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)
        self.textBrowser_Resp = QtWidgets.QTextBrowser(self.layoutWidget)
        self.textBrowser_Resp.setObjectName("textBrowser_Resp")
        self.gridLayout.addWidget(self.textBrowser_Resp, 6, 1, 1, 2)
        self.pushButton_reset = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_reset.setStyleSheet("background-color: rgb(170, 170, 0);\n"
"font: 75 8pt \"MS Shell Dlg 2\";\n"
"color: rgb(0, 85, 0);")
        self.pushButton_reset.setObjectName("pushButton_reset")
        self.gridLayout.addWidget(self.pushButton_reset, 6, 3, 1, 1)
        self.label_ResType = QtWidgets.QLabel(self.layoutWidget)
        self.label_ResType.setAutoFillBackground(False)
        self.label_ResType.setStyleSheet("color: rgb(0, 0, 255);")
        self.label_ResType.setAlignment(QtCore.Qt.AlignCenter)
        self.label_ResType.setObjectName("label_ResType")
        self.gridLayout.addWidget(self.label_ResType, 3, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.layoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 6, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        self.label_2.setMinimumSize(QtCore.QSize(130, 0))
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 1)
        self.pushButton_clearLog = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_clearLog.setStyleSheet("background-color: rgb(85, 255, 127);\n"
"color: rgb(85, 0, 0);")
        self.pushButton_clearLog.setObjectName("pushButton_clearLog")
        self.gridLayout.addWidget(self.pushButton_clearLog, 3, 2, 1, 1)
        self.lineEdit_dtc = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_dtc.setText("")
        self.lineEdit_dtc.setObjectName("lineEdit_dtc")
        self.gridLayout.addWidget(self.lineEdit_dtc, 2, 1, 1, 1)
        self.pushButton_Send14Req = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_Send14Req.setStyleSheet("background-color: rgb(0, 255, 255);\n"
"border-color: rgb(0, 0, 0);\n"
"color: rgb(0, 0, 0);")
        self.pushButton_Send14Req.setObjectName("pushButton_Send14Req")
        self.gridLayout.addWidget(self.pushButton_Send14Req, 2, 2, 1, 2)
        self.textBrowser_Resp.raise_()
        self.pushButton_reset.raise_()
        self.label_3.raise_()
        self.label_ResType.raise_()
        self.label_2.raise_()
        self.lineEdit_dtc.raise_()
        self.label_4.raise_()
        self.pushButton_clearLog.raise_()
        self.pushButton_appendLog.raise_()
        self.pushButton_Send14Req.raise_()
        self.label_status = QtWidgets.QLabel(Form_SID14)
        self.label_status.setGeometry(QtCore.QRect(30, 370, 691, 71))
        self.label_status.setStyleSheet("background-color: rgb(255, 255, 127);\n"
"color: rgb(85, 0, 0);\n"
"border-color: rgb(0, 0, 255);")
        self.label_status.setAlignment(QtCore.Qt.AlignCenter)
        self.label_status.setWordWrap(True)
        self.label_status.setObjectName("label_status")

        self.retranslateUi(Form_SID14)
        QtCore.QMetaObject.connectSlotsByName(Form_SID14)

    def retranslateUi(self, Form_SID14):
        _translate = QtCore.QCoreApplication.translate
        Form_SID14.setWindowTitle(_translate("Form_SID14", "Clear Diagnostic Information Service 14"))
        self.pushButton_appendLog.setText(_translate("Form_SID14", "Add to Log"))
        self.label_4.setText(_translate("Form_SID14", "DTC Bytes"))
        self.pushButton_reset.setText(_translate("Form_SID14", "Reset"))
        self.label_ResType.setText(_translate("Form_SID14", "No Response"))
        self.label_3.setText(_translate("Form_SID14", "Response"))
        self.label_2.setText(_translate("Form_SID14", "Response Type"))
        self.pushButton_clearLog.setText(_translate("Form_SID14", "Clear Log"))
        self.lineEdit_dtc.setToolTip(_translate("Form_SID14", "Enter DTC bytes in hexadecimal format"))
        self.pushButton_Send14Req.setToolTip(_translate("Form_SID14", "Sends the 14 service request to ECU"))
        self.pushButton_Send14Req.setText(_translate("Form_SID14", "Send Request"))
        self.label_status.setText(_translate("Form_SID14", "No Status"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form_SID14 = QtWidgets.QWidget()
    ui = Ui_Form_SID14()
    ui.setupUi(Form_SID14)
    Form_SID14.show()
    sys.exit(app.exec_())