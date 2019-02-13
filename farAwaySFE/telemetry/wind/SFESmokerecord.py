class SFETelemerty(TCP):


    def __init__(self,loginurl: str,Paramer: dict,PERMIT: bool=True):
        '''
            @ Paramer dict: 登陆账户密码
            @ loginurl str: 网址IP(域名)
            @ PERMIT  文件夹权限
        '''
        with open('SFETConfig.json',encoding='utf-8') as f:
            alls = json.load(f)
            self.configs = alls
        URLlogin = self.configs['publicURL']['login']['url']
        user = self.configs['account']['user'] # 用户名
        
        self.TSNO  = self.configs['telemetryEquipment'] #prefix = deviceNumber （english）
        self.TSNO_ = dict(zip(self.TSNO.values(),self.TSNO.keys()))
        # 存在登陆接口
        self.cookies_urllogin = loginurl[:loginurl.rindex('/')+1]+'json:'+user+'@'+\
                                loginurl[loginurl.rindex('/')+1:]+URLlogin
        # self.cookies_urllogin =None # 不存在登入接口

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
    """ paramer """

    # 获取设备站点的编号(id)
    @property
    def sites(self):
        """@return 站点id列表"""    
        targitURL = str(self.configs['publicURL']['website']['url'])
        targitURL = self.loginurl + targitURL
        res  = self.getInfo(targitURL)
        sites = [_ for _ in json.loads(res.content)['content']]
        return sites

    # 获取设备编号site 每条记录的集合(record_id)
    def per_site_lists(self,site):
        list_url = self.loginurl+str(self.configs['publicURL']['websiterecord']['url']).replace("{site}",site)
        _lists = json.loads(self.getInfo(list_url).content)['content']
        return _lists
    
    # 获取所有设备编号和对应记录集合 (id,record_id)
    def lists(self) -> list:
        _temp = []
        for _ in self.sites:
            _temp.append((_,self.per_site_lists(_)))
        return _temp
    
    def _download(self):
        