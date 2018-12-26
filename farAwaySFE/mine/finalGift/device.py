from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from  ui.mainUI import Ui_Main

import sys,os

class DeviceGui(QWidget,Ui_Main):
    """ 最后的酱油界面 """
   

    def __init__(self):
        super(DeviceGui,self).__init__()
        self.setupUi(self)
        
        # 站点
        site = ['清远','新乡']
        self._addtab(site)


    # 添加站点
    def _addtab(self,name):
        for _ in name:
            self._ = QWidget()
            self._.setObjectName(_)
            self.tabWidget.addTab(self._, _)


def main():
    app = QApplication(sys.argv) # ui主程序
    ui = DeviceGui()
    ui.show()
    sys.exit(app.exec_())
    

if __name__ == '__main__':
    main()