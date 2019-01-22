class SFETelemerty(TCP):
    

    def __init__(self,loginurl: str,Paramer: dict,PERMIT = 0):
        '''
            @ Paramer dict: 登陆账户密码
            @ loginurl str: 网址IP(域名)
        '''
        with open('SFETConfig.json',encoding='utf-8') as f:
            alls = json.load(f)
            self.configs = alls
        URLlogin = self.configs['publicURL']['login']['url']
        user = self.configs['account']['user'] # 用户名
        
        self.TSNO  = self.configs['telemetryEquipment'] #prefix = deviceNumber （english）
        self.TSNO_ = dict(zip(self.TSNO.values(),self.TSNO.keys()))
        self.cookies_urllogin = loginurl[:loginurl.rindex('/')+1]+'json:'+user+'@'+\
                            loginurl[loginurl.rindex('/')+1:]+URLlogin

        super().__init__(loginurl,Paramer)

        self.PERMIT =PERMIT

        # self.SITES = self.sitesID  # 站点名称
    
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
    def authenticate(self,currentPath: str,dirName: str,begindate,platsubfix: str=None):
        '''     '''
        savePath = r'\\192.168.20.21/AIMaterials/每日素材-未入库/车辆误判/'+_T+'/'+'车辆误判'+carErrorsufix
        local_savePath = path.join(currentPath,begindate.replace('-',''),'车辆误判'+carErrorsufix)


        if self.PERMIT:
            os.makedirs(savePath,exist_ok=True)
        os.makedirs(local_savePath,exist_ok=True)

        SCALE = 0.8     # 图片缩放比例
        switch =True #鉴赏的开关 # ['o']
        currentDir =os.getcwd()
        sites = [_ for _ in os.listdir(currentPath) if path.isdir(path.join(currentPath,_)) and _.replace('-','')[:8] not  in [dirName]] # 通过文件夹名称获取站点对应名

        for site in sites:
            print('每个站点间隔50张图片显示一次当前图片地址:',site)
            _path = path.join(currentPath,site)
            index = -1
            if not switch:
                break
            if not path.exists(path.join(_path,'image2')):continue
            for f in os.listdir(path.join(_path,'image2')):
                im1,im2 = None,None
                if f[-3:].lower() in ['mp4','avi','jpg','png']:
                    try:
                        f = f[:-2]
                        # im1 = cv_imread(path.join(_path,'image1',f[:-4]+'_1.jpg'))
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
                        # cv2.imshow('Image1',cv2.resize(im1,None,fx=SCALE,fy=SCALE))
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
                        # cv_imwrite(path.join(currentPath,dirName,'车辆误判',f[:-4]+'_1.jpg'),im1)
                        # cv_imwrite(path.join(currentPath,dirName,'车辆误判',f[:-4]+'_2.jpg'),im2)
                        # cv_imwrite(savePath,im1)
                        _T = begindate.replace('-','')[:-2]
                        _srcPath = path.join(_path,'image1',f[:-4]+'_1.jpg')

                        
                        try:
                            if PERMIT:
                                shutil.copy(_srcPath,savePath)
                            shutil.copy(_srcPath,local_savePath)
                            print('---写入成功--- ',f[:-4])
                        except:
                            traceback.print_exc()
                    if k in [102,70]: # f
                        _url = self.loginurl+'/api/record/'+self.TSNO_[site]+'/'+str(f.split('~')[0])+'/video'
                        print('url:',_url)
                        _p  = path.join(currentPath,site,f[:-4]+'.mp4')
                        self.download(_url,_p,stream=True,cookies=self.cookie)
                        os.chdir(path.abspath(path.join(currentPath,site)))
                        # os.system("\""+f+"\"") #含有空格
                        os.system("\""+f[:-4]+'.mp4'+"\"")
                        os.chdir(currentDir) #回到基本路径防止相对路径错误
                    if k==111: #'o' 全部关闭
                        switch = False
                        cv2.destroyAllWindows()
                        break
                if not switch:break
        cv2.destroyAllWindows()
