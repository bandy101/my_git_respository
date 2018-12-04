from __init__ import *

from TCP import TCP

Chunk_Size =1024 #字节数

class SFETelemerty(TCP):
    
    def __init__(self,loginurl: str,Paramer :dict):
        '''
            @ Paramer dict: 登陆账户密码
            @ loginurl str: 网址IP(域名)
        '''

        super().__init__(loginurl,Paramer)

        self.SITES = self.sitesID  # 站点名称
    
    # 操作黑烟
    def opSmoke(self,site,recordID,flag: str='status'):
        '''@paramer `` flag∈['status','upload']``` '''

        targitURL = str(self.configs['publicURL'][flag]['url'])
        targitURL = targitURL.replace(r'{site}',site)
        targitURL = targitURL.replace(r'{record_id}',recordID)
        self.getInfo(self.loginurl+targitURL)
        flag = 1
        if flag:
            print(self.loginurl+targitURL,'--确认成功')

    # 鉴赏黑烟
    def authenticate(self,currentPath: str,dirName: str,Names=['车辆误判','黑烟视频','非黑烟']):
        '''     '''
        SCALE = 0.8
        switch =True #鉴赏的开关 # ['o']
        currentDir =os.getcwd()
        sites = [_ for _ in os.listdir(currentPath) if path.isdir(path.join(currentPath,_)) and _.replace('-','')[:8] not  in [dirName]] # 通过文件夹名称获取站点对应名
        # 初始化开始文件夹
        for _ in Names:
            os.makedirs(path.join(currentPath,dirName,_),exist_ok=True)

        for site in sites:
            print('每个站点间隔50张图片显示一次当前图片地址:',site)

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
                        if not index%50:
                            print(path.join(_path,'image2',f[:-4]+'_2.jpg'))
                    except:
                        ''' #重新下载# 待完成'''    
                        traceback.print_exc()
                        with open('log.txt',mode='a') as fs:
                            fs.write(traceback.format_exc()+'\n'+path.join(_path,'image1',f[:-4])+'\n')
                        continue
                else:continue
                while(1):
                    try:
                        cv2.imshow('Image1',cv2.resize(im1,None,fx=SCALE,fy=SCALE))
                        cv2.imshow('Image2',cv2.resize(im2,None,fx=SCALE,fy=SCALE))

                    except:
                        traceback.print_exc()
                        with open('log.txt',mode='a') as fs:
                            fs.write(traceback.format_exc()+'\n'+'imshowError:'+path.join(_path,'image1',f[:-4])+'\n')
                        break
                    k=cv2.waitKey(1)&0xFF  
                    if k ==32:
                        break
                    if k in [ord('w'),ord('W')]:
                        #写入记录的操作#
                        #print('---写入成功---')
                        cv_imwrite(path.join(currentPath,dirName,'车辆误判',f[:-4]+'_1.jpg'),im1)
                        cv_imwrite(path.join(currentPath,dirName,'车辆误判',f[:-4]+'_2.jpg'),im2)
                        print('  --写入成功 ',f)
                    if k in [102,70]: # f  
                        os.chdir(path.abspath(path.join(currentPath,site)))
                        os.system("\""+f+"\"") #含有空格
                        os.chdir(currentDir) #回到基本路径防止相对路径错误
                    if k==111: #'o' 全部关闭
                        switch = False
                        cv2.destroyAllWindows()
                        break
                if not switch:break
        cv2.destroyAllWindows()

    # 获取设备编号(站点)
    @property
    def sitesID(self):
        targitURL = str(self.configs['publicURL']['website']['url'])
        targitURL = self.loginurl + targitURL
        res  = self.getInfo(targitURL)
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
        # '增加平台'
    print('\t请选择区域!')
    flag_site = input('#----1:清远,2:新乡----#:')
    if flag_site=='1':
        urlPrefix = str(alls['sitePosition']['qingyuan'])
        paths = './videoData_qingyuan' 
        platform = '清远平台'
    elif flag_site=='2':
        urlPrefix = str(alls['sitePosition']['xinxiang'])
        paths = './videoData_xinxiang' 
        platform = '新乡平台'

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
    recordINFO = str(begindate).replace('-','') + '_info.txt'

    #```flag_fun 功能标识
    flag_fun = input('#---q:退出---d:下载---c:确认----u:上传(暂无)---v:查看图片#:')
    startTime = time.time() #开始时间
    print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(startTime)))

    if flag_fun.lower() in ['d','q','d','v','c']: # 功能选择
        with open('log.txt',mode='a') as f:
            f.write(str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(startTime)))+'\n')
        if flag_fun.lower() == 'd': #下载
            print('----开始下载----')

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
                        for _ in ['\\','/','*','?','<','>','|',':',' ']:
                            if _ in name:
                                name = name.replace(_,'')
                        
                        targit_path_video  = downloadPath+'/'+str(list_['id'])+'~'+name+'.mp4'
                        targit_path_image1 = path.join(downloadPath,'image1')+'/'+str(list_['id'])+'~'+name+'_1.jpg'
                        targit_path_image2 = path.join(downloadPath,'image2')+'/'+str(list_['id'])+'~'+name+'_2.jpg'
                        targit_paths.extend((targit_path_video,targit_path_image1,targit_path_image2))
                        # print('targit_paths:',targit_paths)
                        # print('test:',video_url_,'path:',targit_path_video)

                        #记录下载信息(id~name~site)
                        with open(path.join(currentPath,recordINFO),mode='a') as tempF:#'~' 是分隔符
                            tempF.write(str(list_['id'])+'~')
                            tempF.write(name+'~'),tempF.write(str(SFET.TSNO[site]))
                            tempF.write('\n')
                #线程池下载
                    #单个站点下载
            all_task = [pool.submit(SFET.download,url,path_) for url,path_ in zip(targit_urls,targit_paths)]
            wait(all_task,return_when=ALL_COMPLETED)  # 当线程全部完成 开始下一步
            print('共下载 ',int(len(targit_urls))/3,' 视频')

        if flag_fun.lower() =='c': #确认
            '''
            通过 输入ID 比对recordINFO.split('separator')->[id,name,site]
            '''
        
            print('确认前需要确保各个站点的视频已经下载下来!')
            print('#----y:推送ID---f:读取文本ID---q:退出----#')
            com =input('输入确认模式↑:')
            if com.lower()=='q':
                print('    ---已退出')
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
                if com.lower() not in ['y','f']: raise '   错误的输入!'
                

                ID =k #所有黑烟的id
                SITE,morn,noon,afnoon =[],[],[],[] # 上中下负样本路径
                confirmNum =0 #确认总数
                _tempStr = ''
                try:
                    with open(path.join(currentPath,recordINFO),mode='r+') as f:
                        txt = f.readline()
                        print('正在确认···')
                        while txt:
                            id_,name,site = txt.split('~')
                            site = site.replace('\n','')
                            # name = name.replace(' ','') #后期可能添加的操作 2018.11.29

                            SITE.append(site)
                            if str(name[8:10]) in ['07','08','09','10']:
                                morn.append(path.join(currentPath,site,id_+'~'+name+'.mp4'))
                            elif str(name[8:10]) in ['11','12','13',]:
                                noon.append(path.join(currentPath,site,id_+'~'+name+'.mp4'))
                            else:
                                afnoon.append(path.join(currentPath,site,id_+'~'+name+'.mp4'))
                            
                            # 确认黑烟ID flag: 测试功能开关
                            flag = 1
                            if flag:
                                if str(id_) not in ID:
                                    SFET.opSmoke(SFET.TSNO_[site],id_)
                                    confirmNum = confirmNum+1
                                else: #对应的黑烟ID处理(目前仅支持手动上传2018.11.21)
                                    print('txt:',txt)
                                    _tempStr =_tempStr + (str(txt)+'\n')
                                    targitPsmoke= path.join(currentPath,begindate+'~smoke',site)
                                    os.makedirs(targitPsmoke,exist_ok=True)
                                    shutil.move(path.join(currentPath,site,str(id_)+'~'+name+'.mp4'),path.join(targitPsmoke,str(id_)+'~'+name+'.mp4'))
                            txt = f.readline()
                except Exception as e:
                    print(e)
                    traceback.print_exc()
                    with open('log.txt',mode='a') as f:
                        f.write(repr(e)+'\n')
                print('确认总数:',confirmNum,'下载总数:',len(SITE))
                print('待手动上传:',_tempStr)
                SITE = set(SITE)
                gatherMorn ,gatherNoon ,gatherAfnoon= {}, {}, {}

                for _ in SITE:
                    _ = {_:[]}
                    gatherMorn.update(_)
                    gatherNoon.update(_)
                    gatherAfnoon.update(_)
                           
        # 收集``各站点上中下负样本 各一个
                plat = begindate.replace('-','')+' '+platform   #保存格式
                #非黑烟收集目录
                noSmokePath = path.join(currentPath,begindate.replace('-',''),'非黑烟',plat)
                os.makedirs(noSmokePath,exist_ok=True)
                
                for site in SITE:
                    for m in morn:
                        if site in m: gatherMorn[site].append(m)
                    for n in noon:
                        if site in n: gatherNoon[site].append(n)
                    for a in afnoon:
                        if site in a: gatherAfnoon[site].append(a)
                    print(site,'~非黑烟数:',int(len(gatherMorn[site]+gatherNoon[site]+gatherAfnoon[site]))/3)
                #`` 收集
                for key in SITE:
                    index_ = 0
                    strengthM ,strengthN ,strengthA= len(gatherMorn),len(gatherNoon),len(gatherAfnoon)
                    PM = str(gatherMorn[key][int(random.uniform(0,strengthM))])
                    PN = str(gatherNoon[key][int(random.uniform(0,strengthN))])
                    PA = str(gatherAfnoon[key][int(random.uniform(0,strengthA))])


                    # print('###',f'{str(path.basename(PM)).split('~')}')
                    PMName = path.basename(PM).split('~')[-1][:8] + f'_{key}_{index_:02}.mp4'
                    index_ =index_ +1
                    PNName = path.basename(PN).split('~')[-1][:8] + f'_{key}_{index_:02}.mp4'
                    index_ =index_ +1
                    PAName = path.basename(PA).split('~')[-1][:8] + f'_{key}_{index_:02}.mp4'
                    index_ =index_ +1
                    try:
                        shutil.copy(PM,path.join(noSmokePath,PMName))
                        shutil.copy(PN,path.join(noSmokePath,PNName))
                        shutil.copy(PA,path.join(noSmokePath,PAName))
                    except Exception as e:
                        # print('pm:',PM)
                        # print('pn:',PN)
                        # print('pa:',PA)
                        with open('log.txt',mode='a') as f:
                            f.write(repr(e)+'\n')

        # 将保存的黑烟移入 对应文件夹Dirname  YearMonDay
                _temp = begindate.replace('-','')
                Dirname = path.join(currentPath,begindate+'~smoke')
                targitP = path.join(currentPath,begindate.replace('-',''),'黑烟视频',begindate.replace('-','')+' '+platform)
                os.makedirs(targitP,exist_ok=True)
                if path.exists(Dirname):
                    for p,d,f in os.walk(Dirname):
                        index_ = 0
                        for _ in f:
                            shutil.copy(path.join(p,_),path.join(targitP,f'{_temp}_{path.basename(p)}_{index_:02}.mp4'))
                            index_ = index_ + 1
                print('    --操作完成')
        
        # ohter
        if flag_fun.lower() =='v': #鉴赏
            print('w:将误判的车辆(小轿车)写入对应的文件夹,具体查看``word-线上黑烟记录模板\n\
            f:查看当前图片对应的视频,确定是黑烟后,将视频文件名称进行截图(后续的``确认``操作需要用到)')
            SFET.authenticate(currentPath,begindate.replace('-',''))
        if flag_fun.lower() in ['q']: print('   --已退出')
    else:
        raise '错误的输入！'
    endTime = time.time() #结束时间
    print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(endTime)))
    
    print('历时 ',int(endTime - startTime)//60,' 分钟 ',\
            int(endTime - startTime)-int(endTime - startTime)//60*60,' 秒')
    if flag_fun.lower() not in ['d']:
        input('输入任意键退出!')
        

        