from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
from main_ui import Ui_Form
from threading import Thread
# from main import Ui_Form

import check_pt as C
# import check_device as D
import json
import time
import requests
app = QApplication(sys.argv)




class Gui(QWidget,Ui_Form):

    # signal_search =pyqtSignal() #控制查询按钮
    signal_settext = pyqtSignal(str) #显示查询结果
    signal_start_search = pyqtSignal(int) #最初的等待查询显示
    def __init__(self):
        super(Gui,self).__init__()
        self.setupUi(self)
        print('provinceID:',int(QThread.currentThreadId()))
        with open('config.json',encoding='utf-8') as f:
            alls = json.load(f)
            self.json = alls
        ##实时令牌
        for _ in self.json['platform']:
            url_qy= 'http://202.105.10.126:8055/api/v1/login/'
            url_gz = 'https://gz.etc-cn.com/api/v1/login/'
            try:
                if _['id']=='01':
                    self.json['platform'][0]['token']='bearer '+get_token(url_qy,'demo','demo&123')
            except:
                pass
            try:
                if _['id']=='02':
                    self.json['platform'][1]['token']='bearer '+get_token(url_gz,'demo','demo&123')
                if _['id']=='03':
                    self.json['platform'][1]['token']='bearer '+get_token(url_gz,'demo','demo&123')
            except:
                pass
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
        self.signal_search.connect(self.clicks)
        # self.light_intensity.clicked.connect(self.lights)
        self.signal_settext.connect(self.set_text)
        self.signal_start_search.connect(self.cx)
        # self.search.clicked.connect(self.bt)cx

        ##线程查询
        # self.timer=QTimer()
        # self.timer.timeout.connect(self.wait_search)
        # self.timer.start(200)
        # self.search.clicked.connect(self.search_one)
        # self.search_t =myThread()
        # self.search_t.pre_search.connect(self.search_one) ##绑定需要执行的函数

        ##初始化平台
        self.flat(None)
        self.qingyuan.toggled.emit(True)
    def wait_search(self):
        i=9
        while True:
            if self.wait:
                if i >3:i=i-1
                else:i =9
                self.signal_start_search.emit(i)
                time.sleep(1.2)
            else:break
    def cx(self,i):
        s ='<font size='+str(i)+' color="red"><b>正在查询···</b></font>'
        self.result_text.clear()
        self.result_text.setText(s)
    @pyqtSlot()
    def on_light_intensity_clicked(self):
        self.wait =True
        self.light_intensity.setEnabled(False)
        # self.result_text.setText('<font size="8" color="red"><b>正在查询</b></font>')
        Thread(target=self.lights).start()
        Thread(target=self.wait_search).start()
    @pyqtSlot()
    def on_search_clicked(self):
        # self.search_one()
        self.wait =True
        self.search.setEnabled(False)
        # self.result_text.setText('<font size="8" color="red"><b>正在查询</b></font>')
        Thread(target=self.search_one).start()
        Thread(target=self.wait_search).start()


    def lights(self):
        space = ['&nbsp;' for _ in range(12)]
        strs = C.check_(20)
        strs =''.join(space)+'<font size="8" color="red"><b>查询完毕</b></font>'+strs
        self.wait =False
        time.sleep(0.05)
        self.signal_settext.emit(strs)


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
    def set_text(self,str):
        self.result_text.setText(str)
        self.search.setEnabled(True)
        self.light_intensity.setEnabled(True)
    def search_one(self):
        print('provinceChildrenID:',int(QThread.currentThreadId()))
        try:
            self.fun = self.map_fun()
            # self.result_text.setText('<font size="8" color="red"><b>正在查询</b></font>') 
        except:
            space = ['&nbsp;' for _ in range(7)]
            # self.result_text.setText(''.join(space)+'<font size="8" color="red"><b>请选择查询的数据</b></font>')
            # self.search.setEnabled(True)
            strs = ''.join(space)+'<font size="8" color="red"><b>请选择查询的数据</b></font>'
            self.signal_settext.emit(strs)
            # return (''.join(space)+'<font size="8" color="red"><b>请选择查询的数据</b></font>')
        space = ['&nbsp;' for _ in range(12)]
        for _ in self.fun:
            key,f,mthod_id = list(_)
            #key 查看需要测试的是哪个数据
            # print(key,f.__name__)
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
                    self.TSNO = self.A
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
                strs =''.join(space)+'<font size="8" color="red"><b>查询完毕</b></font><br>\n'+strs
                self.wait =False
                time.sleep(0.05)
                self.signal_settext.emit(strs)
                
                # return (''.join(space)+'<font size="8" color="red"><b>查询完毕</b></font><br>\n'+strs)
                # strs = f()


                # self.result_text.setText(''.join(space)+'<font size="8" color="red"><b>查询完毕</b></font><br>\n'
                #     +strs+'<br>')
                # self.search.setDisabled(False)
                # self.search.setEnabled(True)
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
        self.air_day = False
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
def get_token(url,name,pwd):
    js_pwd ={
    "clientId":"098f6bcd4621d373cade4e832627b4f6",
    'userName':name,
    'password':pwd
    }
    res = requests.post(url,json=js_pwd,verify=False)
    res =json.loads(res.content)
    token = res['content']['token']
    return token

class opI:
    '''
        界面操作接口
    '''
    def __init__(self,parent=None):
        self.ui = Gui()
        # self.ui.signal_search.connect(self.ui.bt)
        self.ui.show()
        # Thread(target=lambda:self.ui.show()).start()

    def search_waittime(self):
        self.ui.result_text.setText('正在查询···')


if __name__=='__main__':
    ui = Gui()
    ui.show()
    sys.exit(app.exec_())
    # url_qy= 'http://202.105.10.126:8055/api/v1/login/'
    # url_gz = 'https://gz.etc-cn.com/api/v1/login/'
    # print('#',get_token(url_gz,'demo','demo&123'))
