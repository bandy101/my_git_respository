from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
from main_ui import Ui_Form

import check_pt as C
app = QApplication(sys.argv)

class Gui(QWidget,Ui_Form):
    def __init__(self):
        super(Gui,self).__init__()
        self.setupUi(self)
        self.site.DrawWindowBackground
        self.qingyuan.toggled.connect(self.qy)
        self.guangzhou.toggled.connect(self.gz)
    def qy(self,value):
        if self.qingyuan.isChecked():
                self.site.clear()
                self.site.addItem('全部')
                self.site.addItems(C.qys.keys())
    def gz(self,value):
        if self.guangzhou.isChecked():
            self.site.clear()

ui = Gui()
ui.show()
sys.exit(app.exec_())
