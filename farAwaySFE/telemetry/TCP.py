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

    def __init__(self,loginurl: str,Paramer :dict=None):
        '''出初始化参数'''
        self.__COOKIES = None
        self.loginurl = loginurl
        self._loginurl= loginurl[:loginurl.rindex('/')+1]+'json:auditor@'+\
                        loginurl[loginurl.rindex('/')+1:]+'/api/login'
        if Paramer:
            self._paramer = Paramer
        else:
            self._paramer = self.__Paramer

    def getInfo(self,url,isStream: bool=False):
        assert isinstance(url,str)
        try:
            # print('url:',url)
            if isStream:
                res = requests.get(url,stream=True,cookies=self._cookie)
            else:
                res = requests.get(url,cookies=self._cookie)
        except:
            traceback.print_exc()
            # return None
        if res.status_code !=200: print(res,url)
        return res

    #下载数据资源
    def download(self,url,paths):
        '''
        paths str:..../xx/xx.xx
        url  str:域名或IP
        '''
        [dir_name,dir_basename] = path.split(paths)
        if not path.exists(dir_name):os.makedirs(dir_name)
        
        #开始下载
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
            res = self.getInfo(url,True)


    @property
    def _cookie(self):
        return self.__getCookies(self._loginurl,self._paramer)

    def __getCookies(self,loginURL,Paramer):
        '''获取cookies'''

        if self.__COOKIES:
            return self.__COOKIES
        else:
            r = requests.post(loginURL,json=Paramer,timeout=8)
            result = r.headers['Set-Cookie'].split(';')[0].split('=')
            return{result[0]:result[1]}
    