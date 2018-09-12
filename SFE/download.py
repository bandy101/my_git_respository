import requests
import os 
from os import path
import json,time
prex = 'http://202.105.10.126:8055/video/'
# url = 'http://202.105.10.126:8055/video/20180911/15366527703302.mp4'
# paths ='./video/2.mp4'
import zipfile,shutil

def dwd(paths,url):
    try:
        pre_content_length = 0
        while True:
            res = requests.get(url,stream=True)
            content_length = int(res.headers['content-length'])
            print(res.headers['content-length'])

            if content_length < pre_content_length or (
                os.path.exists(paths) and os.path.getsize(paths) == content_length):
                break
            pre_content_length = content_length
            with open(paths, 'ab') as file:
                file.write(res.content)
                file.flush()
                print('receive data，file size : %d  total size:%d' % (os.path.getsize(paths), content_length))
    except Exception as e:
        print(e)
def get_token(url,name='demo',pwd='demo&123'):
    try:
        js_pwd ={
            "clientId":"098f6bcd4621d373cade4e832627b4f6",
            'userName':name,
            'password':pwd
        }
        res = requests.post(url,json=js_pwd,verify=False)
        res =json.loads(res.content)
        token = res['content']['token']
        return token
    except Exception as e:
        print(e)

def get_mp4_info(url):
    url_qy = 'http://202.105.10.126:8055/api/v1/login/'
    begindate= time.strftime("%Y-%m-%d", time.localtime())+' 00:00:00'
    enddate = time.strftime("%Y-%m-%d", time.localtime())+' 23:59:59'
    params = {
        'provinceId':440000,
        'cityId':441800,
        'countyID':'',
        'tsNo':'',
        'monitorBeginTime':str(begindate),
        'monitorEndTime':str(enddate),
        'pageSize':1000,
        'pageNum':1
    }
    token = get_token(url_qy)
    res = requests.get(url,params=params,headers={'Authorization':'bearer  '\
        +token},timeout=6000,verify= False)
    print(res.url)
    res = json.loads(res.content)
    lists = res['content']['list']
    print(len(lists))
from os import path
def zips(startdir=None,file_news=None):
    startdir = "./video"  #要压缩的文件夹路径
    if path.exists(startdir):
        shutil.rmtree(startdir)
    os.makedirs(path.abspath(startdir))
    times = time.strftime('%Y-%m-%d',time.localtime())
    fpath = 'G:/分类任务/清远黑烟/清远平台/'+times
    file_news = fpath +'.zip' # 压缩后文件夹的名字
    print(file_news)
    z = zipfile.ZipFile(file_news,'w',zipfile.ZIP_DEFLATED) #参数一：文件夹名（路径）
    for dirpath, dirnames, filenames in os.walk(startdir):
        print('dirpath:',dirpath)
        for filename in filenames:
            z.write(path.join(dirpath,filename))
            print ('压缩成功,',path.join(dirpath,filename))
    z.close()

if __name__=='__main__':
    # dwd(paths)
    url_qy = 'http://202.105.10.126:8055/api/v1/login/'
    url = 'http://202.105.10.126:8055/api/v1/smokeMessagePageQuery'
    # get_mp4_info(url)
    zips()
