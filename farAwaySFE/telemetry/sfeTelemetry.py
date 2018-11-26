from .__init__ import *

from .TCP import TCP


Chunk_Size =1024 #字节数

class SFETelemerty(TCP):
    
    def __init__(self,loginurl: str,Paramer :dict):
        super().__init__(loginurl,Paramer)
        with open('config.json',encoding='utf-8') as f:
            alls = json.load(f)
            self._configs = alls
            self._TSNO = alls['telemetryEquipment'] #prefix = device
            self._TSNO_= dict(zip(self._TSNO.values(),self._TSNO.keys()))
    #操作黑烟
    def opSmoke(self,site,recordID,flag: str):
        '''@paramer `` flag∈['status','upload']``` '''

        targitURL = str(self._configs['publicURL'][flag]['url'])
        targitURL.replace('site',site)
        targitURL.replace('record_id',recordID)
        self.getInfo(targitURL)

    @property
    def sitesID(self):



if __name__ == '__main__':
    #inistanse
    with open('config.json',encoding='utf-8') as f:
        alls = json.load(f)
    paramer ={ 
        'password':'5313232ef0a55311cf31e00b97afa15c',
        'user':'auditor'
    }


    #--start--#
        #urlPrefix: 网址前缀
    print('\t请选择区域!')
    flag_site = input('#----1:清远,2:新乡----#')
    if flag_site=='1':
        urlPrefix = alls['sitePosition']['qingyuan'] 
        SFET = SFETelemerty(+,paramer)
    elif flag_site=='2':
        urlPrefix = alls['sitePosition']['xinxiang'] 
        SFET = SFETelemerty(alls['sitePosition']['xinxiang']+,paramer)
    else:raise '错误的输入！'

    flag_fun = input('#---q:退出---d:下载---c:确认---v:查看图片#:')
    if flag_fun.lower() in ['d','q','d','v']:
        if flag_fun.lower() == 'd':


    else:raise '错误的输入！'
        

        