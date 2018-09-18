import requests
import os,shutil
from os import path
import json,time
import zipfile
from concurrent.futures import ThreadPoolExecutor,ALL_COMPLETED,wait

global PRE_URL,Cookies,Chunk_Size
PRE_URL = 'http://218.28.71.220:1570/api/'
Cookies={'session_id': 'aaebe29b66de5232cb11faad2d357ab857cbb847'}
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
    lists = list(json.loads(res.content)['content'])
    return lists

def get_sites(url):
    res = requests.get(url,cookies=Cookies)
    sites = list(json.loads(res.content)['content'].keys())
    return sites

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
    site_url = 'http://218.28.71.220:1570/api/status'
    list_pre = 'http://218.28.71.220:1570/api/record/'
    sites = get_sites(site_url)
    for site in sites:
        lists =get_lists(list_pre+site)
        names = []
        for l in lists:
            names.append(l['name'])
        # print(names)
        mp4_url= []
        target_name = []
        for name in names:
            mp4_url.append('http://218.28.71.220:1570/api/record/'+site+'/'+name+'/video')
            target_name.append(pre_path+TSNO[site]+'/'+name+'.mp4')
            # print(TSNO[site])
        all_task = [pool.submit(download,url,name) for name,url in zip(target_name,mp4_url)]
        wait(all_task,return_when=ALL_COMPLETED)


if __name__ == '__main__':
    pre_start('./video/')