from os import path 
import os,cv2,time,re
import numpy as np
import sys,shutil
import re
def cv_imread(f_path):
    img = cv2.imdecode(np.fromfile(f_path,dtype=np.uint8),-1)
    return img
def cv_imwrite(f_path,im):
    cv2.imencode('.jpg',im)[1].tofile(f_path)#保存图片

'''
    cv2.flip(im1,0)) #0 垂直翻转 >=1 水平翻转
'''

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
    
    # lbp的辅助操作 
    def _get_neighbor(self,mat,i,j):
        center = mat[i,j][-1]
        x1,y1= i+1,j+1
        result = 0
        for k in range(8):
            result = result + (mat[x1,y1][-1]>center)*(1<<k)
            if y1-j>=0:
                y1 =y1-1
            else:
                x1,y1 = x1 -1,j+1
            if (x1,y1) in [(i,j)]:y1 = y1-1
        return result

    #归一化
    def _normlize(self,a):
        r = max(a)-min(a)
        a = a-min(a)
        a = a/r
        return a
   
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

    
    #处理黑烟视频素材
    def grabVideo(self,flag: str,placeName: str=None,scale: float=0.4,serialNumber: int=0,):
        """ 获取视频素材    flag[ test,train]
        截出的图片以`日期_地名_编号`的格式命名
        @videoPath str: 视频路径
        @placeName str: 地点名称
        @scale float: 显示图片缩放比例(0~1,默认0.4)
        @serialNumber: 起始编号
        """ 

        # videoPath: str,
        videoPath = r'H:\AI_Data\海康Data\海康数据\青岛\视频\非黑烟视频\测试夹\非黑烟视频\20181212 青岛\20181212_青岛_022.mp4'
        fs = path.basename(videoPath)
        placeName= fs[:-4]
        from datetime import datetime
        today = datetime.now().strftime('%Y%m%d%H%M%S')
        _bianhao = str(today).split('.')[-1]
        
        # placeName = _bianhao

        # saveDirName = path.join(path.dirname(videoPath),path.basename(videoPath)[:path.basename(videoPath).rindex('.')])
        saveDirName = path.dirname(path.dirname(path.dirname(videoPath))) #测试训练夹
        
        #初始化目录
        # if all([path.exists(saveDirName),path.isdir(saveDirName)]):
        #     import shutil
        #     try:shutil.rmtree(saveDirName)
        #     except:
        #         for p,d,fs in os.walk(saveDirName):
        #             for _ in fs:os.remove(path.join(p,_))
        srcDir = path.join(saveDirName,'src',path.basename(path.dirname(videoPath)),flag,str(1))
        dstDir = path.join(saveDirName,'dst',path.basename(path.dirname(videoPath)),flag,str(1))
        print(srcDir,dstDir)
        _srcDir = path.join(saveDirName,'src',path.basename(path.dirname(videoPath)),flag,'0') #posive
        _dstDir = path.join(saveDirName,'dst',path.basename(path.dirname(videoPath)),flag,'0')
        os.makedirs(srcDir,exist_ok=True),os.makedirs(dstDir,exist_ok=True)
        os.makedirs(_srcDir,exist_ok=True),os.makedirs(_dstDir,exist_ok=True)# f——Key 收集负样本

        cap = cv2.VideoCapture(videoPath)
        # namedWindow 默认情况下，是1，自动调整窗口大小模式。如果在图片高清情况下，显示图片窗口很大，电脑屏幕放不下，
        # 并且窗口还不能通过拖动鼠标来调整打下。Flags=0，是WINDOW_NORMAL，在这个模式下可以调整窗口的大小.
        cv2.namedWindow(self._widghtName,1),cv2.setMouseCallback(self._widghtName,self._callBack)
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
                    _ =f'{placeName}_{index:04}.jpg' 
                    # _ = f'{today}_{path.basename(videoPath)[9:-4]}_{index:04}.jpg'
                    try:
                        self._write_sample(path.join(dstDir,_),self._tempIm)
                        cv_imwrite(path.join(srcDir,_),self._img)
                        index +=1
                    except:break
                if key in[70,102]:#f #position
                    _ =f'{placeName}_{index:04}.jpg' 
                    try:
                        self._write_sample(path.join(_dstDir,_),self._tempIm)
                        cv_imwrite(path.join(_srcDir,_),self._img)
                        index +=1
                    except:break
            if not switch:break
    #处理黑烟图片素材
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
        try:
            os.makedirs(srcDir),os.makedirs(dstDir)
            # os.makedirs(_srcDir),os.makedirs(_dstDir) #接触f 负样本
        except:pass
        cv2.namedWindow(self._widghtName),cv2.setMouseCallback(self._widghtName,self._callBack)
        switch =True#图像显示开关
        index = serialNumber
        for p,d,f in os.walk(picPath):
            if any([srcDir in p,dstDir in p,_srcDir in p,_dstDir in p]):continue
            for _ in f:
                if _[-3:].lower() in ['jpg','jpeg','png']:
                    print('start')
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
    #移动一个目录所有特定文件
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
    #处理黑烟记录   
    def smokeManager(self,*arg):
        def down_video():
            pass


    # 使用对应标准分类黑烟视频
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
                dt = f
                if '-' in f:
                    dt = f.replace('-','')
                    print(dt,f)
                siteName = path.basename(p)
                # print(siteName)
                #判断视频文件命名方式转换对应格式[ID,format(date),timestamp]
                if f[0] in ['4']:
                    idDir = path.join(targitDir,'未知时间')
                    os.makedirs(idDir,exist_ok=True)
                    shutil.copy(path.join(p,f),idDir)
                else:
                    if f[0] in ['1']:
                        dateName = time.strftime('%Y%m%d',time.localtime(int(dt[:10])))
                    elif f[0] in ['2']:
                        dateName =dt[0:8]
                    else:
                        dateName =dt[9:17]
                    dateDir =  path.join(targitDir,dateName+' '+platform)
                    os.makedirs(dateDir,exist_ok=True)
                    newVideoName = f"{dateName}_{siteName}_{index:04}"
                    shutil.copy(path.join(p,f),path.join(dateDir,newVideoName+f[-4:]))
                    index +=1

    # 从分类完成的视频中筛选出符合要求
    def classifyVideo_(self,srcPath: str,arg: str):
        #使用ANSI  避免乱码
        '''
        @pramer
        srcPath str:分类的文件夹
        *arg :特殊参数文本 (关键词_serialNumber):文本名称
        '''
        csfName,start= ['非黑烟视频','不明显'],1
        import re
        for k in [arg]:
            with open(k,mode='r+') as ff:
                text = ff.read()
                results =[_ for _ in re.split('[\s]',text) if _ not in['',None]]
                for p,d,fs in os.walk(srcPath):     #H:\AI_Data\素材库_黑烟视频\分站点\all\视频素材\黑烟视频
                    if d in [[]]:targitDir = path.join(path.dirname(path.dirname(p)),csfName[start],path.basename(p))
                    for f in fs:
                        #if any([all([_x in f for _x in a.split('_')]) for a in results if ]):
                        for r in results:
                            # print(r.split('-'),[_x in f for _x in r.split('_')])
                            if all([_x in f for _x in r.split('-')]):
                                os.makedirs(targitDir,exist_ok=True)
                                print(r)
                                results.remove(r)
                                shutil.move(path.join(p,f),targitDir)
                                break
            print(results)
            start +=1

    # 合并线上记录的黑烟
    def smokeSet(self,srcPath: str,dstPath: str=None,tagt :str='dest'):
        '''
            description:
            将分好的视频合并成对应的站点
            eg.
            -K
                A           B       
                    -a          -a
                    -b          -b
            将A、B文件夹中对应的文件夹[a,b]中相同名称的文件夹中的文件合并在
            (默认)当前目录的tagt中
        @paramer
            srcPath str:A、B的上层目录K
            dstPath str:默认(K/tagt)
            tagt str:子目录名称
        '''

        if not dstPath:dstPath=srcPath
        dstPath =path.join(dstPath,tagt)
        if not path.exists(dstPath):os.makedirs(dstPath,exist_ok=True)
        for p,d,fs in os.walk(srcPath):
            if tagt in p:continue
            targitD = path.join(dstPath,path.basename(p))
            for f in fs:
                if  'train' not in targitD and 'test' not in targitD: #--计算素材库的量
                    if 'train' in p:
                        targitD +='/train'
                    if 'test' in p:
                        targitD +='/test'
                os.makedirs(targitD,exist_ok=True)
                shutil.copy(path.join(p,f),targitD)                          


    # word文档表格生成
    def wordG(self,dataPath: str,delimiter: str='#'):
        '''
        dataPath str:导入的数据路径
        delimiter str:分隔符（界定符）
        '''

        from docx import Document
        from docx.shared import Inches
        document = Document()
        table = document.add_table(rows=35, cols=5,style="Table Grid")
        heading_cells = table.rows[0].cells
        heading_cells[0].text = '车牌号'
        heading_cells[1].text = '车牌颜色'
        heading_cells[2].text = '抓拍时间'
        heading_cells[3].text = '抓拍点位'
        heading_cells[4].text = '林格曼等级'
        index = 0
        with open(dataPath,mode='r+') as f:
            text = f.readline()
            while text:
                print(text.split('\t'))
                try:
                    # for j,_ in enumerate(re.split('[\s]',text)):
                    for j,_ in enumerate(text.split(delimiter)):
                        table.cell(index,j).text= _
                except:pass
                text = f.readline()
                index +=1

        document.save('test.docx')

    # excel 生成
    def excelX(self):
        '''
        description:
        '''
        
    def importData(self,url: str):
        pass

    # 间隔取一定数目文件                 
    def filtrate(self,paths: str,num: int,targitPath: str='targit'):
        '''num: 数目'''
        index = 0
        targitPath = path.join(paths,targitPath)
        os.makedirs(targitPath,exist_ok=True)
        for p,d,f in os.walk(paths):
            if targitPath in p: continue
            for _ in f:
                if not index%num:
                    shutil.copy(path.join(p,_),targitPath)
                index +=1

    # LBP
    def LBP(self,img):
        '''设置灰度阈值
            BP的基本思想是定义于像素的8邻域中,以中心像素的灰度值为阈值,
            将周围8个像素的值与其比较,如果周围的像素值小于中心像素的灰度值,
            该像素位置就被标记为0,否则标记为1.每个像素得到一个二进制组合,
            就像00010011.每个像素有8个相邻的像素点,即有2^8种可能性组合 
        '''
        dst = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        mat = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
        h,w = dst.shape
        for i in range(1,h-1):
            for j in range(1,w-1):
                dst[i,j] =self._get_neighbor(mat,i,j)
        return dst
    
    # 巴适距离 筛选相似的图片
    def get_probility(self,im1,im2):
        '''
            @im1,im2 灰度图
            通过比对 对应灰度值的频率
            return 相似的的概率(0~1)
        '''
        hist0,_ = np.histogram(im1.ravel(),256,[0,256])
        hist1,_ = np.histogram(im2.ravel(),256,[0,256])
        a ,b= self._normlize(hist0),self._normlize(hist1)
        BC = sum(np.sqrt(a*b))  
        prob_0 = BC/np.sqrt(sum(a)*sum(b))  #原始巴适距离
        prob_1 = 1-np.sqrt(1-(BC/np.sqrt(sum(a)*sum(b)))) #进行优化
        return prob_1

    # 对于不同文件夹存放相同名称文件 进行同步(删除)
    def delsNoSrc(self,src: str='原始素材',**arg):
        '''删除src[原始素材]中没有的文件'''

        _index  = 0 # 删除数量
        allFiles = [ _ for p,d,f in os.walk(src) for _ in f]
        print((allFiles))
        if not arg:
            srcPrfix = src.split('原始素材')[0]
            arg = [path.join(srcPrfix,'原图')]
        for _ in arg:
            print('arg:',arg)
            for p,d,fs in os.walk(_):
                for f in fs:
                    if f not in allFiles:
                        os.remove(path.join(p,f))
                        _index +=1
                        print(f'删除:{path.join(p,f)} 成功{_index:04}')
                        
    #重新命名目录下的文件名称
    def rename(self,srcPath: str):
        """重命名"""
        _index = 0
        for p,d,f in os.walk(srcPath):
            for _ in f:
                if path.isfile(path.join(p,_)):
                    _index +=1
                    _r = f'{_index:04}.jpg'
                    shutil.move(path.join(p,_),path.join(p,_r))

    #2018.12.14 
    def Classify(self,srcPath):
        dstP = path.join(srcPath,'视频')
        pattern = re.compile(r'\d')
        allData = [path.join(srcPath,_) for _ in os.listdir(srcPath) if path.isdir(path.join(srcPath,_))]  
        for _ in allData:
            _dateName = '2018'+''.join(pattern.findall(_))
            for p,d,f in os.walk(_):
                if '黑烟视频' in d:
                    _tP = path.join(p,'黑烟视频')
                    index = 0
                    for _f in os.listdir(_tP):
                        _name = f'{_dateName}_青岛_{index:03}.mp4'
                        index +=1
                        os.makedirs(path.join(dstP,'黑烟视频',_dateName+' 青岛'),exist_ok=True)
                        shutil.copy(path.join(_tP,_f),path.join(dstP,'黑烟视频',_dateName+' 青岛',_name))

                    # shutil.copytree(_tP,path.join(dstP,_dateName))
                if '非黑烟视频' in d:
                    index = 0
                    _tP = path.join(p,'非黑烟视频')
                    for _f in os.listdir(_tP):
                        _name = f'{_dateName}_青岛_{index:03}.mp4'
                        index +=1
                        os.makedirs(path.join(dstP,'非黑烟视频',_dateName+' 青岛'),exist_ok=True)
                        shutil.copy(path.join(_tP,_f),path.join(dstP,'非黑烟视频',_dateName+' 青岛',_name))
                    # shutil.copytree(_tP,path.join(dstP,_dateName))

    #2018.12.14
    def moveS(self,srcPath):
        '''
            将srcPath 目录【训练夹和测试夹】 里面的文件 转换成对应的结构
                -训练夹
                    ---黑烟视频
                            ---日期来源
                                ----日期_来源_编号
        '''
        #srcP = H:\AI_Data\海康Data\海康数据\青岛\视频\黑烟视频
        alls = [path.join(srcPath,_) for _ in os.listdir(srcPath) if '青岛' in _]
        _ttt = path.join(srcPath,'训练夹')
        _t = [_ for _ in os.listdir(_ttt)]
        for a in alls:
            for p,d,f in os.walk(a):
                for _ in f:
                    if _ in _t:
                        path_ = path.join(_ttt,path.basename(path.dirname(p)),path.basename(p))
                        os.makedirs(path_,exist_ok=True)
                        shutil.copy(path.join(p,_),path.join(path_,_))
if __name__ == '__main__':
    from fire import Fire
    Fire(BlackBox)