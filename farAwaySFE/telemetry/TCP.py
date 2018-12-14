"""
date:
author: miachelwbzhu
"""
from __init__ import *


Chunk_Size =1024 #字节数
_TCP__COOKIES = None  #format{cookiesID:Value}
_TCP__Paramer =None
class TCP:
    """创建对应的TCP连接"""

    def __init__(self,loginurl: str,Paramer :dict=None,flag: bool=False):
        '''出初始化参数
        flag bool:True 对应查询光强,否则其他
        '''
        

        if Paramer:
            self._paramer = Paramer
        else:
            # self._paramer = self.__Paramer
            self._paramer = None

        with open('SFETConfig.json',encoding='utf-8') as f:
            alls = json.load(f)
            self.configs = alls
        user = self.configs['account']['user']
        URLlogin = self.configs['publicURL']['login']['url']


        self.TSNO  = self.configs['telemetryEquipment'] #prefix = deviceNumber
        self.TSNO_ = dict(zip(self.TSNO.values(),self.TSNO.keys()))
        self.__COOKIES = None
        self.loginurl = loginurl
        if not flag:
            self._loginurl = loginurl[:loginurl.rindex('/')+1]+'json:'+user+'@'+\
                            loginurl[loginurl.rindex('/')+1:]+URLlogin
        else:
            self._loginurl = loginurl + URLlogin[1:] + '/'

        print(self._loginurl)
        self._cookie_ = self._cookie

    @property
    def cookie(self):
        return self._cookie_ 

    def getInfo(self,url, isStream: bool=False,flag: str='get',**arg):
        assert isinstance(url,str)
        RE ,res= None, None
        try:
            if 'get' in flag.lower():
                RE = requests.get
            if 'post' in flag.lower():
                RE = requests.post
            if isStream:
                res = RE(url,stream=True,cookies=self.cookie,**arg)
            else:
                res = RE(url,cookies=self.cookie,**arg)
        except:
            traceback.print_exc()
            return None

        try:
            if res.status_code !=200 : 
                print(f' --异常!,{flag},{res},{url}')
                return None
            elif not isStream:
                try:
                    if not json.loads(res.content)['success']:
                        print(f' --异常!,{flag},{res},{url}')
                        return None
                except:
                    try:
                        if json.loads(res.content)['errcode']:
                            print(f' --异常!,{flag},{res},{url}')
                            return None
                    except:
                        traceback.print_exc()
                        return None
            else: 
                pass
        except Exception as e:
            traceback.print_exc()
            with open('log.txt',mode='a') as f:
                f.write(repr(e)+'\n')
            print('flag:',flag,'error!:',res,url)
            return None
        return res

    #下载数据资源
    def download(self,url,paths):
        '''
        paths str:..../xx/xx.xx
        url  str:域名或IP
        '''
        [dir_name,dir_basename] = path.split(paths)
        if not path.exists(dir_name):os.makedirs(dir_name)

        res = self.getInfo(url,True)
        while res:
            content_length = int (res.headers['content-length'])
            if path.exists(paths):
                if path.getsize(paths)==content_length:
                    print(res,res.url,'already exists!')
                    break
                else:os.remove(paths)
            try:
                with open(paths,'ab') as f:
                    for _ in res.iter_content(chunk_size=Chunk_Size*Chunk_Size):
                        if _:f.write(_),f.flush()
                    print('download sucessly,receive data,file size : %d  total size:%d' % (os.path.getsize(paths), content_length))
                    if path.getsize(paths) ==content_length:
                        break
            except:
                traceback.print_exc()
                with open('log.txt',mode='a') as f:
                    f.write(traceback.format_exc()+'\n')
            res = self.getInfo(url,True)


    @property
    def _cookie(self):
        return self.__getCookies(self._loginurl,self._paramer)

    def __getCookies(self,loginURL,Paramer):
        '''获取cookies'''

        if self.__COOKIES:
            return self.__COOKIES
        else:
            try:
                r = requests.post(loginURL,json=Paramer,timeout=6,verify=False)
                result = r.headers['Set-Cookie'].split(';')[0].split('=')
            except:
                traceback.print_exc()
                return None
            return {result[0]:result[1]}
    