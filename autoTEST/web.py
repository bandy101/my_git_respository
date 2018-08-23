import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWebSockets import *

class Form(QWidget):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        # self.setWindowOpacity(1)
        # self.setWindowFlags(Qt.FramelessWindowHint)
        # self.setAttribute(Qt.WA_TranslucentBackground)
        # self.showFullScreen()
        rect = QApplication.desktop().screenGeometry()
        self.resize(600,600)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        self.webview = QWebEngineView()

        vbox = QVBoxLayout()
        vbox.addWidget(self.webview)

        main = QGridLayout()
        main.setSpacing(0)
        main.addLayout(vbox, 0, 0)

        self.setLayout(main)

        # self.setWindowTitle("CoDataHD")
        # webview.load(QUrl('http://www.cnblogs.com/misoag/archive/2013/01/09/2853515.html'))
        # webview.show()

    def load(self, url):
        self.webview.load(QUrl(url))
        self.webview.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    screen = Form()
    screen.show()
    url = "https://www.baidu.com"
    screen.load(url)
    sys.exit(app.exec_())