#!venv/bin/python3

# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import requests
import json

__author__ = "SomeClown"
__license__ = "MIT"
__maintainer__ = "Teren Bryson"
__email__ = "account_info@packetqueue.net"

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

    css = '''
    .red_normal{
        color: red;
    }
    .red_italic{
        color: red; 
        font-style: italic;
    }
    .red_left_pad{
        color: red;
        padding-left:5em;
    }
    .black_normal{
        color: black;
    }
    .black_italic{
        color: black;
        font-style: italic;
    }
    .blue_normal{
        color: blue;
    }
    .blue_left_pad{
        color: blue;
        padding-left:5em;
    }
    .blue_italic{
        color: blue; 
        font-style: italic;
    }
    '''

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

        self.accountInfoPushButton.clicked.connect(self.account_info)
        self.dnsPushButton.clicked.connect(self.dns_info)
        self.dropletsPushButton.clicked.connect(self.droplets_info)

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

    def account_info(self):
        """
        
        :return: 
        """
        self.return_account_info(self)

    def dns_info(self):
        """
        
        :return: 
        """
        self.return_dns_records(self)

    def droplets_info(self):
        """
        
        :return: 
        """
        self.return_droplets_info(self, droplet_id=0)

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

    @staticmethod
    def return_account_info(self):
        """
        Returns account information
        """
        get_account = self.get_stuff(suffix='account')
        if not isinstance(get_account, dict):
            raise TypeError('returned object type is incorrect')
        self.textBrowser.setPlainText(' ')
        cursor = self.textBrowser.textCursor()
        doc = self.textBrowser.document()
        doc.setDefaultStyleSheet(self.css)
        for k, v in get_account['account'].items():
            cursor.insertHtml('''<p><span class='red_normal'>{}</span>'''.format(k))
            cursor.insertHtml(''': ''')
            cursor.insertHtml('''<span class='blue'>{}</span></p>'''.format(v))
            cursor.insertHtml("<br>")

    @staticmethod
    def return_droplets_info(self, droplet_id: int):
        """
        
        :param self: 
        :param droplet_id: 
        :return: 
        """
        cursor = self.textBrowser.textCursor()
        doc = self.textBrowser.document()
        doc.setDefaultStyleSheet(self.css)
        if droplet_id:
            cursor.insertHtml('''<p><span class='red_normal'>{}</span>'''.format('Not yet implemented'))
            return
        else:
            get_droplets = self.get_stuff(suffix='droplets')
            if not isinstance(get_droplets, dict):
                raise TypeError('returned object is incorrect')

        def print_dict(d: dict):
            """

            :param d: 
            :return: 
            """
            for k, v in d.items():
                if isinstance(v, dict):
                    print_dict(v)
                elif isinstance(v, list):
                    for item in v:
                        cursor.insertHtml(
                            '''<p><span class='red_normal'>{}</span></p>'''.format('Name: '))
                        cursor.insertHtml(
                            '''<p><span class='black_normal'>{}</span><br /></p>'''.format(item['name']))

                        cursor.insertHtml(
                            '''<p><span class='red_normal'>{}</span></p>'''.format('ID: '))
                        cursor.insertHtml(
                            '''<p><span class='black_normal'>{}</span><br /></p>'''.format(str(item['id'])))

                        cursor.insertHtml(
                            '''<p><span class='red_normal'>{}</span></p>'''.format('Memory: '))
                        cursor.insertHtml(
                            '''<p><span class='black_normal'>{}</span><br /></p>'''.format(str(item['size']['slug'])))

                        cursor.insertHtml(
                            '''<p><span class='red_normal'>{}</span></p>'''.format('vCPUs: '))
                        cursor.insertHtml(
                            '''<p><span class='black_normal'>{}</span><br /></p>'''.format(str(item['vcpus'])))

                        cursor.insertHtml(
                            '''<p><span class='red_normal'>{}</span></p>'''.format('Disk: '))
                        cursor.insertHtml(
                            '''<p><span class='black_normal'>{}</span><br /></p>'''.format(str(item['disk'])))

                        cursor.insertHtml(
                            '''<p><span class='red_normal'>{}</span></p>'''.format('Status: '))
                        cursor.insertHtml(
                            '''<p><span class='black_normal'>{}</span><br /></p>'''.format(str(item['status'])))

                        cursor.insertHtml(
                            '''<p><span class='red_normal'>{}</span></p>'''.format('Created: '))
                        cursor.insertHtml(
                            '''<p><span class='black_normal'>{}</span><br /></p>'''.format(str(item['created_at'])))

                        cursor.insertHtml(
                            '''<p><span class='red_normal'>{}</span><br /></p>'''.format('Image Information: '))

                        cursor.insertHtml(
                            '''<p><span class='blue_left_pad'>{}</span></p>'''.format('ID: '))
                        cursor.insertHtml(
                            '''<p><span class='black_normal'>{}</span><br /</p>'''.format(str(item['image']['id'])))

                        cursor.insertHtml(
                            '''<p><span class='blue_normal'>{}</span></p>'''.format('Name: '))
                        cursor.insertHtml(
                            '''<p><span class='black_normal'>{}</span><br /></p>'''.format(str(item['image']['name'])))

                        cursor.insertHtml(
                            '''<p><span class='blue_normal'>{}</span></p>'''.format('Distribution: '))
                        cursor.insertHtml(
                            '''<p><span class='black_normal'>{}</span><br /></p>'''.format(str(item['image']['distribution'])))

                        cursor.insertHtml(
                            '''<p><span class='red_normal'>{}</span></p>'''.format('Monthly Price: '))
                        cursor.insertHtml(
                            '''<p><span class='black_normal'>{}</span><br /></p>'''.format('$' + str(item['size']['price_monthly'])))

                        cursor.insertHtml(
                            '''<p><span class='red_normal'>{}</span><br /></p>'''.format('Networking Information: '))

                        for thing, other_thing in item['networks'].items():
                            for address_stuff in other_thing:
                                cursor.insertHtml(
                                    '''<p><span class='blue_normal'>{}</span></p>'''.format('ip address: '))
                                cursor.insertHtml(
                                    '''<p><span class='black_normal'>{}</span><br /></p>'''.format(address_stuff['ip_address']))

                                cursor.insertHtml(
                                    '''<p><span class='blue_normal'>{}</span></p>'''.format('ip net mask: '))
                                cursor.insertHtml(
                                    '''<p><span class='black_normal'>{}</span><br /></p>'''.format(address_stuff['netmask']))

                                cursor.insertHtml(
                                    '''<p><span class='blue_normal'>{}</span></p>'''.format('ip gateway: '))
                                cursor.insertHtml(
                                    '''<p><span class='black_normal'>{}</span><br /></p>'''.format(address_stuff['gateway']))

                                cursor.insertHtml(
                                    '''<p><span class='blue_normal'>{}</span></p>'''.format('ip type: '))
                                cursor.insertHtml(
                                    '''<p><span class='black_normal'>{}</span><br /></p>'''.format(address_stuff['type']))

                                cursor.insertHtml(
                                    '''<p><span class='black_normal'>{}</span><br /></p>'''.format('-----------------------'))

                            cursor.insertHtml(
                                '''<p><span class='red_normal'>{}</span></p>'''.format('Region Name: '))
                            cursor.insertHtml(
                                '''<p><span class='black_normal'>{}</span></p>'''.format(item['region']['name']))
                            cursor.insertHtml(
                                '''<p><span class='black_normal'> {}</span></p>'''.format('('))
                            cursor.insertHtml(
                                '''<p><span class='red_normal'>{}</span></p>'''.format(item['region']['slug']))
                            cursor.insertHtml(
                                '''<p><span class='black_normal'>{}</span><br /></p>'''.format(')'))

                        cursor.insertHtml(
                            '''<p><span class='red_normal'>{}</span></p>'''.format('Tags: '))
                        cursor.insertHtml(
                            '''<p><span class='black_normal'>{}</span><br /></p>'''.format(str(item['tags'])))
                else:
                    pass

        print_dict(get_droplets)

    @staticmethod
    def return_dns_records(self):
        """
        
        :return: 
        """
        get_dns = self.get_stuff(suffix='domains')
        if not isinstance(get_dns, dict):
            raise TypeError('returned object type is incorrect')
        try:
            self.textBrowser.setPlainText(' ')
            self.textBrowser.append(str(get_dns))
        except BaseException as e:
            self.textBrowser.append(str(e))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

