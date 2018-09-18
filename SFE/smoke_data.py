import requests
import os,shutil
from os import path
import json,time
import zipfile

from concurrent.futures import ThreadPoolExecutor,ALL_COMPLETED,wait

global URL,Chunk_Size,TSNO
Chunk_Size =1024
URL =['http://202.105.10.126:8055','http://117.158.91.105:6153']#[qy,xx]
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
'''
    @@ flag ∈ (0,1)<->(清远,新乡)
'''
def params(flag,begindate,enddate,pagesize=1000):
    if flag==0:
        param = {
            'provinceId':440000,
            'cityId':441800,
            'countyId':'',
            'tsNo':'',
            'monitorBeginTime':str(begindate),
            'monitorEndTime':str(enddate),
            'pageSize':pagesize,
            'pageNum':1
        }
        return param
    if flag==1:
        param = {
        'provinceId':410000,
        'cityId':410700,
        'countyID':410701,
        'tsNo':'',
        'monitorBeginTime':str(begindate),
        'monitorEndTime':str(enddate),
        'pageSize':pagesize,
        'pageNum':1
        }
        return param
    raise '参数错误！'
    
def down_video(url):
    assert isinstance(url,str)
    try:
        res = requests.get(url,stream=True)
        return res
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
def zips(flag,zip_name,startdir="./target_smoke",fpath = 'H:/分类任务/清远黑烟/清远平台/'):
    '''
        @paramer
    '''
    # if path.exists(startdir):
    #     shutil.rmtree(startdir)
    # if not path.exists(startdir):os.makedirs(path.abspath(startdir))
    file_news = fpath+zip_name +'.zip' # 压缩后文件夹的名字
    print('zip-name:',file_news)
    z = zipfile.ZipFile(file_news,'w',zipfile.ZIP_DEFLATED) #参数一：文件夹名（路径）
    for dirpath, dirnames, filenames in os.walk(startdir):
        for filename in filenames:
            ff = path.join(dirpath,filename)
            _,target_mon,target_day = list(map(lambda x:int(x),filename.split(' ')[0].split('-')))
            print('ff:',ff)
            if flag==0:
                cond_0 = path.split(dirpath)[-1] in['广清大道(龙塘)','治超站出口','三棵竹一桥(源潭)','清远大道(党校)']
            if flag==1:
                cond_0 = path.split(dirpath)[-1] not in['广清大道(龙塘)','治超站出口','三棵竹一桥(源潭)','清远大道(党校)']
            #zip_name:xxxx-xx.xx-.xx.xx xxxx-xx-xx#
            if '-.' in zip_name:#检测多天
                x1,x2 = [_.split('.') for _ in zip_name.split('-.')]
                x1 = [x1[0].split('-')[-1],x1[-1]] #第一部分
                if x2[0]>=x1[0] and x2[-1]>=x1[-1]:
                    if target_mon in [_ for _ in range(int(x1[0]),int(x2[0]+1))] and \
                        target_day in [_ for _ in range(int(x1[-1]),int(x2[-1]+1))]:
                        cond_1 =True
                    else:cond_1 =False
                else:
                    '''
                        处理特殊日期
                    '''
                    #8-31 9-2 12-31 1-2
                    x = [_ for _ in range(x2[-1]+1)]
                    x = x + [_ for _ in range(x1[-1],32)]
                    if target_mon in [x2[0],x1[0]] and target_day in x:
                        cond_1 = True
                    else:cond_1 = False
                    #---stop---#
                    # print('该数据特殊请修改代码!date1-date2!',x1,x2)
                    # raise ('查询日期特殊,请手动修改!')
            #检测当天
            else:cond_1 = str(time.strftime('%Y-%m-%d',time.localtime())) in ff
            if cond_1 and cond_0:
                print('ppp:',dirpath)
                z.write(ff)
                print ('压缩成功,',path.join(dirpath,filename))
    z.close()
#-------start------#
def download(url,paths):
    #判断文件夹是否存在
    [dir_name,dir_basename] = path.split(paths)
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

def get_mp4_info_list(pre_url,check_date,flag,day_num=2):
    '''
        -paramer@check_date:['1','y','Y']->检测礼拜,其他->正常检测
    '''
    # url_qy = 'http://202.105.10.126:8055/api/v1/login/'
    assert isinstance(pre_url,str)
    if (pre_url[-1]!='/'):pre_url=pre_url+'/'
    print(pre_url,'##',pre_url[-1]!='/')
    login_url = pre_url+'api/v1/login/'
    if check_date in['1','y','Y']:
        # from datetime import datetime
        import datetime
        import calendar
        now_time = datetime.datetime.now()
        isweekday = now_time.isoweekday()
        begindate = (now_time + datetime.timedelta(days = -day_num)).strftime('%Y-%m-%d')+ ' 00:00:00'
        enddate = (now_time + datetime.timedelta(days = -1)).strftime('%Y-%m-%d')+' 23:59:59'
        zip_name = '.'.join(str(begindate[:10]).split('-')).replace('.','-',1)+'-'+\
            '.'.join((str(enddate[:10]).split('-')[-2],str(enddate[:10]).split('-')[-1]))
    else:    
        begindate= time.strftime("%Y-%m-%d", time.localtime())+ ' 00:00:00'
        enddate = time.strftime("%Y-%m-%d", time.localtime())+' 23:59:59'
        zip_name =time.strftime('%Y-%m-%d',time.localtime())
    print(f'date-->-:{begindate}<-->{enddate}')
    param =params(flag,begindate,enddate,1)
    token = get_token(login_url)
    url = pre_url+'api/v1/smokeMessagePageQuery'
    res = requests.get(url,params=param,headers={'Authorization':'bearer  '\
        +token},timeout=6000,verify= False)
    print('res:',res,res.content)
    res = json.loads(res.content)
    lists = res['content']['list']
    info = []
    urls = pre_url+'api/v1/video/'
    for _ in lists:
        try:
            re = requests.get(urls+str(_['id'])+'?v=706611?',headers={'Authorization':'bearer  '\
            +token},timeout=6000,verify= False)
        except Exception as e:
            print(e)
        re = json.loads(re.content)['content']
        info.append((re['url'],re['tsNo']))
    print(len(lists))
    return lists,info,len(lists),zip_name    

def move_targtId_to_path(ID=None,flag=None,target='./target_smoke/'):
    if ID in [None,'',' ']:
        print('ID错误!')
        return
    # target ='./target_smoke/'
    Y  = False
    for _,fdir,files in os.walk('./video'):
        for f in files:
            if (ID in f):
                print(path.split(_))
                belongFolder = None #判断文件夹名字属于的哪个地区
                if flag==0:#清远
                    belongFolder = path.split(_)[-1] not in['广清大道(龙塘)','治超站出口','三棵竹一桥(源潭)','清远大道(党校)']
                if flag==1:#新乡
                    belongFolder = path.split(_)[-1] in['广清大道(龙塘)','治超站出口','三棵竹一桥(源潭)','清远大道(党校)']
                if belongFolder:
                    continue
                print('dicrection:',path.join(_,f)) 
                dirs = target+path.split(_)[-1]
                if not path.exists(dirs):os.makedirs(dirs)
                shutil.move(path.join(_,f),dirs)
                Y = True
    # if Y:print('移动成功')
    # else:print('找不到该ID')
    return Y

def pre_start(root_dir='./video/'):
    if root_dir[-1] not in['/','\\']:
        root_dir =root_dir+'/'
    global TSNO
    print('\n-----清远:0---新乡:1-----')
    flag = int(input('输入查询的地区(0 or 1)↑:'))
    if flag not in [1,0]:raise '错误的输入！👆'
    print("['1','y','Y']->检测礼拜,其他(0,a,b,c···)->检测工作日(周一----周五)'")
    check_date  = input('检测(需求))👆::')
    try:
        prex_url = URL[flag]
    except Exception as e:
        print(e)
    lists,info,total_video_num ,zip_name= get_mp4_info_list(prex_url,check_date,flag,2)
    names = [] # video/mp4’name
    urls = [] # video/mp4’infomation
    for _,(url,tsno)in zip(lists,info):
        time_name = time.strftime('%Y-%m-%d %H.%M.%S',time.localtime(int(str(_['monitorTime'])[0:10])))
        site = TSNO[tsno]
        names.append((root_dir+site+'/'+time_name+'-'+_['id']+'.mp4'))
        urls.append(prex_url+'/video/'+url)
    return names,urls,prex_url,total_video_num,flag,zip_name

def start(target_path='./target_test',down_video_path='./video_test'):
    names,urls,prex_url,total_video_num,flag,zip_name = pre_start(down_video_path)
    pool = ThreadPoolExecutor(max_workers=4)
    all_task = [pool.submit(download,url,name) for name,url in zip(names,urls)]
    wait(all_task,return_when=ALL_COMPLETED)
    print('today smoke’s num->total_video_num:',total_video_num)
    print('退出输入:q or n')
    ID = input('请输入ID:')
    while   True:
        if ID.lower() =='q' or ID.lower() =='n':
            break
        Y =move_targtId_to_path(ID,flag,target_path)
        print('退出输入q or quit!')
        if Y:
            print('目标ID移动成功')
            ID =input('请输入新ID:')
        else:
            ID =input('找不到该ID,请输入正确ID:')
    zz = input('是否压缩(y or n):')
    if zz.lower() =='y':
        zips(flag,zip_name)
    else:print('操作完成🆗')
if __name__=='__main__':
    print('start···')
    start()