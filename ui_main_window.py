# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_main_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(840, 668)
        Form.setStyleSheet("background-color:rgb(123,86,191);\n"
"color:rgb(220,220,220);")
        self.frame_top = QtWidgets.QFrame(Form)
        self.frame_top.setGeometry(QtCore.QRect(0, 0, 2011, 51))
        self.frame_top.setStyleSheet("background-color: rgb(35, 35, 35);")
        self.frame_top.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_top.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_top.setObjectName("frame_top")
        self.pushButton = QtWidgets.QPushButton(self.frame_top)
        self.pushButton.setGeometry(QtCore.QRect(0, 0, 101, 51))
        self.pushButton.setStyleSheet("background-color:rgba(255, 255, 255, 255);\n"
"color:rgba(35, 35, 35);")
        self.pushButton.setObjectName("pushButton")
        self.label_3 = QtWidgets.QLabel(self.frame_top)
        self.label_3.setGeometry(QtCore.QRect(320, 0, 221, 41))
        font = QtGui.QFont()
        font.setPointSize(22)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color:rgba(255, 255, 255, 255);")
        self.label_3.setObjectName("label_3")
        self.control_bt = QtWidgets.QPushButton(self.frame_top)
        self.control_bt.setGeometry(QtCore.QRect(100, 0, 101, 51))
        self.control_bt.setStyleSheet("background-color:rgba(255, 255, 255, 255);\n"
"color:rgba(35, 35, 35);")
        self.control_bt.setObjectName("control_bt")
        self.image_label = QtWidgets.QLabel(Form)
        self.image_label.setGeometry(QtCore.QRect(110, 80, 631, 531))
        self.image_label.setObjectName("image_label")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "AI-an toàn lúc lái xe"))
        self.pushButton.setText(_translate("Form", "TÀI KHOẢN"))
        self.label_3.setText(_translate("Form", "Skynet xin chào"))
        self.control_bt.setText(_translate("Form", "CAMERA AI"))
        self.image_label.setText(_translate("Form", "Màn hình"))
