"""
date:
author: miachelzhuwb
"""
from __init__ import *

_TCP__COOKIES = None
class TCP:
    def __init__(self,url):
        self._url = url
    
    def __getInfo(self,url):
        assert isinstance(url,str)
        try:
            res = requests.get(url,cookies=self.cookie)
        except:
            traceback.print_exc()
            return None
        return res

    @property    
    def cookie(self):
        return self.__COOKIES