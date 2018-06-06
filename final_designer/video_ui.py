# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'video.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1093, 597)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.bt1 = QtWidgets.QPushButton(self.centralwidget)
        self.bt1.setGeometry(QtCore.QRect(30, 10, 61, 31))
        self.bt1.setObjectName("bt1")
        self.bt2 = QtWidgets.QPushButton(self.centralwidget)
        self.bt2.setGeometry(QtCore.QRect(190, 10, 61, 31))
        self.bt2.setObjectName("bt2")
        self.formLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 60, 781, 441))  
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.formLayoutWidget)
        self.label.setText("")
        self.label.setObjectName("label")
        # self.label.setScaledContents(True)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.SpanningRole, self.label)
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setGeometry(QtCore.QRect(820, 60, 251, 381))
        self.tableView.setObjectName("tableView")
        self.bt_recognize = QtWidgets.QPushButton(self.centralwidget)
        self.bt_recognize.setGeometry(QtCore.QRect(920, 20, 61, 31))
        self.bt_recognize.setObjectName("bt_recognize")
        self.one_recognize = QtWidgets.QPushButton(self.centralwidget)
        self.one_recognize.setGeometry(QtCore.QRect(670, 10, 61, 41))
        self.one_recognize.setObjectName("one_recognize")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1093, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.bt1, self.bt2)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.bt1.setText(_translate("MainWindow", "打开视频"))
        self.bt2.setText(_translate("MainWindow", "暂停"))
        self.bt_recognize.setText(_translate("MainWindow", "车牌识别"))
        self.one_recognize.setText(_translate("MainWindow", "Recognize"))

