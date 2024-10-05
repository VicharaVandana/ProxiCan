# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dsc_widget.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form_SID10(object):
    def setupUi(self, Form_SID10):
        Form_SID10.setObjectName("Form_SID10")
        Form_SID10.resize(639, 425)
        Form_SID10.setMinimumSize(QtCore.QSize(400, 400))
        self.label_status = QtWidgets.QLabel(Form_SID10)
        self.label_status.setGeometry(QtCore.QRect(10, 340, 621, 71))
        self.label_status.setStyleSheet("background-color: rgb(255, 255, 127);\n"
"color: rgb(85, 0, 0);\n"
"border-color: rgb(0, 0, 255);")
        self.label_status.setAlignment(QtCore.Qt.AlignCenter)
        self.label_status.setWordWrap(True)
        self.label_status.setObjectName("label_status")
        self.layoutWidget = QtWidgets.QWidget(Form_SID10)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 20, 621, 302))
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
        self.textBrowser_Resp = QtWidgets.QTextBrowser(self.layoutWidget)
        self.textBrowser_Resp.setObjectName("textBrowser_Resp")
        self.gridLayout.addWidget(self.textBrowser_Resp, 6, 1, 1, 2)
        self.pushButton_clearLog = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_clearLog.setStyleSheet("background-color: rgb(85, 255, 127);\n"
"color: rgb(85, 0, 0);")
        self.pushButton_clearLog.setObjectName("pushButton_clearLog")
        self.gridLayout.addWidget(self.pushButton_clearLog, 3, 2, 1, 1)
        self.comboBox_Diagsession = QtWidgets.QComboBox(self.layoutWidget)
        self.comboBox_Diagsession.setMinimumSize(QtCore.QSize(220, 0))
        self.comboBox_Diagsession.setMaximumSize(QtCore.QSize(220, 16777215))
        self.comboBox_Diagsession.setObjectName("comboBox_Diagsession")
        self.comboBox_Diagsession.addItem("")
        self.comboBox_Diagsession.addItem("")
        self.comboBox_Diagsession.addItem("")
        self.comboBox_Diagsession.addItem("")
        self.gridLayout.addWidget(self.comboBox_Diagsession, 0, 1, 1, 1, QtCore.Qt.AlignHCenter)
        self.label_ResType = QtWidgets.QLabel(self.layoutWidget)
        self.label_ResType.setAutoFillBackground(False)
        self.label_ResType.setStyleSheet("color: rgb(0, 0, 255);")
        self.label_ResType.setAlignment(QtCore.Qt.AlignCenter)
        self.label_ResType.setObjectName("label_ResType")
        self.gridLayout.addWidget(self.label_ResType, 3, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        self.label_2.setMinimumSize(QtCore.QSize(130, 0))
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.layoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 6, 0, 1, 1)
        self.pushButton_reset = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_reset.setStyleSheet("background-color: rgb(170, 170, 0);\n"
"font: 75 8pt \"MS Shell Dlg 2\";\n"
"color: rgb(0, 85, 0);")
        self.pushButton_reset.setObjectName("pushButton_reset")
        self.gridLayout.addWidget(self.pushButton_reset, 6, 3, 1, 1)
        self.label = QtWidgets.QLabel(self.layoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.pushButton_Send10Req = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_Send10Req.setStyleSheet("background-color: rgb(0, 255, 255);\n"
"border-color: rgb(0, 0, 0);\n"
"color: rgb(0, 0, 0);")
        self.pushButton_Send10Req.setObjectName("pushButton_Send10Req")
        self.gridLayout.addWidget(self.pushButton_Send10Req, 0, 3, 1, 1)
        self.checkBox_suppressposmsg = QtWidgets.QCheckBox(self.layoutWidget)
        self.checkBox_suppressposmsg.setObjectName("checkBox_suppressposmsg")
        self.gridLayout.addWidget(self.checkBox_suppressposmsg, 0, 2, 1, 1, QtCore.Qt.AlignRight)
        self.pushButton_appendLog.raise_()
        self.label_ResType.raise_()
        self.textBrowser_Resp.raise_()
        self.pushButton_clearLog.raise_()
        self.label.raise_()
        self.pushButton_reset.raise_()
        self.label_3.raise_()
        self.pushButton_Send10Req.raise_()
        self.comboBox_Diagsession.raise_()
        self.label_2.raise_()
        self.checkBox_suppressposmsg.raise_()

        self.retranslateUi(Form_SID10)
        QtCore.QMetaObject.connectSlotsByName(Form_SID10)

    def retranslateUi(self, Form_SID10):
        _translate = QtCore.QCoreApplication.translate
        Form_SID10.setWindowTitle(_translate("Form_SID10", "Disgnostic Session Control Service 10"))
        self.label_status.setText(_translate("Form_SID10", "No Status"))
        self.pushButton_appendLog.setText(_translate("Form_SID10", "Add to Log"))
        self.pushButton_clearLog.setText(_translate("Form_SID10", "Clear Log"))
        self.comboBox_Diagsession.setToolTip(_translate("Form_SID10", "Select the Diag session to which you want ECU to move. If your session is not in list then contact admin"))
        self.comboBox_Diagsession.setItemText(0, _translate("Form_SID10", "01 - Default"))
        self.comboBox_Diagsession.setItemText(1, _translate("Form_SID10", "02 - Programming"))
        self.comboBox_Diagsession.setItemText(2, _translate("Form_SID10", "03 - Extended"))
        self.comboBox_Diagsession.setItemText(3, _translate("Form_SID10", "04 - Safety"))
        self.label_ResType.setText(_translate("Form_SID10", "No Response"))
        self.label_2.setText(_translate("Form_SID10", "Response Type"))
        self.label_3.setText(_translate("Form_SID10", "Response"))
        self.pushButton_reset.setText(_translate("Form_SID10", "Reset"))
        self.label.setText(_translate("Form_SID10", "Diag Session"))
        self.pushButton_Send10Req.setToolTip(_translate("Form_SID10", "Sends the 10 service request to ECU"))
        self.pushButton_Send10Req.setText(_translate("Form_SID10", "Send Request"))
        self.checkBox_suppressposmsg.setToolTip(_translate("Form_SID10", "If selected then Suppress Positive Response Message Indication bit will be set in Subfunction"))
        self.checkBox_suppressposmsg.setText(_translate("Form_SID10", "SPRMIB"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form_SID10 = QtWidgets.QWidget()
    ui = Ui_Form_SID10()
    ui.setupUi(Form_SID10)
    Form_SID10.show()
    sys.exit(app.exec_())