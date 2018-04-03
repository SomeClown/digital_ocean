#!venv/bin/python3

# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    """
    main window
    """
    def setupUi(self, MainWindow):
        """
        more main window
        :param MainWindow: 
        :return: 
        """
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.accountInfoPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.accountInfoPushButton.setGeometry(QtCore.QRect(20, 20, 113, 32))
        self.accountInfoPushButton.setObjectName("accountInfoPushButton")
        self.dropletsPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.dropletsPushButton.setGeometry(QtCore.QRect(20, 50, 113, 32))
        self.dropletsPushButton.setObjectName("dropletsPushButton")
        self.ImagesPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.ImagesPushButton.setGeometry(QtCore.QRect(20, 80, 113, 32))
        self.ImagesPushButton.setObjectName("ImagesPushButton")
        self.dnsPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.dnsPushButton.setGeometry(QtCore.QRect(20, 110, 113, 32))
        self.dnsPushButton.setObjectName("dnsPushButton")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(170, 20, 611, 521))
        self.textBrowser.setObjectName("textBrowser")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        """
        stuff goes here
        :param MainWindow: 
        :return: 
        """
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Digital Ocean Utility"))
        self.accountInfoPushButton.setText(_translate("MainWindow", "Account Info"))
        self.dropletsPushButton.setText(_translate("MainWindow", "Droplets"))
        self.ImagesPushButton.setText(_translate("MainWindow", "Images"))
        self.dnsPushButton.setText(_translate("MainWindow", "DNS"))

        self.accountInfoPushButton.clicked.connect(self.teren)

    def teren(self):
        self.textBrowser.setPlainText('test')

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

