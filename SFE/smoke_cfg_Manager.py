import requests
import os,shutil
from os import path
import json,time
import zipfile
from concurrent.futures import ThreadPoolExecutor,ALL_COMPLETED,wait

global PRE_URL,Cookies,Chunk_Size
PRE_URL = 'http://218.28.71.220:1570/api/'
Cookies={'session_id': '508e3929c760f48a7f80c07a280d725009ee541f'}
Chunk_Size =1024
TSNO={
    "SFE-R600-B22W4419":"移动式",
    "SFE-R600-V22W3522":"S229环宇立交桥治超站1号机",
    "SFE-R600-V22W4495":"S229环宇立交桥治超站2号机",
    "SFE-R600-V23W1906":"S308大召营镇1号机",
    "SFE-R600-V23W1922":"S308大召营镇2号机",
    "SFE-R600-V23W1948":"S308新乡收费站1号机",
    "SFE-R600-V23W2819":"S308新乡收费站2号机",
    "SFE-R600-V23W2833":"G107好运饲料1号机",
    "SFE-R600-V23W2851":"G107好运饲料2号机",
    "SFE-R600-V23W2902":"G107铁道路桥1号机",
    "SFE-R600-V23W2926":"G107铁道路桥2号机",
    "SFE-R600-G22W2807":"广清大道(龙塘)",
    "SFE-R600-G22W2714":"治超站出口",
    "SFE-R600-G22W2772":"三棵竹一桥(源潭)",
    "SFE-R600-G22W2798":"清远大道(党校)"
}
##---mp4---http://218.28.71.220:1570/api/+\
#       record/SFE-R600-V23W1906/20180918144332.619583/video
# --确认---http://218.28.71.220:1570/api/record/SFE-R600-V23W1906/+\
#       20180918124537.883825/status
#all lists http://218.28.71.220:1570/api/record/SFE-R600-V23W1906/

#'exist'http://218.28.71.220:1570/api/status
def get_lists(url):
    res = requests.get(url,cookies=Cookies)
    try:
        lists = list(json.loads(res.content)['content'])
    except:
        raise 'COOKIES 无效!!!'
    return lists

def get_sites(url):
    res = requests.get(url,cookies=Cookies)
    sites = json.loads(res.content)['content'].keys()
    return list(sites)

def down_video(url):
    assert isinstance(url,str)
    try:
        res = requests.get(url,stream=True,cookies=Cookies)
        print(res)
        return res
    except Exception as e:
        print(e)
def download(url,paths):
    #判断文件夹是否存在
    [dir_name,dir_basename] = path.split(paths)
    # yield
    if not path.exists(dir_name):os.makedirs(dir_name)
    res=down_video(url)
    while   res:    
        content_length = int(res.headers['content-length'])
        if path.exists(paths):
            if path.getsize(paths)==content_length:
                print(res,res.url,'already exists!')
                break
            else:os.remove(paths)
        begin_t = time.time()               
        with open(paths,'ab') as f:
            for _ in res.iter_content(chunk_size=Chunk_Size*Chunk_Size):
                if _:f.write(_),f.flush()
            print('download sucessly,receive data,file size : %d  total size:%d' % (os.path.getsize(paths), content_length))
            if path.getsize(paths) ==content_length:break
        res=down_video(url)

###-------------start--------------#
pool = ThreadPoolExecutor(max_workers=4)

def pre_start(pre_path='./video/'):
    if pre_path[-1] not in ['\\','/']:
        pre_path = pre_path +'/'
    site_url = 'http://218.28.71.220:1570/api/status'
    list_pre = 'http://218.28.71.220:1570/api/record/'
    sites = get_sites(site_url)
    for site in sites:
        lists =get_lists(list_pre+site)
        names = []
        for l in lists: 
            # print(l['upload'],l['upload']=='未上传')
            if l['status']==False and l['upload']=='未上传':
                names.append(l['name'])
        print(names)
        mp4_url= []
        target_name = []
        for name in names:
            mp4_url.append('http://218.28.71.220:1570/api/record/'+site+'/'+name+'/video')
            target_name.append(pre_path+TSNO[site]+'/'+name+'.mp4')
            # print(TSNO[site])
        all_task = [pool.submit(download,url,name) for name,url in zip(target_name,mp4_url)]
        wait(all_task,return_when=ALL_COMPLETED)
#确认

def confirm(ID,paths,current=time.time()):
    if ID in ['',None]:
        raise '请输入正常的ID!!'
    if ID==['no']:
        is_confirm =True
    time_range = [time.mktime(time.strptime(i[:8],"%Y%m%d")) for i in ID]
    sites = dict(zip(TSNO.values(),TSNO.keys()))
    for p,fdirs,files in os.walk(paths):
        for _ in files:
            timestamp = _[:-4]
            # timestamp  = timestamp[:8]
            # dates = time.strptime(timestamp,"%Y%m%d%H%M%S")
            # timestamp = time.mktime(dates)
            print('timestamp,time_range:\n',timestamp,time_range)
            # if timestamp <int(min(time_range)) or timestamp >int(max(time_range)) \
            #     or timestamp < int(current):
            #     continue
            site = sites[path.split(p)[-1]]
            # 如果all(IDS) not in 文件名中则确认
            print('##',len([True for i in ID if i not in _])==len(ID))
            if len([True for i in ID if i not in _])==len(ID) :
                url = 'http://218.28.71.220:1570/api/record/'+site+\
                  '/'+timestamp+'/status'
                try:
                    res = requests.get(url,cookies=Cookies)
                    print(res.url,'确认成功！')
                    # print('确认成功！')
                except Exception as e:
                    print(e)

if __name__ == '__main__':
    path_name = time.strftime('%Y-%m-%d',time.localtime())
    
    #---download---#
    path_name = time.strftime('%Y-%m-%d',time.localtime())
    # pre_start('./video_new/'+path_name)


    #----confirm-----#
    k = []
    x = input('ID(q or n end!):')
    while x.lower() not in ['q','n']:
        k.append(x)
        x = input('请继续输入ID:')
    confirm(k,'./video_new/'+path_name)

    ##----stop----##
    # import re
    # x =input(':')
    # while True:
    #     if x[0] in ['',' ']:
    #         x = x[1:]
    #     else:break
    # k = re.split('[\s]',x)
    # print(len(x),len(k),k)
    # print('xx:',x)