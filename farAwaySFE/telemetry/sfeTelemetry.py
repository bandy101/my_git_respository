from __init__ import *

from TCP import TCP


Chunk_Size =1024 #字节数

class SFETelemerty(TCP):
    
    def __init__(self,loginurl: str,Paramer :dict):
        super().__init__(loginurl,Paramer)
        with open('config.json',encoding='utf-8') as f:
            alls = json.load(f)
            self._configs = alls
            self.TSNO  = alls['telemetryEquipment'] #prefix = deviceNumber
            self.TSNO_ = dict(zip(self.TSNO.values(),self.TSNO.keys()))
            self._SITES = None # 站点集合 
    
    # 操作黑烟
    def opSmoke(self,site,recordID,flag: str='status'):
        '''@paramer `` flag∈['status','upload']``` '''

        targitURL = str(self._configs['publicURL'][flag]['url'])
        targitURL.replace('{site}',site)
        targitURL.replace('{record_id}',recordID)
        self.getInfo(targitURL)

    # 鉴赏黑烟
    def authenticate(self,currentPath: str,dirName: str,Names=['车辆误判','黑烟视频','非黑烟']):
        '''     '''
        switch =True #鉴赏的开关
        currentDir =os.getcwd()
        sites = [_ for _ in os.listdir(currentPath) if path.isdir(path.join(currentPath,_)) and _ not  in [dirName]] # 通过文件夹名称获取站点对应名
        print(sites)
        # 初始化开始文件夹
        for _ in Names:
            os.makedirs(path.join(currentPath,dirName,_),exist_ok=True)

        for site in sites:
            _path = path.join(currentPath,site)
            index = -1
            if not switch:
                break
            for f in os.listdir(_path):
                im1,im2 = None,None
                if f[-3:].lower() in ['mp4','avi']:
                    try:
                        im1 = cv_imread(path.join(_path,'image1',f[:-4]+'_1.jpg'))
                        im2 = cv_imread(path.join(_path,'image2',f[:-4]+'_2.jpg'))
                        index +=1
                    except:
                        ''' #重新下载#'''
                        traceback.print_exc()
                        continue
                while(1):
                    try:
                        cv2.imshow('Image1',im1)
                        cv2.imshow('Image2',im2)
                        if not index%50:
                            print(path.join(_path,'image2',f[:-4]+'_2.jpg'))
                    except:
                        traceback.print_exc()
                        break
                    k=cv2.waitKey(1)&0xFF  
                    if k ==32:
                        break
                    if k in [ord('w'),ord('W')]:
                        #写入记录的操作#
                        #print('---写入成功---')
                        cv_imwrite(path.join(currentPath,dirName,'车辆误判',f[:-4]+'_1.jpg'),im1)
                        cv_imwrite(path.join(currentPath,dirName,'车辆误判',f[:-4]+'_2.jpg'),im2)
                        
                    if k in [102,70]: # f 
                        os.chdir(path.abspath(path.join(currentPath,site)))
                        print(f)
                        print(os.getcwd())
                        os.system("\""+f+"\"") #含有空格
                        os.chdir(currentDir) #回到基本路径防止相对路径错误
                    if k==111: #'o' 全部关闭
                        switch = False
                        break
                if not switch:break

    # 获取设备编号(站点)
    @property
    def sitesID(self):
        targitURL = str(self._configs['publicURL']['website']['url'])
        targitURL = self.loginurl + targitURL
        res  = self.getInfo(targitURL)
        print(res.content)
        sites = [_ for _ in json.loads(res.content)['content']]
        return sites

if __name__ == '__main__':
    #inistanse
    pool = ThreadPoolExecutor(max_workers=8) # 线程池初始化
    with open('config.json',encoding='utf-8') as f:
        alls = json.load(f)
    paramer ={ 
        'password':'5313232ef0a55311cf31e00b97afa15c',
        'user':'auditor'
    }


    #--start--#
        #urlPrefix: 网址前缀
        #paths : 操作的根目录
    print('\t请选择区域!')
    flag_site = input('#----1:清远,2:新乡----#:')
    if flag_site=='1':
        urlPrefix = str(alls['sitePosition']['qingyuan'])
        paths = './videoData_qingyuan' 
        
    elif flag_site=='2':
        urlPrefix = str(alls['sitePosition']['xinxiang'])
        paths = './videoData_xinxiang' 

    else:raise '错误的输入！'
    #```初始化 接口
    loginrurl = urlPrefix
    SFET = SFETelemerty(loginrurl,paramer)
    
    #当前时间 year-mon-day
        #day_num 距离当前的日期的天数 （0表示当天）
    now_time ,day_num= datetime.datetime.now(),0
    begindate = (now_time + datetime.timedelta(days = -day_num)).strftime('%Y-%m-%d')
     
    #当前文件夹:root/time(year-mon-day)
    currentPath = path.join(paths,str(begindate))
    if not path.exists(currentPath): os.makedirs(currentPath)
    
    #记录下信息的文件:currentPath/recordinfo
    recordINFO = str(begindate) + '_info.txt'

    #```flag_fun 功能标识
    flag_fun = input('#---q:退出---d:下载---c:确认----u:上传---v:查看图片#:')
    if flag_fun.lower() in ['d','q','d','v','c']:
        if flag_fun.lower() == 'd': #下载
            sites = SFET.sitesID
            video_url = SFET.loginurl + alls['publicURL']['video']['url']    
            image1_url = SFET.loginurl + alls['publicURL']['image1']['url']
            image2_url = SFET.loginurl + alls['publicURL']['image2']['url']
            
            targit_urls= []
            targit_paths = []
            for site in sites:
                downloadPath = path.join(currentPath,SFET.TSNO[site]) #下载的文件夹
                if not path.exists(downloadPath): os.makedirs(downloadPath)
                # 获取站点记录列表
                list_url = urlPrefix+str(alls['publicURL']['websiterecord']['url']).replace("{site}",site)
                lists =json.loads(SFET.getInfo(list_url).content)['content']
                for list_ in lists:
                    if all([list_['status'] in [False],list_['upload']\
                    in ['未上传']]):
                        video_url_ = video_url.replace('{record_id}',str(list_['id'])).replace('{site}',site)
                        image1_url_ = image1_url.replace('{record_id}',str(list_['id'])).replace('{site}',site)
                        image2_url_ = image2_url.replace('{record_id}',str(list_['id'])).replace('{site}',site)
                        targit_urls.extend((video_url_,image1_url_,image1_url_))
                        
                        name = list_['name']
                        #排除非法命名
                        for _ in ['\\','/','*','?','<','>','|',':']:
                            if _ in name:
                                name = name.replace(_,'')
                        
                        targit_path_video  = downloadPath+'/'+str(list_['id'])+'~'+name+'.mp4'
                        targit_path_image1 = path.join(downloadPath,'image1')+'/'+str(list_['id'])+'~'+name+'_1.jpg'
                        targit_path_image2 = path.join(downloadPath,'image2')+'/'+str(list_['id'])+'~'+name+'_2.jpg'
                        targit_paths.extend((targit_path_video,targit_path_image1,targit_path_image2))

                        #记录下载信息(id~name~site)
                        with open(path.join(currentPath,recordINFO),mode='a') as tempF:#'~' 是分隔符
                            tempF.write(str(list_['id'])+'~')
                            tempF.write(name+'~'),tempF.write(str(SFET.TSNO[site]))
                            tempF.write('\n')
                #线程池下载
                    #单个站点下载
                all_task = [pool.submit(SFET.download,url,path_) for url,path_ in zip(targit_urls,targit_paths)]

        if flag_fun.lower() =='c': #确认
            '''
            通过 输入ID 比对recordINFO.split('separator')->[id,name,site]
            '''
        
            print('确认前需要确保各个站点的视频已经下载下来!')
            print('#----y:推送ID---n:全部确认---f:读取文本ID---q:退出----#')
            com =input('输入确认模式↑:')
            if com.lower()=='q':
                print('已退出')
            else:
                if com.lower()=='y':
                    k = []
                    x = input('请输入黑烟ID(输入->(q or n) 完成输入!):')
                    while x.lower() not in ['q','n']:
                        k.append(str(x))
                        x = input('请继续输入黑烟ID:')

                if com.lower()=='f':
                    dirs = input('输入文本路径(默认./year-mon-day/config.txt):')
                    if dirs in [None,'']:
                        print('start')
                        k = []
                        with open('config.txt',encoding='utf-8',mode='r') as f:
                            k = f.read().split()
                ID =k #所有黑烟的id
                morn,noon,afnoon =[],[],[] # 上中下负样本路径
                try:
                    with open(path.join(currentPath,recordINFO),mode='r+') as f:
                        txt = f.readline()
                        while txt:
                            id_,name,site = txt.split('~')
                            name = name.replace(' ','')
                            if str(name[8:10]) in ['07','08','09','10']:
                                morn.append(path.join(currentPath,site,id_+'~'+name+'.mp4'))
                            elif str(name[8:10]) in ['11','12','13',]:
                                noon.append(path.join(currentPath,site,id_+'~'+name+'.mp4'))
                            else:
                                afnoon.append(path.join(currentPath,site,id_+'~'+name+'.mp4'))
                            
                            # 确认黑烟ID
                            if str(id_) not in ID:
                                SFET.opSmoke(site,id_)
                            else: #对应的黑烟ID处理(目前仅支持手动上传2018.11.21)
                                targitPsmoke= path.join(currentPath,begindate+'~smoke',site)
                                os.makedirs(targitPsmoke,exist_ok=True)
                                shutil.move(path.join(currentPath,site,str(id_)+'~'+name+'.mp4'),path.join(targitPsmoke,str(id_)+'~'+name+'.mp4'))
                            txt = f.readline()
                except Exception as e:
                    print(e)
                # 收集``上中下负样本
                
        if flag_fun.lower() =='v': #鉴赏
            SFET.authenticate(currentPath,begindate.replace('-',''))
    else:raise '错误的输入！'
        

        