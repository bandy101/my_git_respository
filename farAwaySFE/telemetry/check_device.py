from __init__ import *
from TCP import TCP
from sfeTelemetry import SFETelemerty
class Device(SFETelemerty):
    """检测设备"""
#参数 http://61.178.104.30:11000
#/api/telemetry/telemetryResult/?t=0.4814316365376913?

#'json': {'clientId': '098f6bcd4621d373cade4e832627b4f6', 'userName': 'operator', 'password': '123456'}

    def __init__(self,loginurl: str,Paramer: dict,flag: bool=True):
        super().__init__(loginurl,Paramer,flag)
        self._Token()
        self.config = '../basicDaily/siteConfig.json'
        self.redSource, self.purpleSource, self.speed= 0, 0, []
        self.redStrength, self.purpleStrength = 0, 0

    def _Token(self):
        js_pwd ={
            "clientId":"098f6bcd4621d373cade4e832627b4f6",
            'userName':'operator',
            'password':'123456'
        }
        print(self._loginurl)
        r = self.getInfo(self._loginurl,flag='post',json=js_pwd,timeout=6,verify=False)
        if r:
            self._token = json.loads(r.content)['content']['token']
        else:
            for _ in range(4):
                r = self.getInfo(self._loginurl,flag='post',json=js_pwd,timeout=6,verify=False)
                if r:
                    self._token = json.loads(r.content)['content']['token']
                    break
            else:
                self._token = None

    @property
    def Token(self):
        return self._token

    def test(self):
        prfix = 'http://60.165.50.66:11000/'
        p_data = '/api/telemetry/telemetryResult/?t=0.4814316365376913?'
        ps = 'api/light_source_settings/lightStrength/?t=0.1571323848346986?'
        p_status ='api/light_source_settings/lightStatus/?t=0.58649866685018985?'
        res = self.getInfo('http://60.165.50.66:11000/'+p_status,headers={'Authorization':'bearer  '+self._token},verify= False,timeout=6)
        ress = self.getInfo(prfix+p_data,headers={'Authorization':'bearer  '+self._token},verify= False,timeout=6)
        print(json.loads(ress.content)['content']['velocity'])
    
    @property
    def getLightStrength(self,nums: int=20):
        """
        @return (coStrength,refStrength,uvStrength,greenStrength)
        """
        ps = '/api/light_source_settings/lightStrength/?t=0.1571323848346986?'
        _index = 0
        for _ in range(nums):
            res = self.getInfo(self.loginurl+ps,headers={'Authorization':'bearer  '+self._token},verify= False,timeout=6)
            if res:
                _index +=1
                r = json.loads(res.content)['content']
                # return (r['coStrength'],r['refStrength'],r['uvStrength'],r['greenStrength'])
                self.redStrength, self.purpleStrength = int(max(self.redStrength,r['coStrength'])),\
                                                        int(max(self.purpleStrength,r['uvStrength']))
                if all([self.redStrength+100>500, self.purpleStrength+100>2000]):
                    break
        if _index:
            return True
        else:return False

    @property
    def getLightSource(self,nums=6):
        """
        @return (redSource,purpleSource)
        """
        p_status ='/api/light_source_settings/lightStatus/?t=0.58649866685018985?'
        for _ in range(nums):
            res = self.getInfo(self.loginurl+p_status,headers={'Authorization':'bearer  '+self._token},verify= False,timeout=6)
            if res:
                r = json.loads(res.content)['content']
                self.redSource, self.purpleSource = max(self.redSource,r['irIntenPower']),\
                                        max(self.purpleSource,r['uvIntenIntegral'])
                return True
                break                                                        
        else:return False
    
    @property
    def getSpeed(self,nums: int=20):
        _index = 0
        p_data = '/api/telemetry/telemetryResult/?t=0.4814316365376913?'
        for _ in range(nums):
            res = self.getInfo(self.loginurl+p_data,headers={'Authorization':'bearer  '+self._token},verify= False,timeout=6)
            if res:
                try:
                    r = json.loads(res.content)['content']['velocity']
                except:
                    return True
                self.speed.append(r)
        if any(self.speed):
            return True
        return False

def main():
    with open('./巡检记录.txt',encoding='utf-8',mode='a') as ff:
        ff.writelines(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())+'\n')
        # strs+=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())+'<br>'

    siteSet = None
    with open('siteConfig.json',encoding='utf-8') as f:
        alls = json.load(f)
        siteSet = alls['citySet']

    startTime = time.time() #开始时间

    for place in siteSet: 

        print(list(place.values())[-1])
        PsiteName = list(list(place.values())[-1][-1].keys())[-1][:\
                    list(list(place.values())[-1][-1].keys())[-1].index('-')]
        _index = len(list(place.values())[-1]) # 记录站点异常数量
        for _place in list(place.values())[-1]:
            Pname = list(_place.keys())[-1]
            url = list(_place.values())[-1] # 获取每个点的地址
            X = Device(url,None,flag=True)# 
            if X.Token: #
                if all([X.getLightSource,X.getLightStrength]):
                    if any([X.redStrength+100<500,X.purpleStrength+100<2000]):# 异常
                        with open('巡检记录.txt',encoding='utf-8',mode='a') as f:
                            _speed = '' if X.getSpeed else '无速度'
                            _temp = f"{Pname} 红外功率: {X.redSource} 光强: {str(X.redStrength)} 紫外积分: {X.purpleSource} 光强: {str(X.purpleStrength)} {_speed}\n"
                            f.write(_temp)
                    else:
                        _index = _index - 1
                # 页面无法打开    
                else:
                    with open('巡检记录.txt',encoding='utf-8',mode='a') as f:
                        f.write(Pname+' 页面无法打开\n')
            # 页面无法打开
            else:
                with open('巡检记录.txt',encoding='utf-8',mode='a') as f:
                    f.write(Pname+' 页面无法打开\n')
            del X
        if not _index:
            with open('巡检记录.txt',encoding='utf-8',mode='a') as f:
                f.write(PsiteName+' 正常\n')
        with open('./巡检记录.txt',encoding='utf-8',mode='a') as ff:
            ff.write('\n')
    endTime = time.time() #结束时间
    _str = f'历时 {int(endTime - startTime)//60} 分钟  {int(endTime - startTime)-int(endTime - startTime)//60*60} 秒'
    with open('巡检记录.txt',encoding='utf-8',mode='a') as f:
        f.write(_str+'\n')

    
    
    
            
            


if __name__ == '__main__':
    X = Device('http://60.165.50.66:11000/',None,True)
    # X.test()
    main()