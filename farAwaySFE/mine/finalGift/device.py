from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from ui.mainUI import Ui_Main
from ui.mainUItest import Ui_Form
import sys,os,json,time
from threading import Thread
from __init__ import *

class DeviceGui(QWidget,Ui_Form):
    """ 最后的酱油界面 """
    '''
        车流量功能设备编号和遥测设备编号一致
        操作遥测的时候同时操作车流量
    '''
    # 站点

    isselect = False # 是否选择功能
    siteSet = [] # 站点集合
    sitename = None # 站点名称
    flats = [] # json全部站点名称
    url = None # 平台地址
    user = None # 用户名
    pwd = None # 用户密码
    cityId = None        # 省函数
    countyId = None
    provinceId = None 
    selectSearch = None # 查询的功能名称
    firstselectplat = False
    function = None  # 查询函数
    tsno = None # 平台站点集合中某个设备号
    TSNO = None # 平台站点集合 （dict）

    signal_settext = pyqtSignal(str) #显示查询结果
    signal_start_search = pyqtSignal(int) #最初的等待查询显示

    def __init__(self):
        super(DeviceGui,self).__init__()

        self.setupUi(self)
        self.site_rows = 1 # 站点布局的行数

        # load
        with open('Telemetry.json',encoding='utf-8') as f:
            self.json = json.load(f)
            for _ in self.json['platform']:
                self.flats.append(_['plat'])

        # 功能选项
        self.airs =[self.air_quality,self.air_quality_data,self.air_quality_day,self.air_quality_mon,self.air_quality_year]
        self.telemetrys =[self.telemetry_data,self.telemetry_day,self.telemetry_mon]
        self.cars = [self.car_flow_hour,self.car_flow_day,self.car_flow_mon,self.car_flow_year]
        self.all_radio =self.airs+self.telemetrys+self.cars
        self.lightstrength.toggled.connect(self.checkTestselect)
        for _ in self.all_radio:
            _.toggled.connect(self.checkTestselect)
        self.signal_start_search.connect(self.cx)
        self.signal_settext.connect(self.set_text)
       
        # 默认平台
        self.addplat,self.siteSet[0].setChecked(True)

    # 添加平台
    @property
    def addplat(self):
        _weight, _height = self.PlatgroupBox.width(), self.PlatgroupBox.height()
        coordW, coordH = _weight/2, _height/2 # radiobutton起始居中位置
        
        # 测试
        site_ = self.flats

        indexFS = len(site_[0])*15 + 16
        indexF = indexFS
        index = 1 # 第几个站点
        firstRow = None # 第一行
        endRow = None
        # coordX = [] # 站点的位置
        for _ in site_[1:]:
            indexF +=len(_)*15 + 16
            index +=1
            if indexF > _weight-17*2:
                self.site_rows +=1
                indexF = indexFS
                if self.site_rows ==2:firstRow = index -1
            if self.site_rows ==3:
                endRow = index -1
                self.site_rows -=1
                break
        # 写入行
        for row in range(self.site_rows):
            strength = 24
            writeSite = self.flats[firstRow:endRow]
            _flat = self.flats[firstRow:endRow]
            if not row:
                writeSite= self.flats[:firstRow]
                _flat = self.flats[:firstRow]
            coordH_ =coordH - row*16 
            for flat,_ in zip(_flat,writeSite):
                w,h = int(len(flat))*15+16,20
                x,y = (strength,coordH_-h/2)
                strength += len(flat)*15+16
                self._addplat(_,flat,(x,y,w,h))
        # eg.居中显示
        # name = '清远'
        # w,h = int(len(name))*15+16,20
        # x,y = (coordW-w/2,coordH-h/2)
        # self._addplat(name,(x,y,w,h))

    # 设置平台
    def _addplat(self,nameC,name,Geometry: tuple):
        """
            name str:添加平台的名称
            Geometry tuple:几何坐标(x,y,w,h) 注意 PlatgroupBox 边界
        """
        nameC = QRadioButton(self.PlatgroupBox)
        nameC.setObjectName(name)
        nameC.setGeometry(QRect(*Geometry))
        nameC.setText(name)
        nameC.toggled.connect(self.checkplat)
        self.siteSet.append(nameC)

    # 选中对应平台radio按钮
    def checkplat(self,btn):
        self.initTestselect()
       # 加载选中的站点信息
        for rb,flat in zip(self.siteSet,self.flats):
            if rb.isChecked():
                self.sitename = rb.text()
                break
        for _ in self.json['platform']:
            if _['plat'] == str(self.sitename):
                self.url = _['indexlogin']
                self.user ,self.pwd = _['username'], _['password']
                self.cityId = _['cityId']
                self.countyId = _['countyId']
                self.provinceId = _['provinceId']
                # 检测
                if _['checkAir'].lower() == 'true':
                    for __ in self.airs:
                        __.setEnabled(True)
                if _['checkTelemetry'].lower() == 'true':
                    for __ in self.telemetrys+self.cars:
                        __.setEnabled(True)
                break
    
        self.site.clear()
        if not self.firstselectplat:
            self.site.addItem('请选择查询的功能')
        else:
            self.checkTestselect(None)
        
    
    # 初始化测试选项
    def initTestselect(self):
        for _ in self.all_radio:
            _.setEnabled(False)

    # 选择测试功能radiobutton #
    def checkTestselect(self,btn):
        self.firstselectplat = True
        sitesName = ''
        self.token = self.json['request']['token']
        for __ in self.json['platform']:
            if __['plat'] == str(self.sitename):
                if  self.lightstrength.isChecked():
                    self.TSNO = None
                    self.function = searchMap()['光强']
                    break
                for _ in self.all_radio:
                    if _.isChecked():
                        self.param = self.json['param'][_.text()]
                        self.selectSearch = self.json['request'][_.text()]
                        self.function = searchMap()[_.text()]
                        if '遥测' in _.text() or '车流量' in _.text():
                            sitesName = __['telemetryTSNO'].keys()
                            self.TSNO = __['telemetryTSNO']
                        if '空气' in _.text():
                            sitesName = __['airTSNO'].keys()
                            self.TSNO = __['airTSNO']
                        break
                else:
                    self.TSNO = None
                break
        # else:
        #     return False

        self.site.clear()
        if sitesName:
            self.site.addItem('全部')
        else:
            self.site.addItem('None')
        self.site.addItems(list(sitesName))
        self.isselect = True

    @pyqtSlot()
    def on_search_clicked(self):
        # self.site.currentIndex()
        # self.site.currentText()
        self.wait =True
        self.search.setEnabled(False)

        Thread(target=self._search).start()
        Thread(target=self.wait_search).start()

    # 刚点击查询无返回结果
    def cx(self,i):
        s ='<font size='+str(i)+' color="red"><b>正在查询···</b></font>'
        self.result_text.clear()
        self.result_text.setText(s)

    # 查询
    def _search(self):

        if not self.isselect:
            QMessageBox.warning(self,
                                    "!!!",  
                                    "请选择查询的功能",  
                                    QMessageBox.Yes)
            return
        if self.TSNO:
            token = 'bearer '+get_token(self.url+self.token,self.user,self.pwd)
            url = self.url+self.selectSearch # 查询的完整url
            tsno = None
            if self.site.currentIndex() in [0,-1]:
                tsno = self.TSNO.values()
            else:
                tsno = self.TSNO[self.site.currentText()]
            param = self.Param
            _x = self.function(url,param,tsno,self.TSNO,token)
        else:# 光强
            print(self.function.__name__)
            _x = self.function()
        self.wait =False
        time.sleep(0.05)
        space = ['&nbsp;' for _ in range(12)]
        strs =''.join(space)+'<font size="8" color="red"><b>查询完毕</b></font><br>\n'+_x
        self.signal_settext.emit(strs)

    # 设置文字
    def set_text(self,str):
        self.result_text.setText(str)
        self.search.setEnabled(True)


    @property
    def Param(self):
        _Param = self.param
        keys = _Param.keys()
        if 'cityId' in keys:
            _Param['cityId'] = self.cityId
        if 'provinceId' in keys:
            _Param['provinceId'] = self.provinceId
        if 'countyId' in keys:
            _Param['countyId'] = self.countyId
        return _Param



    def wait_search(self):
        i=9
        while True:
            if self.wait:
                if i >3:i=i-1
                else:i =9
                self.signal_start_search.emit(i)
                time.sleep(1.2)
            else:break

def main():
    app = QApplication(sys.argv) # ui主程序
    ui = DeviceGui()
    ui.show()
    sys.exit(app.exec_())
    

if __name__ == '__main__':
    main()