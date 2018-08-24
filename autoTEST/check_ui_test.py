from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
from main_ui import Ui_Form
from threading import Thread
# from main import Ui_Form
import check_pt as C

app = QApplication(sys.argv)

class myThread(QThread):
    pre_search =pyqtSignal()
    def __init__(self,parent=None):  
        super(myThread,self).__init__(parent)  
    
    def run(self):
        # self.pre_search.emit()
        pass

class Gui(QWidget,Ui_Form):
    def __init__(self):

        super(Gui,self).__init__()
        self.setupUi(self)
        self.pre = myThread()
        self.pre.pre_search.connect(lambda :self.result_text.setText('正在查询···'))
        self.pre.start()
        ##平台{1:qingyuan,2:guangzhou}
        self.flats = 1

        #需要查询的
        # self.air_day =False
        # self.air_mon=False
        # self.air_year = False
        # self.air_data = False
        # self.telem_day = False
        # self.telem_mon = False
        # self.telem_data = False


        self.qingyuan.toggled.connect(self.flat)
        self.guangzhou.toggled.connect(self.flat)

        #测量选项
        self.all_radio =[self.air_quality_data,self.air_quality_day,self.air_quality_mon,
        self.air_quality_year,self.telemetry_data,self.telemetry_day,self.telemetry_mon]
        for _ in self.all_radio:
            _.toggled.connect(self.radiobutton)
    
        #单点查询
        self.search.clicked.connect(self.search_one)

    def search_one(self):
        self
        try:
            self.fun = self.map_fun()
            self.result_text.setText('<font size="8" color="red"><b>正在查询</b></font>')
            
        except:
            space = ['&nbsp;' for _ in range(7)]
            self.result_text.setText(''.join(space)+'<font size="8" color="red"><b>请选择查询的数据</b></font>')
            return
        # T = Thread(target=lambda :self.result_text.setText('正在查询···'))
        # T.setDaemon(True)#设置线程为后台线程
        # T.start()
        # self.pre.pre_search.emit()
        self.result_text.setText('正在查询···')
        self.result_text.textChanged.emit()
        # self.result_text.insertHtml('<font size="8" color="red"><b>查询的数据</b></font>')
        # self.result_text.insertPlainText('123456')
        space = ['&nbsp;' for _ in range(12)]
        for _ in self.fun:
            key,f = list(_)
            # print(key,f)
            if key:
                print('开始···')
                strs = f()
                self.result_text.setText(''.join(space)+'<font size="8" color="red"><b>查询完毕</b></font><br>\n'
                    +strs+'<br>')
                break

    def flat(self,value):
        if self.qingyuan.isChecked():
                self.site.clear()
                self.site.addItem('全部')
                self.site.addItems(C.qys.keys())
        if self.guangzhou.isChecked():
            self.site.clear()
    def radiobutton(self,value):
        self.air_day =False
        self.air_mon = False
        self.air_year = False
        self.air_data = False   
        self.telem_day = False
        self.telem_mon = False
        self.telem_data = False
        if self.air_quality_data.isChecked():
            self.air_data =True
        if self.air_quality_day.isChecked():
            self.air_day =True
        if self.air_quality_mon.isChecked():
            self.air_mon = True
        if self.air_quality_year.isChecked():
            self.air_year = True
        if self.telemetry_data.isChecked():
            self.telem_data =True
        if self.telemetry_day.isChecked():
            self.telem_data =True
        if self.telemetry_mon.isChecked():
            self.telem_mon =True

    def map_fun(self):
        key = [self.air_day,self.air_mon,self.air_year,self.air_data,
        self.telem_day,self.telem_mon,self.telem_data]
        print(key)
        values =[C.air_quality_statistics_day,C.air_quality_statistics_month,C.air_quality_statistics_year,C.air_quality_data_manger,
        C.telemetry_data_day,C.telemetry_data_month,C.telemetry_data_manerger]
        return zip(key,values)


class opI:
    '''
        界面操作接口
    '''
    def __init__(self):
        self.ui = Gui()
        self.ui.show()
        # Thread(target=lambda:self.ui.show()).start()

    def search_waittime(self):
        self.ui.result_text.setText('正在查询···')
if __name__=='__main__':
    # ui = Gui()
    # ui.pre.pre_search.emit()
    opI()
    sys.exit(app.exec_())
