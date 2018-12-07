from __init__ import *
from TCP import TCP
from sfeTelemetry import SFETelemerty
class Device(SFETelemerty):
    """检测设备"""

#'json': {'clientId': '098f6bcd4621d373cade4e832627b4f6', 'userName': 'operator', 'password': '123456'}

    def __init__(self,loginurl: str,Paramer: dict):
        super().__init__(loginurl,Paramer)
        self._getToken()
    
    def _getToken(self):   
        js_pwd ={
            "clientId":"098f6bcd4621d373cade4e832627b4f6",
            'userName':'operator',
            'password':'123456'
        }
        loginurl = self.loginurl + '/api/login/'
        print('url:',loginurl)
        r = self.getInfo(loginurl,flag='post',json=js_pwd)
        print(r)
        r = requests.post(loginurl,json=js_pwd)
        self.token = json.loads(r.content)['content']['token']

    @property
    def getToken(self):
        return self.token

    def test(self):
        p_status ='api/light_source_settings/lightStatus/?t=0.38649866685018985?'
        res = self.getInfo('http://60.165.50.66:11000/'+p_status,headers={'Authorization':'bearer  '+self.getToken})
        print('res:',res)

def main():
    js_pwd ={
            "clientId":"098f6bcd4621d373cade4e832627b4f6",
            'userName':'operator',
            'password':'123456'
    }
    X = Device('http://60.165.50.66:11000',js_pwd)
    X.test()
if __name__ == '__main__':
    main()