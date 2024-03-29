# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(904, 702)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.button1 = QtWidgets.QPushButton(self.centralwidget)
        self.button1.setObjectName("button1")
        self.horizontalLayout.addWidget(self.button1)
        self.button2 = QtWidgets.QPushButton(self.centralwidget)
        self.button2.setObjectName("button2")
        self.horizontalLayout.addWidget(self.button2)
        self.button3 = QtWidgets.QPushButton(self.centralwidget)
        self.button3.setObjectName("button3")
        self.horizontalLayout.addWidget(self.button3)
        self.button4 = QtWidgets.QPushButton(self.centralwidget)
        self.button4.setObjectName("button4")
        self.horizontalLayout.addWidget(self.button4)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.codeLabel = QtWidgets.QLabel(self.centralwidget)
        self.codeLabel.setObjectName("codeLabel")
        self.verticalLayout.addWidget(self.codeLabel)
        self.codeTextEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.codeTextEdit.setObjectName("codeTextEdit")
        self.verticalLayout.addWidget(self.codeTextEdit)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.varsLabel = QtWidgets.QLabel(self.centralwidget)
        self.varsLabel.setObjectName("varsLabel")
        self.verticalLayout_2.addWidget(self.varsLabel)
        self.varsTextView = QtWidgets.QTextBrowser(self.centralwidget)
        self.varsTextView.setObjectName("varsTextView")
        self.verticalLayout_2.addWidget(self.varsTextView)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.horizontalLayout_2.setStretch(0, 2)
        self.horizontalLayout_2.setStretch(1, 1)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Pointer Explorer"))
        self.button1.setText(_translate("MainWindow", "Start"))
        self.button2.setText(_translate("MainWindow", "Next Line"))
        self.button3.setText(_translate("MainWindow", "Previous Line"))
        self.button4.setText(_translate("MainWindow", "Show Memory"))
        self.codeLabel.setText(_translate("MainWindow", "Code"))
        self.varsLabel.setText(_translate("MainWindow", "Memory"))
