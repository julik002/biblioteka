# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Список_читателей.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1360, 700)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(0, 0, 1361, 91))
        self.frame.setStyleSheet("background-color:rgb(170, 255, 127)")
        self.frame.setFrameShape(QtWidgets.QFrame.Box)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(620, 20, 131, 41))
        font = QtGui.QFont()
        font.setPointSize(22)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setGeometry(QtCore.QRect(0, 90, 271, 611))
        self.frame_2.setStyleSheet("background-color:rgb(170, 255, 127)")
        self.frame_2.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.pushButton = QtWidgets.QPushButton(self.frame_2)
        self.pushButton.setGeometry(QtCore.QRect(40, 60, 181, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("background-color:rgb(255, 255, 255)")
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_2.setGeometry(QtCore.QRect(40, 120, 181, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet("background-color:rgb(255, 255, 255)")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_3.setGeometry(QtCore.QRect(40, 178, 181, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setStyleSheet("background-color:rgb(255, 255, 255)")
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_4.setGeometry(QtCore.QRect(40, 240, 181, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setStyleSheet("background-color:rgb(255, 255, 255)")
        self.pushButton_4.setObjectName("pushButton_4")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(270, 90, 1091, 611))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Список читателей"))
        self.label.setText(_translate("MainWindow", "Читатели"))
        self.pushButton.setText(_translate("MainWindow", "Редактировать"))
        self.pushButton_2.setText(_translate("MainWindow", "Добавить"))
        self.pushButton_3.setText(_translate("MainWindow", "Удалить"))
        self.pushButton_4.setText(_translate("MainWindow", "Назад"))
