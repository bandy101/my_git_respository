import time,os,sys
import calendar


def get_token(url,name,pwd):
    js_pwd ={
    "clientId":"098f6bcd4621d373cade4e832627b4f6",
    'userName':name,
    'password':pwd
    }
    res = requests.post(url,json=js_pwd,verify=False)
    res =json.loads(res.content)
    token = res['content']['token']
    return token


def have_lists_air_telemtry(token,param,url,year,month,day,tsno,lists):

    ps =params_air_telemetry(month,day,param)
    ps['tsNo'] = tsno
    res = requests.get(url,params=ps,headers={'Authorization':token},verify= False)
    
    values = json.loads(res.content)['content']
    lv = values['list']
    if not lv:
        if day==1:
            if month==1:
                _,days = calendar.monthrange(year,12) ##一个月含有多少天
                lv = (have_lists_air_telemtry(token,param,url,year,12,days,tsno,lv))
            else: 
                _,days = calendar.monthrange(year,month-1)
                lv= (have_lists_air_telemtry(token,param,url,year,month-1,days,tsno,lv))
        else:lv =(have_lists_air_telemtry(token,param,url,year,month,day-1,tsno,lv))
    return lv

def params_air_telemetry(m,d,params):
    st = time.localtime()
    if len(str(m))<2:m='0'+str(m)
    if len(str(d))<2:d='0'+str(d)
    st1 =str(list(st)[0])+'-'+str(m)+'-'+str(d)+' 00:00:00'
    st2 =str(list(st)[0])+'-'+str(m)+'-'+str(d)+' 23:59:59'
    x = params
    for _ in params.keys():
        if 'Begin' in _:
            x[_]=st1
        if 'End' in _:
            x[_] = st2
    return x

# 遥测数据管理
def telemetry_data_manerger(url,params,tsno,dict_tsnos,token):
    # url = 'http://202.105.10.126:8055/api/v1/remoteSensingPageQuery'

    keys = dict_tsnos.keys()
    year = list(time.localtime())[0]
    month = list(time.localtime())[1]
    day = list(time.localtime())[2]
    strss =''
    if type(tsno)==str:tsno=[tsno]
    k =None
    for _ in tsno:
        strs =''
        lists = have_lists_air_telemtry(token,params,url,year,month,day,_,[])
        interval = -int(str(lists[0]['monitorTime'])[0:10]) +int(time.time())
        for key in keys:
            if dict_tsnos[key] ==_:
                k=key
                break
        # print(interval//60)
        if (interval//60>18):
            strs +='<b>'+k+'</b>'+'站点 数据<b>异常</b> '+lists[0]['monitorTimeStr']+' 后无遥测数据\n<br>'+\
            '最新数据时间:'+str(lists[0]['monitorTimeStr'])+'  车牌号:'+str(lists[0]['license'])+'<br>'
            strss +=strs
        if strs=='':strss +='<b>'+k+'</b>'+ '站点 数据<b>正常</b>\n<br>'+\
            '最新数据时间:'+str(lists[0]['monitorTimeStr'])+'  车牌号:'+str(lists[0]['license'])+'<br>'

    return(strss)

def searchMap():
    _temp = {
        '遥测数据':telemetry_data_manerger
    }
    return _temp