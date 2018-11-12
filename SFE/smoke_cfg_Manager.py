import requests
import os,shutil,cv2,random

from os import path
import json,time
import zipfile
import numpy as np
from concurrent.futures import ThreadPoolExecutor,ALL_COMPLETED,wait,FIRST_COMPLETED
def cv_imread(f_path):
    img = cv2.imdecode(np.fromfile(f_path,dtype=np.uint8),-1)
    return img

def cv_imwrite(f_path,im):
    cv2.imencode('.jpg',im)[1].tofile(f_path)#保存图片

global PRE_URL,Cookies,Chunk_Size,qys,xxs,INDEX
qys ='http://202.105.10.126:1577'
xxs ='http://218.28.71.220:1570'
select = [qys,xxs]
# PRE_URL = qys
#qy'f0c3672cc1e1d66eab02a9bdf0babf2ceef4c7f6'
#xx'e6a187cdec0afdd50780f797dfd20afd17f3e426'
# Cookies={'session_id': 'f0c3672cc1e1d66eab02a9bdf0babf2ceef4c7f6'}
Cookies =None
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
XLS_NAME={
    '广清大道(龙塘)':1,
    '清远大道(党校)':2,
    '三棵竹一桥(源潭)':3,
    '治超站出口':4,
    'G107好运饲料1号机':5,
    'G107铁道路桥1号机':6,
    'S229环宇立交桥治超站1号机':7,
    'S308大召营镇1号机':8,
    'S308新乡收费站1号机':9
}
##---mp4---http://218.28.71.220:1570/api/+\
#       record/SFE-R600-V23W1906/20180918144332.619583/video
# --确认---http://218.28.71.220:1570/api/record/SFE-R600-V23W1906/+\
#       20180918124537.883825/status
#all lists http://218.28.71.220:1570/api/record/SFE-R600-V23W1906/

#'exist'http://218.28.71.220:1570/api/status


def Classification(namePrefix='video_qy',dir_name='2018-11-08',Names=['车辆误判','黑烟视频','黑烟误判']):
    switch =True
    currentDir =os.getcwd()
    for _ in Names:
        if not path.exists(namePrefix+'/'+path.join(dir_name,dir_name,_)):
            os.makedirs(namePrefix+'/'+path.join(dir_name,dir_name,_))
    srcPath = namePrefix+'/'+path.join(dir_name,dir_name)

    for d in os.listdir(namePrefix+'/'+dir_name):
        print(path.join(namePrefix+'/'+dir_name,d))
        print(f'----{d}----')
        allNames = [ _ for _ in os.listdir(path.join(namePrefix+'/'+dir_name,d)) if _[-3:]=='mp4']

        if not switch:
            break
        for n in allNames:
            try:
                im1 = cv_imread(path.join(namePrefix,dir_name,d+'\\image1\\'+n[:-4]+'_1.jpg'))
                im2 = cv_imread(path.join(namePrefix,dir_name,d+'\\image2\\'+n[:-4]+'_2.jpg'))
            except: 
                print('####error!')
                site = dict(zip(TSNO.values(),TSNO.keys()))[d]
                mp4_url_1 = PRE_URL+'/api/record/'+site+'/'+n[:-4]+'/image1'
                target_name_1 = path.join(namePrefix,dir_name,d,'image1',n[:-4]+'_1.jpg')
                mp4_url_2 = PRE_URL+'/api/record/'+site+'/'+n[:-4]+'/image2'
                target_name_2 = path.join(namePrefix,dir_name,d,'image2',n[:-4]+'_2.jpg')
                print('url:',mp4_url_1)
                print('name:',target_name_1)
                download(mp4_url_1,target_name_1),download(mp4_url_2,target_name_2)
                try:
                    im1 = cv_imread(path.join(namePrefix,dir_name,d+'\\image1\\'+n[:-4]+'_1.jpg'))
                    im2 = cv_imread(path.join(namePrefix,dir_name,d+'\\image2\\'+n[:-4]+'_2.jpg'))
                except:continue
            while(1):
                cv2.imshow('Image1',im1)
                cv2.imshow('Image2',im2)
                k=cv2.waitKey(1)&0xFF  
                if k ==32:
                    break
                if k in [ord('w'),ord('W')]:
                    #写入记录的操作#
                    print('---写入成功---')
                    cv_imwrite(namePrefix+'/'+path.join(dir_name,dir_name,'车辆误判',n[:-4]+'_1.jpg'),im1)
                    cv_imwrite(namePrefix+'/'+path.join(dir_name,dir_name,'车辆误判',n[:-4]+'_2.jpg'),im2)
                if k in [102,70]:
                    os.chdir(path.abspath(path.join(namePrefix,dir_name,d)))
                    os.system(n)
                    os.chdir(currentDir)
                if k==111: #'o' 全部关闭
                    switch = False
            if not switch:break
            
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

def download(url,paths,num=1):
   
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
        try:
            with open(paths,'ab') as f:
                for _ in res.iter_content(chunk_size=Chunk_Size*Chunk_Size):
                    if _:f.write(_),f.flush()
                print('download sucessly,receive data,file size : %d  total size:%d' % (os.path.getsize(paths), content_length))
                if path.getsize(paths) ==content_length:break
        except Exception as e:
            print(e)
        res=down_video(url)

#统计数量xls
xls_names ='黑烟记录表' 
import xlwt
import xlrd,datetime
from xlutils.copy import copy
def get_xls_sheet():
    with open('xls_config.txt',mode='r') as f:
        index = f.read()
        if index in ['',' ',None]:index =0
    if index ==0:
        workbook = xlwt.Workbook()
        ws = workbook.add_sheet(xls_names)
    else:
        wbk = xlrd.open_workbook(xls_names+'.xls')
        workbook = copy(wbk)
        ws = workbook.get_sheet(0)
    return ws,index,workbook
def write_xls(resouce_path,index,ws,site_name,check_times=datetime.datetime.now().strftime('%Y-%m-%d')):
    # ws ,index,wbk= get_xls_sheet()
    all_smoke = len(os.listdir(path.join(resouce_path,site_name)))
    try:
        confirm_smoke = str(len(os.listdir(path.join(resouce_path+'/'+check_times+'-smoke',site_name))))
    except:confirm_smoke = '0'
    all_smoke =str(int(confirm_smoke)+all_smoke)
    print('all_smoke:',all_smoke,'confirm_smoke:',confirm_smoke)
    text = confirm_smoke+'-'+str(all_smoke)
    ws.write(index,XLS_NAME[site_name],text)
###-------------start--------------#
pool = ThreadPoolExecutor(max_workers=8)

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
        print(names)
        mp4_url= []
        target_name = []
        for name in names:
            #视频 download
            mp4_url.append(PRE_URL+'/api/record/'+site+'/'+name+'/video')
            target_name.append(pre_path+TSNO[site]+'/'+name+'.mp4')
            #图片
            mp4_url.append(PRE_URL+'/api/record/'+site+'/'+name+'/image1')
            target_name.append(pre_path+TSNO[site]+'/image1/'+name+'_1.jpg')

            mp4_url.append(PRE_URL+'/api/record/'+site+'/'+name+'/image2')
            target_name.append(pre_path+TSNO[site]+'/image2/'+name+'_2.jpg')

        all_task = [pool.submit(download,url,name) for name,url in zip(target_name,mp4_url)]
        #wait(all_task,return_when=ALL_COMPLETED)
        #wait(all_task,return_when=FIRST_COMPLETED)
#确认

def confirm(ID,paths,flag=False):
    sites_name = [_ for _ in os.listdir(paths) if '2018' not in _]
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
        if p.count('2018',0,len(p)) >=2:
            print(p)
            continue
        if not files:continue
        if 'image1' in p or 'image2' in p:continue
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
                    except Exception as e:
                        print(e)
                # 上传
                else:
                    url =PRE_URL[:7]+'json@'+PRE_URL[7:]+'/api/record/'+site+'/'+f+'/upload'
                    res = requests.get(url,cookies=Cookies)
                    print(res.url,'上传成功！')
                    ps = path.join(paths,path.basename(paths)+'-smoke')
                    ps =path.join(ps,path.split(p)[-1])
                    if not path.exists(ps):os.makedirs(ps)
                    shutil.move(path.join(p,f)+'.mp4',path.join(ps,f)+'_'+ps[-3:]+'.mp4')
            #全部确认
            else:
                site = sites[path.split(p)[-1]]
                url = PRE_URL+'/api/record/'+site+\
                '/'+f+'/status'
                try:
                    #---# 通过文本
                    if ID:
                        if f in ID:
                            url =PRE_URL[:7]+'json@'+PRE_URL[7:]+'/api/record/'+site+'/'+f+'/upload'
                            res = requests.get(url,cookies=Cookies)
                            print(res.url,'上传成功！')
                            ps = path.join(paths,path.basename(paths)+'-smoke')
                            ps =path.join(ps,path.split(p)[-1])
                            if not path.exists(ps):os.makedirs(ps)
                            shutil.move(path.join(p,f)+'.mp4',path.join(ps,f)+'_'+ps[-3:]+'.mp4')
                        else:
                            url = PRE_URL+'/api/record/'+site+\
                            '/'+f+'/status'
                            res = requests.get(url,cookies=Cookies) 
                            print(res.url,'确认成功！')
                    #---#
                    else:
                        res = requests.get(url,cookies=Cookies) 
                        print(res.url,'确认成功！')
                except Exception as e:
                    print(e)

    ##随机选取视频存放到对应的文件夹
    #path:video/20xxx/
    # path.basename ```morning:20181112+07~9 noon:10~13 afternoon:14~17
    for d in sites_name:
        all_name = [_[:-4] for _ in os.listdir(path.join(paths,d)) if path.isfile(path.join(paths,d,_+'.mp4'))]
        morn,noon,afnoon =[],[],[]
        for _ in all_name:
            if str(_[8:10]) in ['7','8','9','10']:
                morn.append([path.join(paths,d,_+'.mp4'),path.join(paths,d+'/image1',_+'_1.jpg'),\
                path.join(paths,d+'/image2',_+'_2.jpg')])
            if str(_[8:10]) in ['11','12','13']:
                noon.append([path.join(paths,d,_+'.mp4'),path.join(paths,d+'/image1',_+'_1.jpg'),\
                path.join(paths,d+'/image2',_+'_2.jpg')])
            if str(_[8:10]) in ['14','15','16','17']:
                afnoon.append([path.join(paths,d,_+'.mp4'),path.join(paths,d+'/image1',_+'_1.jpg'),\
                path.join(paths,d+'/image2',_+'_2.jpg')])
    
    #开始导入
        src = path.join(paths,path.basename(paths),'黑烟误判',d)
        for _,n in zip(['上','中','下'],[morn,noon,afnoon]):
            srss = path.join(src,_)
            os.makedirs(srss,exist_ok=True)
            if len(n)==0:continue
            for i in n[int(random.uniform(0,len(n)))]:
                try:
                    shutil.copy(i,srss)
                except:
                    import traceback
                    traceback.print_exc()

def start(down_load_path='./video_qy/',times=''):
    pre_start(down_load_path+times)
if __name__ == '__main__':
    with open('xls_config.txt',mode='r+') as f:
        try:
            INDEX = f.readline()
        except Exception as e:
            print(e)
    import datetime
    paramer ={ 
        'password':'4f768021243118a2ac7f2d6e524346fc',
        'user':'sfe'
    }


    day_num =0      #距离当前的日期的天数 （0表示当天）


    now_time = datetime.datetime.now()
    begindate = (now_time + datetime.timedelta(days = -day_num)).strftime('%Y-%m-%d')
    # path_name = time.strftime('%Y-%m-%d',time.localtime())
    path_name = begindate
    seach_site = input('#---q:退出---0:清远---1:新乡---#:')
    if seach_site=='0':PRE_URL,p=qys, './video_qy/'
    elif seach_site=='1':PRE_URL,p=xxs ,'./video_new/'
    else:raise '错误的站点输入！'
    print('######-',PRE_URL[:7]+'json:sfe@'+PRE_URL[7:]+'/api/login')
    r =requests.post(PRE_URL[:7]+'json:sfe@'+PRE_URL[7:]+'/api/login',json=paramer,timeout=10)
    r =r.headers['Set-Cookie'].split(';')[0].split('=')
    Cookies ={r[0]:r[1]}
    flag = input('#---q:退出---d:下载---c:确认---t:查看图片#:')

    if flag.lower()=='d':
    
    #---download---#
        start(p,times=path_name)
        xls_cow_num = 1
        if seach_site=='1':xls_cow_num =0
        with open('xls_config.txt',mode='r+') as f:
            try:
                index = f.readline()
                print('index',index,len(index))
            except Exception as e:
                print(e)
        with open('xls_config.txt',mode='w') as f:
            f.write(str(int(index)+xls_cow_num))
    elif flag.lower()=='c':
    #----confirm-----#
        print('确认前需要确保各个站点的视频已经下载下来!')
        print('#----y:推送ID---n:全部确认---f:读取文本ID---q:退出----#')
        com =input('输入确认模式↑:')
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
        if com.lower()=='f':
            dirs = input('输入文本路径(默认./config.txt):')
            if dirs in [None,'']:
                print('start')
                k = []
                with open('config.txt',encoding='utf-8',mode='r') as f:
                    k = f.read().split()
                confirm(k,p+path_name,True)
        #统计记录(xls)
        # if com.lower() in ['n','y','f']:        
        #     ws,index,wbk =get_xls_sheet()
        #     resouce_path = p+path_name
        #     for name in os.listdir(resouce_path):
        #         if name[:2]=='20':continue  #排除确认的黑烟
        #         write_xls(resouce_path,int(index),ws,name,path_name)
        #     ws.write(int(index),0,str(path_name))
        #     wbk.save(xls_names+'.xls')
    elif flag.lower()=='q':print('已退出!')
    elif flag.lower() in ['t','T']:
        Classification(p,begindate)
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