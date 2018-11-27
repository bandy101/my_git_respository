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
            self._SITES = None #站点集合 
    
    #操作黑烟
    def opSmoke(self,site,recordID,flag: str):
        '''@paramer `` flag∈['status','upload']``` '''

        targitURL = str(self._configs['publicURL'][flag]['url'])
        targitURL.replace('site',site)
        targitURL.replace('record_id',recordID)
        self.getInfo(targitURL)

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
    pool = ThreadPoolExecutor(max_workers=8) #线程池初始化
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
     
    #当前文件夹:
    currentPath = path.join(paths,str(begindate))
    if not path.exists(currentPath): os.makedirs(currentPath)
    
    #```flag_fun 功能标识
    flag_fun = input('#---q:退出---d:下载---c:确认---v:查看图片#:')
    if flag_fun.lower() in ['d','q','d','v']:
        if flag_fun.lower() == 'd': #下载
            sites = SFET.sitesID
            video_url = alls['publicURL']['video']['url']    
            image1_url = alls['publicURL']['image1']['url']
            image2_url = alls['publicURL']['image2']['url']
            
            targit_urls= []
            targit_paths = []
            for site in sites:
                downloadPath = path.join(currentPath,SFET.TSNO[site]) #下载的文件夹
                if not path.exists(downloadPath): os.makedirs(downloadPath)
                # 获取站点记录列表
                list_url = urlPrefix+str(alls['publicURL']['websiterecord']['url']).replace('site_id',site)
                lists =SFET.getInfo(list_url)
                for list_ in lists:
                    print(list_)
                    print(list_['upload'].encode().decode('unicode_escape'))
                    if all([list_['status'] in [False],list_['upload'].encode().decode('unicode_escape')\
                    in ['未上传']]):
                        video_url_ = video_url.replace('record_id',str(list_['id'])).replace('site',site)
                        image1_url_ = image1_url.replace('record_id',str(list_['id'])).replace('site',site)
                        image2_url_ = image2_url.replace('record_id',str(list_['id'])).replace('site',site)
                        targit_urls.extend((video_url_,image1_url_,image1_url_))
                        
                        targit_path_video  = path.join(currentPath,SFET.TSNO_[site])
                        targit_path_image1 = path.join(currentPath,SFET.TSNO_[site],'image1')
                        targit_path_image2 = path.join(currentPath,SFET.TSNO_[site],'image2')
                        targit_paths.extend((targit_path_video,targit_path_image1,targit_path_image2))
                        with open(path.join(currentPath,'temp_timeId.txt'),mode='a') as tempF:
                            tempF.write(str(list_['id']))
                            tempF.write(list_['name']),tempF.write(str(SFET.TSNO[site]))
                            tempF.write('\n')
                #线程池下载
                    #单个站点下载
                all_task = [pool.submit(SFET.download,url,path_) for url,path_ in zip(targit_urls,targit_paths)]
                    
    else:raise '错误的输入！'
        

        