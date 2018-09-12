import requests
import os,shutil
from os import path
import json,time
import zipfile
prex = 'http://202.105.10.126:8055/video/'
# url = 'http://202.105.10.126:8055/video/20180911/15366527703302.mp4'
# paths ='./video/2.mp4'
from concurrent.futures import ThreadPoolExecutor,ALL_COMPLETED,wait

def dwd(paths,url):
    try:
        # pre_content_length = 0
        if not path.exists(path.split(paths)[0]):os.makedirs(path.split(paths)[0])
        while True:
            res = requests.get(url,stream=True)
            print(res,res.url)
            content_length = int(res.headers['content-length'])
            # if content_length < pre_content_length or (
            #     os.path.exists(paths) and os.path.getsize(paths) == content_length):
            #     break
            if (os.path.exists(paths)):
                if (os.path.getsize(paths) == content_length):
                    break
                else:os.remove(paths)
            # pre_content_length = content_length
            with open(paths, 'ab') as file:
                for _ in res.iter_content(chunk_size=1024*1024):   
                # for _ in res.iter_lines():
                    if _:
                        file.write(_)
                        file.flush()
                print('receive data，file size : %d  total size:%d' % (os.path.getsize(paths), content_length))
            break
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
    res = json.loads(res.content)
    lists = res['content']['list']
    info = []
    urls = 'http://202.105.10.126:8055/api/v1/video/'
    for _ in lists:
        re = requests.get(urls+str(_['id'])+'?v=706611?',headers={'Authorization':'bearer  '\
        +token},timeout=6000,verify= False)
        re = json.loads(re.content)['content']
        info.append((re['url'],re['tsNo']))
    print(len(lists))
    return lists,info,len(lists)

def smoke_move(ID):
    target ='./target_smoke/'
    Y  = False
    for _,fdir,files in os.walk('./video'):
        for f in files:
            if ID in f:
                print('dicrection:',path.join(_,f))
                dirs = target+path.split(_)[-1]
                if not path.exists(dirs):os.makedirs(dirs)
                shutil.move(path.join(_,f),dirs)
                Y = True
    # if Y:print('移动成功')
    # else:print('找不到该ID')
    return Y

def zips(startdir=None,file_news=None):
    startdir = "./target_smoke"  #要压缩的文件夹路径
    if path.exists(startdir):
        shutil.rmtree(startdir)
    os.makedirs(path.abspath(startdir))
    file_news = '.'+startdir +'.zip' # 压缩后文件夹的名字
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
    TSNO={
        "SFE-R600-G22W2807":"广清大道(龙塘)",
        "SFE-R600-G22W2714":"治超站出口",
        "SFE-R600-G22W2772":"三棵竹一桥(源潭)",
        "SFE-R600-G22W2798":"清远大道(党校)"
    }
    url_qy = 'http://202.105.10.126:8055/api/v1/login/'
    url = 'http://202.105.10.126:8055/api/v1/smokeMessagePageQuery'
    pool = ThreadPoolExecutor(max_workers=4)
    l,info,total_video_num= get_mp4_info(url)
    p = []#名字
    ur = []
    for _,(u,tsno)in zip(l,info):
        time_name = time.strftime('%Y-%m-%d %H.%M.%S',time.localtime(int(str(_['monitorTime'])[0:10])))
        site = TSNO[tsno]
        p.append(('./video/'+site+'/'+time_name+'-'+_['id']+'.mp4'))
        ur.append('http://202.105.10.126:8055/video/'+u)

    all_task = [pool.submit(dwd,p,ur) for p,ur in zip(p,ur)]
    wait(all_task,return_when=ALL_COMPLETED)
    print('total_video_num:',total_video_num)
    x =input('请输入ID号:')
    while True:
        Y =smoke_move(x)
        print('退出输入q or quit!')
        if Y:
            print('目标ID移动成功')
            x =input('请输入新ID:')
            # break
        else:
            x =input('找不到该ID,请输入正确ID:') 
        if x =='q' or x =='quit':
            break
    zips()