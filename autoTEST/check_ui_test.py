from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
from main_ui import Ui_Form
from threading import Thread
# from main import Ui_Form
import check_pt as C
import check_device as D
import json
import time
app = QApplication(sys.argv)

class myThread(QThread):
    pre_search =pyqtSignal()
    def __init__(self,ui,parent=None):  
        super(myThread,self).__init__(parent)  
        self.ui =ui
        self.pre_search.connect(self.ui.search_one)
    def run(self):
        # self.ui.search_one()
        self.ui.search.setEnabled(False)
        # self.ui.search_one()
        self.pre_search.emit()

class Gui(QWidget,Ui_Form):
    def __init__(self):
        super(Gui,self).__init__()
        self.setupUi(self)
        with open('config.json',encoding='utf-8') as f:
            alls = json.load(f)
            self.json = alls
        ##平台{01:qingyuan,02:guangzhou}
        self.flats = '01'
        self.qingyuan.toggled.connect(self.flat)
        self.guangzhou.toggled.connect(self.flat)
        #平台设备
        self.get_site_info()
        #空质量和遥测方法ID
        self.air_mthod_id = None
        self.telemetru_mthod_id = None
        self.click =False #是否查询
        #测量选项 (radiobutton 控件objectname)
        self.airs =[self.air_quality,self.air_quality_data,self.air_quality_day,self.air_quality_mon,self.air_quality_year]
        self.telemetrys =[self.telemetry_data,self.telemetry_day,self.telemetry_mon]
        self.cars = [self.car_flow_hour,self.car_flow_day,self.car_flow_mon,self.car_flow_year]
        self.all_radio =self.airs+self.telemetrys+self.cars
        for _ in self.all_radio:
            _.toggled.connect(self.radiobutton)

        #单点查询
        self.light_intensity.clicked.connect(self.lights)
        self.search.clicked.connect(self.clicks)

        ##线程查询
        # self.timer=QTimer()
        # self.timer.timeout.connect(self.seach_t)
        # self.timer.start(200)
        # self.search.clicked.connect(self.search_one)
        self.search_t =myThread(self)
        # self.search_t.pre_search.connect(self.search_one) ##绑定需要执行的函数
        ##初始化平台
        self.flat(None)
        self.qingyuan.toggled.emit(True)
    def clicks(self):
        self.click= True
        self.search.setEnabled(False)
        self.search_t.start()
        # self.search_one()
    def lights(self):
        space = ['&nbsp;' for _ in range(12)]
        self.result_text.setText(''.join(space)+'<font size="8" color="red"><b>查询完毕</b></font>')
        strs = D.check_(10)
        self.result_text.append('<br>'+strs)
        
    def seach_t(self):
        pass
        # QThread(self.search_one).start()
        # Thread(target=self.search_one).start()
        # if self.click:
        #     self.search.setDisabled(True)
        #     self.click =False
        #     self.search_one()

    def get_site_info(self):
            for _ in self.json['platform']:
                if _['id']==self.flats:
                    self.token = _['token']
                    self.air_tsno =_['airTSNO']
                    self.telemetry_tsno = _['telemetryTSNO']
                    self.car_tsno = _['carTSNO']
                    self.sitename=_['site']
                    self.air_mthod_id = _['air']
                    self.telemetru_mthod_id = _['telemetry']
                    self.car_mthod_id = _['carflow']
                    return
    def search_one(self):
        try:
            self.fun = self.map_fun()
            self.result_text.setText('<font size="8" color="red"><b>正在查询</b></font>')   
        except:
            space = ['&nbsp;' for _ in range(7)]
            self.result_text.setText(''.join(space)+'<font size="8" color="red"><b>请选择查询的数据</b></font>')
            self.search.setEnabled(True)
            return
        space = ['&nbsp;' for _ in range(12)]
        for _ in self.fun:
            key,f,mthod_id = list(_)
            #key 查看需要测试的是哪个数据
            print(key,f.__name__)
            test_site = self.site.currentIndex()
            if key:
                print('开始···')
                if 'air' in f.__name__:
                    if test_site in [0,-1]:
                        self.tsno = self.air_tsno.values()
                    else:self.tsno = self.air_tsno[self.site.currentText()]
                    self.TSNO = self.air_tsno
                        
                if 'telemetry' in f.__name__:
                    if test_site in [0,-1]:self.tsno = list(self.telemetry_tsno.values())
                    else:self.tsno = self.telemetry_tsno[self.site.currentText()]
                    self.TSNO = self.telemetry_tsno
                if 'car' in f.__name__:
                    if test_site in [0,-1]:self.tsno =list(self.car_tsno.values())
                    else:self.tsno = self.car_tsno[self.site.currentText()]
                    self.TSNO = self.car_tsno
                # print('tsno-----ui,',self.tsno)
                url,param = None,None
                for _ in self.json['request']:
                    if _['id']==mthod_id and _['platid']==self.flats:
                        url = _['url']
                        param =_['param']
                        break
                print('start--#')
                print(f.__name__)
                strs = f(url,param,self.tsno,self.TSNO,self.token)
                # strs = f()
                self.result_text.setText(''.join(space)+'<font size="8" color="red"><b>查询完毕</b></font><br>\n'
                    +strs+'<br>')
                # self.search.setDisabled(False)
                self.search.setEnabled(True)
                break

    def flat(self,value):
        if self.qingyuan.isChecked():
            self.flats ='01'
            self.site.clear()
            self.site.addItem('全部')
            self.get_site_info()
            self.site.addItems(self.sitename)
            self.search_data()
        if self.guangzhou.isChecked():
            self.flats='02'
            self.site.clear()
            self.site.addItem('全部')
            self.get_site_info()
            self.site.addItems(self.sitename)
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
        self.car_hour =False
        self.car_day = False
        self.car_mon =False
        self.car_year=False
        if self.car_flow_hour.isChecked():
            self.car_hour =True
        if self.car_flow_day.isChecked():
            self.car_day =True
        if self.car_flow_mon.isChecked():
            self.car_mon = True
        if self.car_flow_year.isChecked():
            self.car_year =True
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
        self.telem_data,self.telem_day,self.telem_mon,
        self.car_hour,self.car_day,self.car_mon,self.car_year]
        values =[C.air_quality,C.air_quality_data_manger,C.air_quality_statistics_day,C.air_quality_statistics_month,C.air_quality_statistics_year,
        C.telemetry_data_manerger,C.telemetry_data_day,C.telemetry_data_month]+[C.car_flow]*4
        if self.flats=='02':
            self.air_mthod_id=[0,0,0,0,0] # 广州平台没有空气质量
        alls_metho_id = self.air_mthod_id+self.telemetru_mthod_id+self.car_mthod_id
        print(alls_metho_id)
        return zip(key,values,alls_metho_id)
    def search_data(self):
        for _ in self.json['platform']:
            if _['id']==self.flats:
                have_air = _['air']
                have_telemetr = _['telemetry']
                have_car = _['carflow']
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
        if have_car:
            for _ in self.cars:
                _.setEnabled(True)
        else:
            for _ in self.cars:
                _.setEnabled(False)
class opI(Gui):
    '''
        界面操作接口
    '''
    def __init__(self,parent=None):
        super(opI,self).__init__()
        t1 =QThread()
        # Thread(target=lambda:self.ui.show()).start()

    def search_waittime(self):
        self.ui.result_text.setText('正在查询···')
if __name__=='__main__':
    ui = Gui()
    ui.show()
    # ui.pre.pre_search.emit()
    # opI()
    sys.exit(app.exec_())
