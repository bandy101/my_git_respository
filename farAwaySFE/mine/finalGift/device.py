from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from ui.mainUI import Ui_Main
from ui.mainUItest import Ui_Form
import sys,os,json

class DeviceGui(QWidget,Ui_Form):
    """ 最后的酱油界面 """
    
    # 站点
    siteA = None
    siteB = None
    siteC = None
    siteD = None
    siteF = None
    siteE = None
    siteG = None
    siteSet = []
    siteSet.extend((siteA,siteB,siteC,siteD,siteE,siteF,siteG))


    flats = []
    def __init__(self):
        super(DeviceGui,self).__init__()
        self.setupUi(self)
        self.site_rows = 1 # 站点布局的行数

        # load
        with open('Telemetry.json',encoding='utf-8') as f:
            self.json = json.load(f)
            for _ in self.json['platform']:
                self.flats.append(_['plat'])
        self._rdb_site = zip(self.siteSet,self.flats)

        self.addplat()
        
    # 添加平台
    # @property
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
            print('index:',self.site_rows,firstRow,endRow)
            strength = 24
            writeSite = site_[firstRow:endRow]
            if not row:
                writeSite= site_[:firstRow]
           
            coordH_ =coordH - row*16 
            for flat,_ in zip(self.flats,writeSite):
                w,h = int(len(flat))*15+16,20
                x,y = (strength,coordH_-h/2)
                strength += len(flat)*15+16
                print((x,y,w,h))
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
        # try :
        nameC.toggled.connect(self.checkflat)
        print('type:',type(nameC))
        # except Exception as e:
        #     print(e)
        #     print(name)

    def checkflat(self,btn):
        a = '新乡'
        print(a,self.siteSet)

        sitename = None
        # 加载选中的站点信息
        for rb,flat in self._rdb_site:
            if rb.isChecked():
                sitename = rb.text()
                break
        sitesName = None
        for _ in self.json['platform']:
            if _['plat'] == str(sitename):
                print('####:')
                if _['checkAir'] == 'True':sitesName = _['airTSNO'].keys()
                else:
                    if _['checkTelemetry'] == 'True':
                        sitesName = _['telemetryTSNO'].keys()
        # print('##~~:',list(sitesName))
        self.site.clear()
        self.site.addItem('全部')
        # if btn.isChecked():
        #     print(btn.text(),'选中')
        self.site.addItems(list(sitesName))
        
def main():
    app = QApplication(sys.argv) # ui主程序
    ui = DeviceGui()
    ui.show()
    sys.exit(app.exec_())
    

if __name__ == '__main__':
    main()