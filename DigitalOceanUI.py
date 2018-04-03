#!venv/bin/python3

# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import requests
import json

__author__ = "SomeClown"
__license__ = "MIT"
__maintainer__ = "Teren Bryson"
__email__ = "teren@packetqueue.net"

"""
Copyright 2018 by Teren Bryson

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""


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

    color_black2 = "\033[1;30m"
    color_red2_on = "\033[01;31m"
    color_red2_off = "\33[00m"
    color_green2 = "\033[1;32m"
    color_yellow2 = "\033[1;33m"
    color_blue2 = "\033[1;34m"
    color_purple2 = "\033[1;35m"
    color_cyan2 = "\033[1;36m"
    color_white2 = "\033[1;37m"
    color_off = "\33[00m"

    with open('uid.txt', 'r') as f:
        api_token = (f.readline().rstrip())
    api_url_base = 'https://api.digitalocean.com/v2/'
    headers = {'Content-Type': 'application/json',
               'User-Agent': 'Umbrella Corporation',
               'Authorization': 'Bearer {0}'.format(api_token)}

    def teren(self):
        self.return_account_info()

    def get_stuff(self, suffix: str):
        """
        return a python response object to calling object
        :param: suffix
        :return: json object
        """
        api_url = (self.api_url_base + suffix)
        response = requests.get(api_url, headers=self.headers)
        if response.status_code == 200:
            return json.loads(response.content.decode('utf-8'))
        elif response.status_code >= 500:
            self.textBrowser.setPlainText('[!] [{0}] Server Error'.format(response.status_code))
            return None
        elif response.status_code == 404:
            self.textBrowser.setPlainText('[!] [{0}] URL not found: [{1}]'.format(response.status_code, api_url))
            return None
        elif response.status_code == 401:
            self.textBrowser.setPlainText('[!] [{0}] Authentication Failed'.format(response.status_code))
            return None
        elif response.status_code == 400:
            self.textBrowser.setPlainText('[!] [{0}] Bad Request'.format(response.status_code))
            return None
        elif response.status_code >= 300:
            self.textBrowser.setPlainText('[!] [{0}] Unexpected Redirect'.format(response.status_code))
            return None
        else:
            self.textBrowser.setPlainText('[?] Unexpected Error: [HTTP {0}]: '
                                  'Content: {1}'.format(response.status_code, response.content))
            return None

    def return_account_info(self):
        """
        Returns account information
        """
        get_account = self.get_stuff(suffix='account')
        if not isinstance(get_account, dict):
            raise TypeError('returned object type is incorrect')
        self.textBrowser.setPlainText(' ')
        for k, v in get_account['account'].items():
            self.textBrowser.append(str(k) + ': ' + str(v))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

