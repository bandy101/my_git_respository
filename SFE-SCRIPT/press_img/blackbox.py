from os import path 
import os,cv2,time
import numpy as np
import sys,shutil

def cv_imread(f_path):
    img = cv2.imdecode(np.fromfile(f_path,dtype=np.uint8),-1)
    return img
def cv_imwrite(f_path,im):
    cv2.imencode('.jpg',im)[1].tofile(f_path)#保存图片


_BlackBox__img = None
class BlackBox:
    """ 黑盒 """
    def __init__(self):
        '''
        ```@没有你想不到的打杂工具@```

        @grabVideo:抓取黑烟视频素材
        @grabVideo:抓取黑烟图片素材
        '''
        self._widghtName = 'ImageShow' 
        #self._img = None
        self._drawing=False
    def _loadMouseCallback(self):
        '''
        @
        '''
        return self.__callBack

    def __callBack(self,event,x,y,flags,param):
        # 当按下左键是返回起始位置坐标
        if event==cv2.EVENT_LBUTTONDOWN:
            self._drawing=True
            self.ix,self.iy=x,y

        # 当鼠标左键按下并移动是绘制图形。event可以查看移动，flag查看是否按下
        elif event==cv2.EVENT_MOUSEMOVE and flags==cv2.EVENT_FLAG_LBUTTON:
            if self._drawing==True:
                    cv2.rectangle(self._tempIm,(self.ix,self.iy),(x,y),(0,0,0),-1)
   
        elif event==cv2.EVENT_LBUTTONUP:
            if self.ix >x and self.iy >y:
                x = x^self.ix
                self.ix =x^x
                x = x^self.ix
                y = y^self.iy
                self.iy = y^self.iy 
                y  = y^self.iy
            self._drawing==False
            self.car_weight = abs(x -self.ix)
            self.car_height = abs(y -self.iy)
            self.right_x,self.right_y = max(x,self.ix),max(self.iy,y)    

    @property
    def _callBack(self):
        return self._loadMouseCallback()

    @property
    def _Img(self):
        return self._img
    
    @property
    def mouseVars(self):
        '''
            返回鼠标回调的参数值
            ix ,iy:起始坐标值
            car_weight,car_height:鼠标最后框中的宽高
        '''
        return self.ix,self.iy,self.car_weight,self.car_height,self.right_x,self.right_y

    def _write_sample(self,paths,img):
        ix,iy,car_weight,car_height,right_x,right_y = self.mouseVars
        '''
            周围的间距 ∈ car_weight/2
        '''
        x1 = max(ix-car_weight//2,0)
        y1 = max(iy-car_weight//2,0)
        x2 = min(right_x+car_weight//2,self._img.shape[1])
        y2 = min(right_y+car_weight//2,self._img.shape[0]) 
        tempImg =img[y1:y2,x1:x2]
        cv_imwrite(paths,tempImg)

    
    #为人民处理黑烟视频素材
    def grabVideo(self,videoPath: str,placeName: str,scale: float=0.4,serialNumber: int=0):
        """ 获取视频素材   
        截出的图片以`日期_地名_编号`的格式命名
        @videoPath str: 视频路径
        @placeName str: 地点名称
        @scale float: 显示图片缩放比例(0~1,默认0.4)
        @serialNumber: 起始编号
        """


        from datetime import datetime
        today = datetime.now().strftime('%Y%m%d')
        saveDirName = path.join(path.dirname(videoPath),path.basename(videoPath)[:path.basename(videoPath).rindex('.')])
        #初始化目录
        if all([path.exists(saveDirName),path.isdir(saveDirName)]):
            import shutil
            try:shutil.rmtree(saveDirName)
            except:
                for p,d,fs in os.walk(saveDirName):
                    for _ in fs:os.remove(path.join(p,_))
        srcDir = path.join(saveDirName,'src')
        dstDir = path.join(saveDirName,'dst')
        _srcDir = path.join(saveDirName,'_src') #posive
        _dstDir = path.join(saveDirName,'_dst')
        os.makedirs(srcDir),os.makedirs(dstDir),os.makedirs(_srcDir),os.makedirs(_dstDir)

        cap = cv2.VideoCapture(videoPath)
        cv2.namedWindow(self._widghtName),cv2.setMouseCallback(self._widghtName,self._callBack)
        switch =True#图像显示开关
        index = serialNumber
        while True:
            ret,self._img = cap.read()
            if not ret:break
            if scale:self._img = cv2.resize(self._img,None,fx=scale,fy=scale)
            self._tempIm = self._img.copy()
            while(1): #等待键值操作
                cv2.imshow(self._widghtName,self._tempIm)
                key = cv2.waitKey(1)&0xFF
                #重新加载当前帧
                if key in[114,82]: # r
                    self._tempIm = self._img.copy()
                if key in[27,32]:#esc,space 
                    break
                if key in[79,111]:#o 退出程序
                    switch =False
                    break
                if key in[86,119]:#w active
                    _ =f'{today}_{placeName}_{index:02}.jpg' 
                    try:
                        self._write_sample(path.join(dstDir,_),self._tempIm)
                        cv_imwrite(path.join(srcDir,_),self._img)
                        index +=1
                    except:break
                if key in[70,102]:#f #position
                    _ =f'{today}_{placeName}_{index:02}.jpg' 
                    try:
                        self._write_sample(path.join(_dstDir,_),self._tempIm)
                        cv_imwrite(path.join(_srcDir,_),self._img)
                        index +=1
                    except:break
            if not switch:break
    #为人民处理黑烟图片素材
    def grabPicture(self,picPath: str,placeName: str,scale: float=0.4,serialNumber: int=0):
        """ 获取图片素材   
        截出的图片以`日期_地名_编号`的格式命名
        @picPath str: 图片文件夹路径
        @placeName str: 地点名称
        @scale float: 显示图片缩放比例(0~1,默认0.4)
        @serialNumber: 起始编号
        """

        from datetime import datetime
        today = datetime.now().strftime('%Y%m%d')
        saveDirName = picPath
        #初始化目录
        # if all([path.exists(saveDirName),path.isdir(saveDirName)]):
        #     import shutil
        #     try:shutil.rmtree(saveDirName)
        #     except:
        #         for p,d,fs in os.walk(saveDirName):
        #             for _ in fs:os.remove(path.join(p,_))
        srcDir = path.join(saveDirName,'src')
        dstDir = path.join(saveDirName,'dst')
        _srcDir = path.join(saveDirName,'_src') #posive
        _dstDir = path.join(saveDirName,'_dst')
        os.makedirs(srcDir),os.makedirs(dstDir),os.makedirs(_srcDir),os.makedirs(_dstDir)
        cv2.namedWindow(self._widghtName),cv2.setMouseCallback(self._widghtName,self._callBack)
        switch =True#图像显示开关
        index = serialNumber
        for p,d,f in os.walk(picPath):
            for _ in f:
                if _[-4:].lower() in ['jpg','jpeg','png']:
                    self._img = cv_imread(path.join(p,_))
                    if scale:self._img = cv2.resize(self._img,None,fx=scale,fy=scale)
                    self._tempIm = self._img.copy()
                    while(1): #等待键值操作
                        cv2.imshow(self._widghtName,self._tempIm)
                        key = cv2.waitKey(1)&0xFF
                        #重新加载当前帧
                        if key in[114,82]: # r
                            self._tempIm = self._img.copy()
                        if key in[27,32]:#esc,space 
                            break
                        if key in[79,111]:#o 退出程序
                            switch =False
                            break
                        if key in[86,119]:#w active
                            _ =f'{today}_{placeName}_{index:02}.jpg' 
                            try:
                                self._write_sample(path.join(dstDir,_),self._tempIm)
                                cv_imwrite(path.join(srcDir,_),self._img)
                                index +=1
                            except:break
                        if key in[70,102]:#f #position
                            _ =f'{today}_{placeName}_{index:02}.jpg' 
                            try:
                                self._write_sample(path.join(_dstDir,_),self._tempIm)
                                cv_imwrite(path.join(_srcDir,_),self._img)
                                index +=1
                            except:break
                    if not switch:break
            if not switch:break
    #改变世界的格局
    def moveFormat(self,srcPath :str,moveType :str='mp4',dstPath :str=None):
        '''
        @srcPath :操作的文件夹目录
        @moveType :操作文件的类型(defalt :mp4)
        @dstPath :目标目录(默认当前输入目录)
        '''
        if not dstPath:dstPath = srcPath
        prefix = 'all_'
        targit = path.join(dstPath,prefix+moveType)
        if not path.exists(targit):os.makedirs(targit)
        print(targit)
        for p,d,f in os.walk(srcPath):
            if path.basename(p)==targit:continue
            for _ in f:
                if _[-3:].lower()==moveType:
                    try:
                        shutil.copy(path.join(p,_),targit)
                    except:
                        print(_)
                        print('p:',p)
        print('移动成功')
    #为世界处理黑烟
    def smokeManager(self,*arg):
        pass
    #使用对应标准分类黑烟视频
    def classifyVideo(self,srcVideoPath: str,dstPath: str=None,platform: str='清远',serialNumber: int=0):
        platform +='平台'
        '''
        description :
            视频素材
                -非黑烟视频
                -黑烟视频
                    -未知时间[ID]
                    -日期+来源(yearmonthday+来源平台) eg.[20181001 清远平台]
                        -视频文件 eg.[20181001_站点名称_serialNumber]
        @paramer
            srcVideoPath :分类的文件夹
            dstPath      :存放的文件夹
        '''
        #index = serialNumber #编号
        if not dstPath:dstPath=srcVideoPath  #输入目录
        targitDir = path.join(dstPath,'视频素材','黑烟视频')
        os.makedirs(targitDir,exist_ok=True)
        for p,d,fs in os.walk(srcVideoPath):
            if '视频素材' in p:continue
            index =serialNumber#编号
            for f in fs:
                siteName = path.basename(p)
                print(siteName)
                #判断视频文件命名方式转换对应格式[ID,format(date),timestamp]
                if f[0] in ['4']:
                    idDir = path.join(targitDir,'未知时间')
                    os.makedirs(idDir,exist_ok=True)
                    shutil.copy(path.join(p,f),idDir)
                else:
                    if f[0] in ['1']:
                        dateName = time.strftime('%Y%m%d',time.localtime(int(f[:10])))
                    elif f[0] in ['2']:
                        dateName =f[0:8]
                    else:
                        dateName =f[9:17]
                    dateDir =  path.join(targitDir,dateName+' '+platform)
                    os.makedirs(dateDir,exist_ok=True)
                    newVideoName = f"{dateName}_{siteName}_{index:04}"
                    shutil.copy(path.join(p,f),path.join(dateDir,newVideoName+f[-4:]))
                    index +=1

if __name__ == '__main__':
    from fire import Fire
    Fire(BlackBox)