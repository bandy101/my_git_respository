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
        '''出初始化参数
        '''
        self.__COOKIES = None
        self.loginurl = loginurl # 网站首地址
        self.cookies_urllogin =None # 登入接口

        if self.cookies_urllogin:
            self._cookie_ = self._cookie
        self.cookieOverdue = False


    @property
    def cookie(self):
        return self._cookie_ 

    def getInfo(self,url,flag: str='get',**arg):
        assert isinstance(url,str)
        RE ,res= None, None
        try:
            if 'get' in flag.lower():
                RE = requests.get
            if 'post' in flag.lower():
                RE = requests.post
            res = RE(url,**arg)
        except:
            traceback.print_exc()
            error = ''
            if res.status_code == 401 :
                self._cookie_ = self._cookie
            # cookie 是否过期
                if not self.cookieOverdue:
                    res = self.getInfo(url,cookies=self.cookie,**arg)
            elif res.status_code !=200:
                error = f' --读取的地址返回异常!,{flag},{res},{url}'
                print(error)
                res = None
            else:
                for _ in ['success','errcode']:
                    if _ in json.loads(res.content).keys():
                        if _ in json.loads(res.content)[_]:
                            break
                else:
                    error = f' --数据流返回异常!,{flag},{res},{url}'
                    res = None
            if error:
                with open('log.txt',mode='a') as f:
                    f.write(error+'\n')
        return res

    #下载数据资源
    def download(self,url,paths):
        '''
        paths str:..../xx/xx.xx
        url  str:域名或IP
        '''
        [dir_name,dir_basename] = path.split(paths)
        if not path.exists(dir_name):os.makedirs(dir_name)

        res = self.getInfo(url,cookies = self.cookie,stream=True)
        while res:
            content_length = int (res.headers['content-length']) # 数据长度
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
                r = self.getInfo(loginURL,flag='post',json=Paramer,timeout=6,verify=False)
                result = r.headers['Set-Cookie'].split(';')[0].split('=')
                self.cookieOverdue = True
            except:
                with open('log.txt',mode='a') as f:
                    f.write('cookies获取错误 '+traceback.format_exc()+'\n')
                traceback.print_exc()
                return None
            return {result[0]:result[1]}
    