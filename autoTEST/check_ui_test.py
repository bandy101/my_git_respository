from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
from main_ui import Ui_Form
from threading import Thread
# from main import Ui_Form
import check_pt as C
import json
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
        with open('config.json',encoding='utf-8') as f:
            alls = json.load(f)
            self.json = alls
        self.pre = myThread()
        self.pre.pre_search.connect(lambda :self.result_text.setText('正在查询···'))
        self.pre.start()
        ##平台{01:qingyuan,02:guangzhou}
        self.flats = '01'
        self.qingyuan.toggled.connect(self.flat)
        self.guangzhou.toggled.connect(self.flat)
        #平台设备
        self.get_site_info()
        #空质量和遥测方法ID
        self.air_mthod_id = None
        self.telemetru_mthod_id = None

        #测量选项
        self.airs =[self.air_quality,self.air_quality_data,self.air_quality_day,self.air_quality_mon,self.air_quality_year]
        self.telemetrys =[self.telemetry_data,self.telemetry_day,self.telemetry_mon]
        self.all_radio =self.airs+self.telemetrys
        for _ in self.all_radio:
            _.toggled.connect(self.radiobutton)
    
        #单点查询
        self.search.clicked.connect(self.search_one)
        ##初始化平台
        self.flat(None)
        self.qingyuan.toggled.emit(True)

    def get_site_info(self):
            for _ in self.json['platform']:
                if _['id']==self.flats:
                    self.air_tsno =_['airTSNO']
                    self.telemetry_tsno = _['telemetryTSNO']
                    self.sitename=_['site']
                    self.air_mthod_id = _['air']
                    self.telemetru_mthod_id = _['telemetry']
                return
    def search_one(self):
        try:
            self.fun = self.map_fun()
            self.result_text.setText('<font size="8" color="red"><b>正在查询</b></font>')   
        except:
            space = ['&nbsp;' for _ in range(7)]
            self.result_text.setText(''.join(space)+'<font size="8" color="red"><b>请选择查询的数据</b></font>')
            return
        space = ['&nbsp;' for _ in range(12)]
        for _ in self.fun:
            key,f,mthod_id = list(_)
            #key 查看需要测试的是哪个数据
            test_site = self.site.currentIndex()
            if key:
                print('开始···')
                if 'air' in f.__name__:
                    if test_site in [0,-1]:self.tsno = self.air_tsno.values()
                    else:self.tsno = self.air_tsno[self.site.currentText()]
                if 'telemetry' in f.__name__:
                    if test_site in [0,-1]:self.tsno = list(self.telemetry_tsno.values())
                    else:self.tsno = self.telemetry_tsno[self.site.currentText()]
                # print('tsno-----ui,',self.tsno)
                url,param = None,None
                for _ in self.json['request']:
                    if _['id']==mthod_id:
                        url = _['url']
                        param =_['param']
                        break

                strs = f(url,param,self.tsno)
                # strs = f()
                self.result_text.setText(''.join(space)+'<font size="8" color="red"><b>查询完毕</b></font><br>\n'
                    +strs+'<br>')
                break

    def flat(self,value):
        if self.qingyuan.isChecked():
            self.flats ='01'
            self.site.clear()
            self.site.addItem('全部')
            self.get_site_info()
            self.site.addItems(self.sitename)
            # print(self.site.currentIndex())
            self.search_data()
        if self.guangzhou.isChecked():
            self.flats='02'
            self.site.clear()
            self.search_data()
    def radiobutton(self,value):
        self.air_day =False
        self.air_mon = False
        self.air_year = False
        self.air_data = False   
        self.air_quality_s =False #空气质量
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
            self.telem_day =True
        if self.telemetry_mon.isChecked():
            self.telem_mon =True
        if self.air_quality.isChecked():
            self.air_quality_s =True
    def map_fun(self):
        key = [self.air_quality_s,self.air_data,self.air_day,self.air_mon,self.air_year,
        self.telem_data,self.telem_day,self.telem_mon]
        values =[C.air_quality,C.air_quality_data_manger,C.air_quality_statistics_day,C.air_quality_statistics_month,C.air_quality_statistics_year,
        C.telemetry_data_manerger,C.telemetry_data_day,C.telemetry_data_month]
        alls_metho_id = self.air_mthod_id+self.telemetru_mthod_id
        print(alls_metho_id)
        return zip(key,values,alls_metho_id)

    def search_data(self):
        for _ in self.json['platform']:
            if _['id']==self.flats:
                have_air = _['air']
                have_telemetr = _['telemetry']
                # print(have_air)
        if have_air:
            for _ in self.airs:
                _.setEnabled(True)
        else:
            for _ in self.airs:
                # print(_)
                _.setEnabled(False)
        if have_telemetr:
            for _ in self.telemetrys:
                _.setEnabled(True)
        else:
            for _ in self.telemetrys:
                _.setEnabled(False)
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
