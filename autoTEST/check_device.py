import requests
from selenium import webdriver
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
    {'河南-金橞大道':'http://218.29.47.202:11000/'}
]
sichuans=[ #----四川----#
        {'四川-01':'http://182.150.48.217:11000/'},
        {'四川-02':'http://182.150.48.218:11000/'},
        {'四川-03':'http://182.150.48.220:11000/'},
        {'四川-04':'http://110.185.174.145:11000/'}
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
            res = requests.get(url,params={},headers={'Authorization':'bearer  '+token},timeout=3)
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
        res = requests.get(url,params={},headers={'Authorization':'bearer  '+token},timeout=3)
        return res
js_pwd ={
    'account':'operator',
    'password':'123456'
    }
global token,paramer
token = \
        'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJyb2xlIjoic2ZlIiwidW5pcXVlX25hbWUiOiJvcGVyYXRvciIsInVzZXJfaWQiOiIzNiIsImlzcyI6InJlc3RhcGl1c2VyIiwiYXVkIjoiMDk4ZjZiY2Q0NjIxZDM3M2NhZGU0ZTgzMjYyN2I0ZjYiLCJleHAiOjE1MzU1MDkwNzAsIm5iZiI6MTUzNDIxMzA3MH0.GMJej2Kr70U2ShsdM9qYk_potZ1uvvbirt4qadDPP1g'
def get_token():
    url_login = 'http://110.185.174.145:11000'
    res = requests.post(url_login,json=js_pwd)
    print(res)
    token = res.json()['content']['token']
    return token
def is_max(url):
    red,purple=None,None
    try:
        res = requests.get(url,params={},headers={'Authorization':'bearer  '+token},timeout=3)
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
if __name__=='__main__':

    # r_m,v_m = 0,0

    alls = []
    ps = 'api/light_source_settings/lightStrength/?t=0.1571323848346986?'
    alls.append(lanzs),alls.append(sichuans),alls.append(henans)
    for it in alls:
        for i in it:
            url = list(i.values())[0]
            print('url:',url)
            r_m,v_m,is_ok= 0,0,False
            for t in range(50):
                time.sleep(0.1)
                red,uv,is_ok= is_max(url+ps)
                if not is_ok:break
                if red>r_m:r_m=red
                if uv >v_m:v_m=uv
            if(is_ok):
                if (r_m>=500 and v_m>=2000):
                    with open('./检测报告.txt',encoding='utf-8',mode='a') as ff:
                        ff.writelines(list(i.keys())[0]+'  正常')
                        ff.writelines('\n')
                else:
                    with open('./检测报告.txt',encoding='utf-8',mode='a') as ff:
                        ff.writelines(list(i.keys())[0]+'  红外功率:'+'光强:'+str(int(r_m))+' 紫外积分:'+'光强:'+str(int(v_m)))
                        ff.writelines('\n')
            else:
                with open('./检测报告.txt',encoding='utf-8',mode='a') as ff:
                    ff.writelines(list(i.keys())[0]+',页面无法打开')
                    ff.writelines('\n')

        # print (r_m,v_m)

    # # print (res.headers)
    # # # r = res.json()
    # D = Devices('http://60.165.50.66:11000/lightSource.html')
    # res = D.req()
    # ps = 'api/light_source_settings/lightStrength/?t=0.1571323848346986?'
    # html = res.content
    # html_doc=str(html,'utf-8')
    # # print(a.encode('UTF-8').decode('UTF-8'))
    # print(html_doc)


    # html=BeautifulSoup(html_doc,'html.parser')
    # attrs=html.title.attrs
    # print(html.select('#infrared__column')[0].attrs)
    # print(attrs['class']) 