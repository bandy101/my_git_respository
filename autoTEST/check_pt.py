import requests
from bs4 import BeautifulSoup
import json
import time
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



token = 'bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1bmlxdWVfbmFtZSI6ImRlbW8iLCJwd2QiOiI3MTcyZGE4ZWY1Zjk1NDcwYjQxNWRiZDEwNDg1NjFlYiIsInVzZXJfaWQiOiIzIiwiaXNzIjoicmVzdGFwaXVzZXIiLCJhdWQiOiIwOThmNmJjZDQ2MjFkMzczY2FkZTRlODMyNjI3YjRmNiIsImV4cCI6MTUzNjE5OTY1OCwibmJmIjoxNTM0OTAzNjU4fQ.HdhVhyMJ8ORq1ingSNL4FW_NS17pXx1FVPqlHGwRC_o'
qys = {
    '广清大道(龙塘)':'AQM65-G22W2807',
    '治超站出口':'AQM65-G22W2714',
    '三棵竹一桥(源潭)':'AQM65-G22W2772',
    '清远大道(党校)':'AQM65-G22W2798',
}
params ={
    'cityId' :441800,
    'collectionBeginDate':	'2018-08-22 00:00:00',
    'collectionEndDate'	:'2018-08-22 23:59:59',
    'countyId':	441801,
    'maxCo':'',
    'maxHumidity':'',	
    'maxNo2':'',	
    'maxO3':'',
    'maxPm10':'',	
    'maxPm25':'',	
    'maxSo2':'',	
    'maxTemperature':'',	
    'minCo':'',	
    'minHumidity':'',	
    'minNo2':'',	
    'minO3':'',	
    'minPm10':'',	
    'minPm25':'',	
    'minSo2':'',	
    'minTemperature':'',
    'pageNum':1,
    'pageSize':12,
    'provinceId':440000,
    'tsNo':''
}
#--空气质量--#
def air_quality():
    ##--清远--#
    url ='http://202.105.10.126:8055/api/v1/monitorAirQualityInfo?provinceId=440000&cityId=441800'
    res = requests.get(url,params={},headers={'Authorization':token},timeout=6000,verify= False)
    values = json.loads(res.content)['content']
    #异常列表
    exe = []
    # print(values)
    strs =''
    for v in values:
        if v['pm25']>PM25:
            strs +=v['name']+' PM2.5:'+str(v['pm25'])+'  数据异常'+'\n'
        if v['pm10']>PM10:
            strs +=v['name']+' PM10:'+str(v['pm10'])+'  数据异常'+'\n'    
        if v['o3']>O3:
            strs +=v['name']+' O3:'+str(v['o3'])+'  数据异常'+'\n'
        if v['so2']>SO2:
            strs +=v['name']+' SO2:'+str(v['so2'])+'  数据异常'+'\n'
        if v['co']>CO:
            strs +=v['name']+' CO:'+str(v['co'])+'  数据异常'+'\n'
        if v['no2']>NO2:
            strs +=v['name']+' NO2:'+str(v['no2'])+'  数据异常'+'\n'
    print(strs)

#--空气质量数据管理--#
def air_quality_data_manger():
    strs =''
    ps = params
    keys = qys.keys()
    url = 'http://202.105.10.126:8055/api/v1/airQualityPageQuery'
    for k in keys:
        ps['tsNo'] = qys[k]
        # print(k)
        res = requests.get(url,params=ps,headers={'Authorization':token},timeout=6000,verify= False)
        values = json.loads(res.content)['content']
        lists = values['list']
        interval = -int(str(lists[0]['collectionDate'])[0:10]) +int(time.time())

        # print(interval//60)
        if (interval//60>18):
            strs +=k + ' 该站点数据异常 '+lists[0]['collectionDateStr']+' 后无空气质量数据\n'
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
            strs +=k + ' 该站点数据异常'+'\n'
    print(strs)

#--空气质量统计--#
def air_quality_statistics():
    keys = qys.keys()
    strs =''
    for k in keys:
        date = time.strftime("%Y-%m-%d", time.localtime())
        url = 'http://202.105.10.126:8055/api/v1/airReportDay?provinceId=440000&cityId=441800&countyId=441801&tsNo='+qys[k]+'&date='+date+''
        res = requests.get(url,headers={'Authorization':token},timeout=6000,verify= False)
        values = json.loads(res.content)['content']
        if not values:
            strs +=k ' 站点空气质量日统计报表数据异常'

#--遥测--#
def telemetry_data_manage():
    pass

def telemetry_

if __name__=='__main__':
    #遥测-Test#
