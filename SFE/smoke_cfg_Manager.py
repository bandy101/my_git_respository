import requests
import os,shutil
from os import path
import json,time
import zipfile
from concurrent.futures import ThreadPoolExecutor,ALL_COMPLETED,wait

global PRE_URL,Cookies,Chunk_Size,qys,xxs
qys ='http://202.105.10.126:1577'
xxs ='http://218.28.71.220:1570'
PRE_URL = qys
#qy'719a110333e17b6f6e418a6cc207653af79ed185'
#xx'2544e6160dc3a7aad6435cd7fadbaaecadffaae4'
Cookies={'session_id': '2544e6160dc3a7aad6435cd7fadbaaecadffaae4'}
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
    site_url = PRE_URL+'/api/status'
    list_pre = PRE_URL+'/api/record/'
    sites = get_sites(site_url)
    for site in sites:
        lists =get_lists(list_pre+site)
        names = []
        for l in lists: 
            # print(l['upload'],l['upload']=='未上传')
            if l['status']==False and l['upload']=='未上传':
                names.append(l['name'])
        # print(names)
        mp4_url= []
        target_name = []
        for name in names:
            mp4_url.append(PRE_URL+'/api/record/'+site+'/'+name+'/video')
            target_name.append(pre_path+TSNO[site]+'/'+name+'.mp4')
            # print(TSNO[site])
        all_task = [pool.submit(download,url,name) for name,url in zip(target_name,mp4_url)]
        wait(all_task,return_when=ALL_COMPLETED)
#确认

def confirm(ID,paths,flag=False):
    if not flag:
        have_is = [((i not in ['',None],len(i)==21)) for i in ID]
        is_confirm = all([_ for _ in (have_is)])
        if not is_confirm:    
            raise '请输入正常的ID!!'
        Y= False
    else:
        Y= True
    sites = dict(zip(TSNO.values(),TSNO.keys()))
    for p,fdirs,files in os.walk(paths):
        if not files:continue
        alls_file_name = list(map(lambda x:x[:-4],files))
        for f in alls_file_name:
            if not Y:
                ids = [_ for _ in ID]
                if f not in ids:
                    site = sites[path.split(p)[-1]]
                    url = PRE_URL+'/api/record/'+site+\
                    '/'+f+'/status'
                    try:
                        res = requests.get(url,cookies=Cookies)
                        print(res.url,'确认成功！')

                        # print('确认成功！')
                    except Exception as e:
                        print(e)
                else:
                    ps = path.join(paths,'smoke')
                    ps =path.join(ps,paths.split(p)[-1])
                    if not path.exists(ps):os.makedirs(ps)
                    shutil.move(path.join(ps,f)+'.mp4',path.join(p,f)+'.mp4')
            else:
                site = sites[path.split(p)[-1]]
                url = PRE_URL+'/api/record/'+site+\
                '/'+f+'/status'
                try:
                    res = requests.get(url,cookies=Cookies)
                    print(res.url,'确认成功！')
                    # print('确认成功！')
                except Exception as e:
                    print(e)

def start(down_load_path='./video_qy/',times=''):
    pre_start(down_load_path+times)
if __name__ == '__main__':
    path_name = time.strftime('%Y-%m-%d',time.localtime())
    seach_site = input('#---q:退出---0:清远---1:新乡---#:')
    if seach_site=='0':PRE_URL=qys
    elif seach_site=='1':PRE_URL=xxs
    else:raise '错误的站点输入！'
    flag = input('#---q:退出---d:下载---c:确认---#:')

    if flag.lower()=='d':
    #---download---#
        start(times=path_name)
    elif flag.lower()=='c':
    #----confirm-----#
        print('#----y:推送ID---n:全部确认----#')
        com =input('输入确认模式↑:')
        if seach_site=='0':
            p = './video_qy/'
        else:
            p = './video_new/'
        if com.lower()=='y':
            k = []
            x = input('请输入黑烟ID(输入->(q or n) 退出!):')
            while x.lower() not in ['q','n']:
                k.append(x)
                x = input('请继续输入黑烟ID:')
            confirm(k,p+path_name)
        if com.lower()=='n':
            confirm(None,p+path_name,True)
        if com.lower()=='q':
            print('已退出')
    elif flag.lower()=='q':print('已退出!')
    else:raise '输入错误!'
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