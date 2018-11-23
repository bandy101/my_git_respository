import requests
from bs4 import BeautifulSoup
import json
import time
global lanzs,henans,sichuans
lanzs=[ #----兰州----#
    {'兰州-南出口':'http://60.165.50.66:11000/'},
    {'兰州-和平点':'http://61.178.104.30:11000/'},
    {'兰州-大沙坪':'http://61.178.58.121:11000/'},
    {'兰州-天水路':'http://61.178.20.71:11000/'},
    {'兰州-岸门口':'http://61.178.114.101:11000/'},
    {'兰州-黄羊头':'http://61.178.12.58:11000/'}
]
henans=[ #----河南----#
    {'河南-金穗大道':'http://218.29.47.202:11000/'}
]
hbxx=[#-----鹤壁----#
    {'鹤壁-刘庄超限站1号机':'http://221.176.241.91:11001/'},
    {'鹤壁-刘庄超限站2号机':'http://221.176.241.91:11002/'},
    {'鹤壁-S305省道1号机':'http://120.194.140.174:11001/'},
    {'鹤壁-S305省道2号机':'http://120.194.140.174:11002/'},
    {'鹤壁-G107国道1号机':'http://120.194.138.243:11001/'},
    {'鹤壁-G107国道2号机':'http://120.194.138.243:11002/'},
    {'鹤壁-东海路1号机':'http://120.194.139.137:11001/'},
    {'鹤壁-东海路2号机':'http://120.194.139.137:11002/'}
    
    
]
sichuans=[ #----四川----#
        {'四川-01':'http://182.150.48.217:11000/'},
        {'四川-02':'http://182.150.48.218:11000/'},
        {'四川-03':'http://182.150.48.220:11000/'},
        {'四川-04':'http://110.185.174.145:11000/'}
]

guangzhous=[ #----广州----#
        {'广州-东华南路':'http://14.23.53.82:35032/'},
        {'广州-人民路':'http://14.23.122.74:33551/'},
        {'广州-八旗二马路':'http://14.23.88.106:10646/'},
        {'广州-寺右新马路':'http://183.6.186.242:12209/'},
        {'广州-水荫二横路':'http://183.6.130.130:20909/'},
        {'广州-环市东路(动物园东往西)':'http://14.23.71.18:11955/'},
        {'广州-环市东路(动物园西往东)':'http://61.140.17.210:44886/'},
        {'广州-解放北路(大北立交)':'http://14.23.86.10:26270/'},
        {'广州-陵园西路(由南向北方向)':'http://14.23.93.18:15291/'}
]
qingyuans=[#----清远----#
        {'清远-三颗竹(源潭)':'http://202.105.10.86:11000/'},
        {'清远-广清大道(龙潭)':'http://202.105.10.78:11000/'},
        {'清远-治超出口':'http://119.135.185.238:11000/'},
        {'清远-清远大道(党校)':'http://202.105.10.18:11000/'}
]
class Devices:
    '''
        检测设备
    '''

    def __init__(self,d_url):
        self.url = d_url
        self.red =None
        self.infrared_num=50
    
    def req(self,**paramer):
        res = requests.get(self.url,paramer)
        return res

    def is_max(self,url):
        red,purple=None,None
        try:
            res = requests.get(url,params={},headers={'Authorization':'bearer  '+token},timeout=6)
            vs = res.content
            vs = str(vs,'utf-8')
            vs = json.loads(vs)
            # print('vs:',vs)
            red = vs['content']['coStrength']
            purple = vs['content']['uvStrength']
            k = True
        except :
            k = False
        return red,purple,k
    def res_content(self,url):
        res = requests.get(url,params={},headers={'Authorization':'bearer  '+token},timeout=6)
        return res
js_pwd ={
    'account':'operator',
    'password':'123456'
    }
global paramer
#bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJyb2xlIjoic2ZlIiwidW5pcXVlX25hbWUiOiJvcGVyYXRvciIsInVzZXJfaWQiOiIzNiIsImlzcyI6InJlc3RhcGl1c2VyIiwiYXVkIjoiMDk4ZjZiY2Q0NjIxZDM3M2NhZGU0ZTgzMjYyN2I0ZjYiLCJleHAiOjE1MzY4MTc2OTAsIm5iZiI6MTUzNTUyMTY5MH0.kbzKl_HfFu331acmNWJBK4F2WnKG4vbKBm8z-R3jgBg

def get_token(url):
    js_pwd ={
    "clientId":"098f6bcd4621d373cade4e832627b4f6",
    'userName':'operator',
    'password':'123456'
    }
    token,k=None,None
    try:
        res = requests.post(url,json=js_pwd,verify=False,timeout=5)
        res =json.loads(res.content)
        token = res['content']['token']
        k =True
        print('token',token)
    except:
        k ,token=False,None
        print('token',token)
    return token,k
    
def is_max(url,token):
    red,purple=None,None
    try:
        res = requests.get(url,params={},headers={'Authorization':'bearer  '+token},timeout=6,verify= False)
        vs = res.content
        vs = str(vs,'utf-8')
        vs = json.loads(vs)
        # print('vs:',vs)
        red = vs['content']['coStrength']
        purple = vs['content']['uvStrength']
        k = True
    except :
        k = False
    return red,purple,k
def get_strength(url,token):
    red,purple=None,None
    try:
        res = requests.get(url,params={},headers={'Authorization':'bearer  '+token},timeout=6,verify= False)
        vs = res.content
        vs = str(vs,'utf-8')
        vs = json.loads(vs)
        # print('vs:',vs)
        red = vs['content']['irIntenPower']
        purple = vs['content']['uvIntenIntegral']
        k = True
    except :
        k = False
    return red,purple,k


def check_(times=200):
    alls = []
    ps = 'api/light_source_settings/lightStrength/?t=0.1571323848346986?'
    p_status ='api/light_source_settings/lightStatus/?t=0.38649866685018985?'
    alls.append(hbxx),alls.append(lanzs),alls.append(sichuans),alls.append(henans),alls.append(guangzhous),alls.append(qingyuans)
    # alls.append(lanzs),,alls.append(guangzhous),alls.append(qingyuans)
    strs =''
    with open('./检测报告.txt',encoding='utf-8',mode='a') as ff:
        ff.writelines(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()))
        strs+=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())+'<br>'
    for it in alls:
        with open('./检测报告.txt',encoding='utf-8',mode='a') as ff:
            ff.writelines('\n')
            strs +='\n'
        ok_num =0   
        print('start****')
        for i in it:
            print(i)
            url = list(i.values())[0]
            print(url)
            token ,is_oppage= get_token(url+'api/login/')
            print('is_oppage',is_oppage)
            nn =0
            while not is_oppage:
                print('is_oppage',is_oppage)
                nn +=1
                if nn>5:break
                token,is_oppage= get_token(url+'api/login/')##令牌
            print('url:',url)
            r_m,v_m,is_ok= 0,0,False
            red_power,uv_power,is_p=get_strength(url+p_status,token)
            is_open =False
            for t in range(times):
                if is_p:
                    time.sleep(0.05)
                    red,uv,is_ok= is_max(url+ps,token)
                    if is_ok:is_open =True
                    if not is_ok:continue
                    if red>r_m:r_m=red
                    if uv >v_m:v_m=uv
            if(is_open):
                if (r_m>=500 and v_m>=2000):
                    ok_num +=1
                else:
                    with open('./检测报告.txt',encoding='utf-8',mode='a') as ff:
                        ff.writelines(list(i.keys())[0]+'  红外功率:'+str(red_power)+' 光强:'+str(int(r_m))+' 紫外积分:'+str(uv_power)+' 光强:'+str(int(v_m)))
                        strs +=list(i.keys())[0]+'  红外功率:'+str(red_power)+' 光强:'+str(int(r_m))+' 紫外积分:'+str(uv_power)+' 光强:'+str(int(v_m))+'\n<br>'
                        ff.writelines('\n')
            else:
                with open('./检测报告.txt',encoding='utf-8',mode='a') as ff:
                    ff.writelines(list(i.keys())[0]+',页面无法打开')
                    strs +=list(i.keys())[0]+',页面无法打开\n<br>'
                    ff.writelines('\n')
        if (ok_num==len(it)):
            with open('./检测报告.txt',encoding='utf-8',mode='a') as ff:
                ff.writelines(list(i.keys())[0][0:2]+'  正常')
                strs +=list(i.keys())[0][0:2]+'  正常\n<br>'
                ff.writelines('\n')
        else:
            if ok_num==0:
                pass
            else:
                with open('./检测报告.txt',encoding='utf-8',mode='a') as ff:
                    ff.writelines(list(i.keys())[0][:2]+',其他正常')
                    strs +=list(i.keys())[0][:2]+',其他正常\n<br>'
                    ff.writelines('\n')
    return strs
if __name__=='__main__':


    # # print (res.headers)
    # # # r = res.json()
    # D = Devices('http://60.165.50.66:11000/lightSource.html')
    # res = D.req()
    # ps = 'api/light_source_settings/lightStrength/?t=0.1571323848346986?'
    # html = res.content
    # html_doc=str(html,'utf-8')
    # # print(a.encode('UTF-8').decode('UTF-8'))
    # print(html_doc)
    print(check_(20))

    # html=BeautifulSoup(html_doc,'html.parser')
    # attrs=html.title.attrs
    # print(html.select('#infrared__column')[0].attrs)
    # print(attrs['class']) 

    # check_(10)
    # print(strs)