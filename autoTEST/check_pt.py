import calendar
import json
import time

import requests
from bs4 import BeautifulSoup

global lanzs,henans,sichuans


'''
    @pm2.5 ~115
    @pm10 ~250
    @so2 ~650
    @no2 ~700   
    @o3 ~300
    @co ~35
'''
PM25,PM10,CO,NO2,O3,SO2= 115,250,35,700,300,650
# PM25,PM10,CO,NO2,O3,SO2= 0,0,0,0,0,0
def have_lists(url,year,month,day,tsno,lists):
    if lists:
        return lists
    ps =params_yc(month,day)
    ps['tsNo'] = tsno
    res = requests.get(url,params=ps,headers={'Authorization':token},verify= False)
    values = json.loads(res.content)['content']
    lv = values['list']
    
    if not lists:
        if day==1:
            if month==1:
                _,days = calendar.monthrange(year,12) ##一个月含有多少天
                lists = (have_lists(url,year,12,days,tsno,lv))
            else: 
                _,days = calendar.monthrange(year,month-1)
                lists= (have_lists(url,year,month-1,days,tsno,lv))
        else:lists =(have_lists(url,year,month,day-1,tsno,lv))
    return lists



def have_lists_air_telemtry(token,param,url,year,month,day,tsno,lists):
    # if lists:
    #     return lists
    ps =params_air_telemetry(month,day,param)
    ps['tsNo'] = tsno
    print('parama:',ps)
    res = requests.get(url,params=ps,headers={'Authorization':token},verify= False)
    
    values = json.loads(res.content)['content']
    # print('res,',res)
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


# token = 'bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1bmlxdWVfbmFtZSI6ImRlbW8iLCJwd2QiOiI3MTcyZGE4ZWY1Zjk1NDcwYjQxNWRiZDEwNDg1NjFlYiIsInVzZXJfaWQiOiIzIiwiaXNzIjoicmVzdGFwaXVzZXIiLCJhdWQiOiIwOThmNmJjZDQ2MjFkMzczY2FkZTRlODMyNjI3YjRmNiIsImV4cCI6MTUzNjE5OTY1OCwibmJmIjoxNTM0OTAzNjU4fQ.HdhVhyMJ8ORq1ingSNL4FW_NS17pXx1FVPqlHGwRC_o'
# dict_tsnos = {
#     '广清大道(龙塘)':'AQM65-G22W2807',
#     '治超站出口':'AQM65-G22W2714',
#     '三棵竹一桥(源潭)':'AQM65-G22W2772',
#     '清远大道(党校)':'AQM65-G22W2798',
# }
# dict_tsnos = {
#     '广清大道(龙塘)':'SFE-R600-G22W2807',
#     '治超站出口':'SFE-R600-G22W2714',
#     '三棵竹一桥(源潭)':'SFE-R600-G22W2807',
#     '清远大道(党校)':'SFE-R600-G22W2798',
# }
gzs = {
}
# params ={
#     'cityId' :441800,
#     'collectionBeginDate':	'2018-08-24 00:00:00',
#     'collectionEndDate'	:'2018-08-24 23:59:59',
#     'countyId':	441801,
#     'maxCo':'',
#     'maxHumidity':'',	
#     'maxNo2':'',	
#     'maxO3':'',
#     'maxPm10':'',	
#     'maxPm25':'',	
#     'maxSo2':'',	
#     'maxTemperature':'',	
#     'minCo':'',	
#     'minHumidity':'',	
#     'minNo2':'',	
#     'minO3':'',	
#     'minPm10':'',	
#     'minPm25':'',	
#     'minSo2':'',	
#     'minTemperature':'',
#     'pageNum':1,
#     'pageSize':12,
#     'provinceId':440000,
#     'tsNo':''
# }
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
#--空气质量--#
def air_quality(url,params,tsno,dict_tsnos,token):
    ##--清远--#
    # url ='http://202.105.10.126:8055/api/v1/monitorAirQualityInfo?provinceId=440000&cityId=441800'
    res = requests.get(url,params=params,headers={'Authorization':token},timeout=6000,verify= False)
    values = json.loads(res.content)['content']
    if type(tsno)==str:values = [_ for _ in values if _['tsNo']==tsno]
    #异常列表
    exe = []
    # print(values)
    strss ='<b>空气质量合格标准界限值</b>:<br><b>PM25:115 PM10:250 CO:35 NO2:700 O3:300 SO2:650</b><br><br>'
    for v in values:
        strs =''
        if v['pm25']>PM25:
            strs +=v['name']+' PM2.5:'+str(v['pm25'])+'  数据异常'+'\n<br>'
        if v['pm10']>PM10:
            strs +=v['name']+' PM10:'+str(v['pm10'])+'  数据异常'+'\n<br>'    
        if v['o3']>O3:
            strs +=v['name']+' O3:'+str(v['o3'])+'  数据异常'+'\n<br>'
        if v['so2']>SO2:
            strs +=v['name']+' SO2:'+str(v['so2'])+'  数据异常'+'\n<br>'
        if v['co']>CO:
            strs +=v['name']+' CO:'+str(v['co'])+'  数据异常'+'\n<br>'
        if v['no2']>NO2:
            strs +=v['name']+' NO2:'+str(v['no2'])+'  数据异常'+'\n<br>'
        if not strs:strss +=v['name'] +'  所有数据正常\n<br>PM2.5:'+str(v['pm25'])+' PM10:'+str(v['pm10'])+\
            ' O3:'+str(v['o3'])+' SO2:'+str(v['so2'])+' CO:'+str(v['co'])+' NO2:'+str(v['no2'])+'<br>'
        else:strss +=strs
    # print(strs)
    return strss
#--空气质量数据管理--#
def air_quality_data_manger(url,params,tsno,dict_tsnos,token):
    strss =''
    ps = params
    # print('pp',params)
    keys = dict_tsnos.keys()
    # url = 'http://202.105.10.126:8055/api/v1/airQualityPageQuery'
    year = list(time.localtime())[0]
    month = list(time.localtime())[1]
    day = list(time.localtime())[2]
    if type(tsno)==str:tsno =[tsno]
    else: tsno=[_ for _ in tsno]
    k = None
    for _ in tsno:
        print('TSNO-',_)
        strs =''
        for key in keys:
            # print(dict_tsnos[key],_)
            # print(dict_tsnos[key]==_)
            if dict_tsnos[key] ==_:
                k=key
                break
        params['tsNo'] = _
        lists=have_lists_air_telemtry(token,params,url,year,month,day,_,[])
        print('str:',strs)
        # time.sleep(1)
        interval = -int(str(lists[0]['collectionDate'])[0:10]) +int(time.time())
        if (interval//60>18):
            strs +=k + '站点 数据异常 '+lists[0]['collectionDateStr']+' 后无空气质量数据\n'
            continue
        o3,no2,co,so2=False,False,False,False
        for l in lists:
            if  not o3:
                if l['o3']!=0:o3=True
            if  not no2:
                if l['no2']!=0:no2=True
            if  not co:
                if l['co']!=0:co=True
            if  not so2:
                if l['so2']!=0:so2=True
        if  not all([o3,so2,co,so2]):
            strs +=k + '站点 数据值异常'+'<br>O3:'+str(l['o3'])+' NO2:'+str(l['no2'])\
            +' CO:'+str(l['co'])+' SO2:'+str(l['so2'])+'<br>'
        if strs=='':strss +='<b>'+k +'</b>'+ '站点 数据正常<br>O3:'+str(l['o3'])+' NO2:'+str(l['no2'])\
            +' CO:'+str(l['co'])+' SO2:'+str(l['so2'])+'<br>'
        print (strss)
    print(strss)
    return strss

#--空气质量统计--#
#日统计
def air_quality_statistics_day(url,params,tsno,dict_tsnos,token):
    strs =''
    keys = dict_tsnos.keys()
    date = str(time.strftime("%Y-%m-%d", time.localtime()))
    params['date'] = date
    resent_hour = list(time.localtime())[3]
    if type(tsno)==str:tsno =[tsno]
    k =None
    for _ in tsno:
        for key in keys:
            print(dict_tsnos[key],_)
            if dict_tsnos[key] ==_:
                k=key
                break
        params['tsNo'] = _
        res = requests.get(url,params=params,headers={'Authorization':token},timeout=6000,verify= False)
        print(res)
        values = json.loads(res.content)['content']
        # print(values)
        have_air = False
        if not values:
            strs +=k +'  '+date+' 空气质量日统计报表无数据'+'\n<br>'
        else:   
            o3,no2,co,so2=False,False,False,False
            ##检测当前时间前几个小时是否有数据
            for _ in range(0,4):

                l = values[(24+resent_hour-_)]
                strs +='<br>#'+l['recordDateStr']+'#  '
                if  not o3:
                    if l['o3']!=0:
                        strs +=' O3:'+str(l['o3'])
                        o3=True
                if  not no2:
                    if l['no2']!=0:
                        strs +=' NO2:'+str(l['no2'])
                        no2=True
                if  not co:
                    if l['co']!=0:
                        strs +=' CO:'+str(l['co'])
                        co=True
                if  not so2:
                    if l['so2']!=0:
                        strs +=' SO2:'+str(l['so2'])
                        so2=True
                if all([o3,so2,co,so2]):
                    have_air =True
                    break
            else:
                have_air=all([o3,so2,co,so2])
                print([o3,so2,co,so2])
            print(have_air)
            if have_air:
                strs +='<br>'+k +' 空气质量日统计报表数据正常'+'\n<br>'
            else:strs +='<br>'+k +' 空气质量日统计报表数据异常'+'\n<br>'
    return strs
#月统计
def air_quality_statistics_month(url,params,tsno,dict_tsnos,token): 
    strs =''
    date = str(time.strftime("%Y-%m-%d", time.localtime()))
    params['date'] = date
    keys =dict_tsnos.keys()
    resent_day = list(time.localtime())[2]
    if type(tsno)==str:tsno =[tsno]
    k =None
    for _ in tsno:
        for key in keys:
            if dict_tsnos[key] ==_:
                k=key
                break
        params['tsNo'] = _
        res = requests.get(url,params=params,headers={'Authorization':token},timeout=6000,verify= False)
        values = json.loads(res.content)['content']
        have_air = False
        if not values:
            strs +=k +'  '+date+' 空气质量月统计报表无数据'+'\n<br>'
        else:
            o3,no2,co,so2=False,False,False,False
            ##检测当前时间前几天是否有数据
            for _ in range(1,3):
                l = values[(resent_day-_-1)]
                strs +='<br>#'+l['recordDateStr']+'#  '
                if  not o3:
                    if l['o3']!=0:
                        strs +=' O3:'+str(l['o3'])
                        o3=True
                if  not no2:
                    if l['no2']!=0:
                        strs +=' NO2:'+str(l['no2'])
                        no2=True
                if  not co:
                    if l['co']!=0:
                        strs +=' CO:'+str(l['co'])
                        co=True
                if  not so2:
                    if l['so2']!=0:
                        strs +=' SO2:'+str(l['so2'])
                        so2=True
                if all([o3,so2,co,so2]):
                    have_air =True
                    break
            else:
                have_air=all([o3,so2,co,so2])
                print([o3,so2,co,so2])
            print(have_air)
            if have_air:
                strs +='<br>'+k +' 空气质量月统计报表数据正常'+'\n<br>'
            else:strs +='<br>'+k +' 空气质量月统计报表数据异常'+'\n<br>'
    return strs
#年统计
def air_quality_statistics_year(url,params,tsno,dict_tsnos,token):
    # param = {
    #    'provinceId':440000,'cityId':441800,'countyId':441801,'tsNo':'','date':str(time.strftime("%Y-%m-%d", time.localtime()))
    # }
    keys = dict_tsnos.keys()
    strs =''
    date = str(time.strftime("%Y-%m-%d", time.localtime()))
    url = 'http://202.105.10.126:8055/api/v1/airReportYear'
    params['date']=date
    resent_month = list(time.localtime())[1]
    if type(tsno)==str:tsno =[tsno]
    k =None ##site--name
    for _ in tsno:
        for key in keys:
            if dict_tsnos[key] ==_:
                k=key
                break
        params['tsNo'] = _
        res = requests.get(url,params=params,headers={'Authorization':token},timeout=6000,verify= False)
        values = json.loads(res.content)['content']
        # print(values)
        ##检测当前时间前几个小时是否有数据
        have_air = False
        if not values:
            strs +=k +'  '+date+' 空气质量年统计报表无数据'+'\n<br>'
        else:
            o3,no2,co,so2=False,False,False,False
            for _ in range(1,2):
                l = values[(resent_month-1)]
                strs +='<br>#'+l['recordDateStr']+'#  '
                if  not o3:
                    if l['o3']!=0:
                        strs +=' O3:'+str(l['o3'])
                        o3=True
                if  not no2:
                    if l['no2']!=0:
                        strs +=' NO2:'+str(l['no2'])
                        no2=True
                if  not co:
                    if l['co']!=0:
                        strs +=' CO:'+str(l['co'])
                        co=True
                if  not so2:
                    if l['so2']!=0:
                        strs +=' SO2:'+str(l['so2'])
                        so2=True
                if all([o3,so2,co,so2]):
                    have_air =True
                    break
            else:
                have_air=all([o3,so2,co,so2])
                print([o3,so2,co,so2])
            print(have_air)
            if have_air:
                strs +='<br>'+k +' 空气质量年统计报表数据正常'+'\n<br>'
            else:strs +='<br>'+k +' 空气质量年统计报表数据异常'+'\n<br>'
    return strs

#--遥测--#
#遥测数据管理
def params_yc(m,d):
    st = time.localtime()
    if len(str(m))<2:m='0'+str(m)
    if len(str(d))<2:d='0'+str(d)
    st1 =str(list(st)[0])+'-'+str(m)+'-'+str(d)+' 00:00:00'
    st2 =str(list(st)[0])+'-'+str(m)+'-'+str(d)+' 23:59:59'
    params={
        'cityId' :441800,
        'monitorBeginTimeStr':st1,
        'monitorEndTimeStr'	:st2,
        'countyId':	441801,
        'pageNum':1,
        'pageSize':10,
        'provinceId':440000,
        'tsNo':'',
        'isNotZero':0,

        'license':'',
        'maxCO':'',
        'maxCO2':'',	
        'maxConfidence':'',	
        'maxHC':'',	
        'maxNO':'',	
        'maxSmoke':'',	
        'maxVSP':'',	
        'minCO':'',	
        'minCO2':'',	
        'minConfidence':'',	
        'minHC':'',	
        'minNO':'',	
        'minSmoke':'',	
        'minVSP':'',	
        'result':'',
        'validity':''
    }
    # print (params)
    return params

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
            strs +='<b>'+k+'</b>'+'站点 数据<b>异常</b> '+lists[0]['monitorTimeStr']+' 后无遥测数据\n<br>'
            strss +=strs
        if strs=='':strss +='<b>'+k+'</b>'+ '站点 数据<b>正常</b>\n<br>'+str(lists[0])+'<br>'

    return(strss)


#遥测日统计
def telemetry_data_day(url,params,tsno,dict_tsnos,token):
    # param = {
    #     'tsNo':'SFE-R600-G22W2807','date':'2018-08-22','smoke':'25','no':'','hc':600,'co':''
    # }
    strss =''
    keys = dict_tsnos.keys()
    date = str(time.strftime("%Y-%m-%d", time.localtime()))
    params['date'] = date
    if type(tsno)==str:tsno =[tsno]
    site_name=''
    for _ in tsno:
        # strs =''
        for k in keys:
            print(dict_tsnos[k],_)
            if dict_tsnos[k]==_:
                site_name =k
                break
        params['tsNo']=_
        res = requests.get(url,params=params,headers={'Authorization':token},verify= False)
        values = json.loads(res.content)['content']
        yctj,cxyz,cxcllx,cxclbl = 0 ,0,0,0
        if not ('licenseType' in values.keys()):
            yctj =0
        else:yctj = values['licenseType']['total']
        date = date
        cxyzs = [values['exceed']['coCount'],values['exceed']['hcCount'],values['exceed']['limitCount'],values['exceed']['noCount'],values['exceed']['smokeCount']]
        cxyz =any(cxyzs)
        cxyzs = list(map(lambda x:str(x),cxyzs))
        print(cxyzs)
        v = values['overrunCar']
        _car =[v['bigBusCount'],v['bigTruckCount'],v['busCount'],v['carCount'],v['truckCount'],v['suvCount'],v['pickUpCount'],v['unknownCount'],v['minibusCount']]
        cxcllx = any(_car)
        _car =list(map(lambda x:str(x),_car))

        cxclbl = v['nativeCount']+v['inProvinceCount']+v['nonLocalCount']
        is_ok = all([yctj,cxyz,cxcllx,cxclbl])

        if (is_ok):strss +=site_name+' 该站点遥测日统计数据<font  color="black"><b>正常</b></font><br>'+\
            '遥测统计总数:'+str(yctj)+' 超限车辆类型数目依次为:'+','.join(_car)+' 超限车辆比例总数:'+str(cxclbl)+\
            ' 超限因子数目依次为:'+','.join(cxyzs)+'<br>'
        else:strss +=site_name+' 该站点遥测日统计数据<font  color="red"><b>异常</b></font><br>'+\
            '遥测统计总数:'+str(yctj)+' 超限车辆类型数目依次为:'+','.join(_car)+' 超限车辆比例总数:'+str(cxclbl)+\
            ' 超限因子数目依次为:'+','.join(cxyzs)+'<br>'
    return strss

#遥测月统计
def telemetry_data_month(url,params,tsno,dict_tsnos,token):
    strss =''
    keys = dict_tsnos.keys()
    date = str(time.strftime("%Y-%m-%d", time.localtime()))
    params['date'] = date
    if type(tsno)==str:tsno =[tsno]
    site_name=''
    for _ in tsno:
        # strs =''
        for k in keys:
            print(dict_tsnos[k],_)
            if dict_tsnos[k]==_:
                site_name =k
                break
        params['tsNo']=_
        res = requests.get(url,params=params,headers={'Authorization':token},verify= False)
        values = json.loads(res.content)['content']
        yctj,cxyz,cxcllx,cxclbl = 0 ,0,0,0
        if not ('licenseType' in values.keys()):
            yctj =0
            date = date
        else:
            yctj = values['licenseType']['total']
            date = values['licenseType']['recordDateStr']
        cxyzs = [values['exceed']['coCount'],values['exceed']['hcCount'],values['exceed']['limitCount'],values['exceed']['noCount'],values['exceed']['smokeCount']]
        cxyz =any(cxyzs)
        cxyzs = list(map(lambda x:str(x),cxyzs))
        print(cxyzs)
        v = values['overrunCar']
        _car =[v['bigBusCount'],v['bigTruckCount'],v['busCount'],v['carCount'],v['truckCount'],v['suvCount'],v['pickUpCount'],v['unknownCount'],v['minibusCount']]
        cxcllx = any(_car)
        _car =list(map(lambda x:str(x),_car))

        cxclbl = v['nativeCount']+v['inProvinceCount']+v['nonLocalCount']
        is_ok = all([yctj,cxyz,cxcllx,cxclbl])

        if (is_ok):strss +=site_name+' 该站点遥测月统计数据<font  color="black"><b>正常</b></font><br>'+\
            '遥测统计总数:'+str(yctj)+' 超限车辆类型数目依次为:'+','.join(_car)+' 超限车辆比例总数:'+str(cxclbl)+\
            ' 超限因子数目依次为:'+','.join(cxyzs)+'<br>'
        else:strss +=site_name+' 该站点遥测月统计数据<font  color="red"><b>异常</b></font><br>'+\
            '遥测统计总数:'+str(yctj)+' 超限车辆类型数目依次为:'+','.join(_car)+' 超限车辆比例总数:'+str(cxclbl)+\
            ' 超限因子数目依次为:'+','.join(cxyzs)+'<br>'
    return strss


#车流量统计(时日月年)
def car_flow(url,params,tsno,dict_tsnos,token):
    strs = ''
    if type(tsno)==str:tsno = [tsno]
    if 'Hour' in url:
        date = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    else:date = str(time.strftime("%Y-%m-%d", time.localtime()))
    params['date']=date
    print(tsno)
    for _ in tsno:
        site_name = None
        #查找对应键值
        for key in dict_tsnos.keys():
            if dict_tsnos[key]==_:
                site_name = key
                break
        params['tsNo']=_
        print('params:',params)
        res = requests.get(url,params=params,headers={'Authorization':token},verify= False)
        print('url:',res.url)
        res = json.loads(res.content)
        licenseType_total = res['content']['licenseType']['total']
        licenseBelonging_total = res['content']['licenseBelonging']['total']
        vehicalType_total = res['content']['vehicalType']['total']
        print(licenseType_total,licenseBelonging_total,vehicalType_total)
        is_normal = all([licenseType_total,licenseBelonging_total,vehicalType_total])
        if is_normal:strs +=date +'  <font color="red"><b>'+site_name +'</b></font>车流量统计数据正常<br>'+\
            '三种车牌的颜色总数:'+str(licenseType_total)+'<br>'+'车辆归属地总数:'+str(licenseBelonging_total)+'<br>'+\
            '车辆总数:'+str(vehicalType_total)+'<br>'
        else:strs +=date +'  <font color="red"><b>'+site_name +'</b></font>车流量统计数据<b>异常</b><br>'+\
            '三种车牌的颜色总数:'+str(licenseType_total)+'<br>'+'车辆归属地总数:'+str(licenseBelonging_total)+'<br>'+\
            '车辆总数:'+str(vehicalType_total)+'<br>'
    return strs
###---广州---###
def telemetry_data_manerger_gz(url,params,tsno):
    pass
if __name__=='__main__':
    #遥测-Test#
    # strs = air_quality_data_manger()
    # air_quality_statistics_year()
    # print('1232131:',strs)
    pass
