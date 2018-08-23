from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
from main_ui import Ui_Form
# from main import Ui_Form
import check_pt as C
app = QApplication(sys.argv)

class Gui(QWidget,Ui_Form):
    def __init__(self):
        super(Gui,self).__init__()
        self.setupUi(self)

        ##平台{1:qingyuan,2:guangzhou}
        self.flats = 1
        ##需要查询的
        self.air_day =False
        self.air_month=False
        self.air_year = False

        self.telem_day = False
        self.telem_mon = False

        self.site.DrawWindowBackground
        self.qingyuan.toggled.connect(self.flat)
        self.guangzhou.toggled.connect(self.flat)

    def flat(self,value):
        if self.qingyuan.isChecked():
                self.site.clear()
                self.site.addItem('全部')
                self.site.addItems(C.qys.keys())
        if self.guangzhou.isChecked():
            self.site.clear()
    def radiobutton(self):
        pass
ui = Gui()
ui.show()
sys.exit(app.exec_())
