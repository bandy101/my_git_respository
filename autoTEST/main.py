import requests
import numpy
import os
from os import path
import xlwt
import xlrd
import numpy as np
from xlutils.copy import copy
from openpyxl import Workbook
from openpyxl import load_workbook
from openpyxl.writer.excel import ExcelWriter 
import json
ip = 'http://plat.dev.ts'
version = 'v1'
prex = ip+'/'+'api/'+version+'/'
global token,paramer,METHOD
paramer = {
'confirmPassword':"demo&123",
'name':"Demo",
'oldPassword':"demo&123",
'password':"demo&123",
'phone':"1592092333",
'remark':"Demos",
'sex':"W"
}

js_pwd ={
    'clientId':'098f6bcd4621d373cade4e832627b4f6',
    'userName':'admin',
    'password':'sfe5188'
    }
def get_token():
    url_login = prex+'login/'
    res = requests.post(url_login,json=js_pwd)
    token = res.json()['content']['token']
    return token
def auto():
    global paramer
    #获取令牌
    token = get_token()
    interface = 'userInfoPageQuery'
    url = prex +interface
    print(url)
    _ = {'pageNum':1,'pageSize':30}
    paramer.update(_)
    print(paramer)
    
    #-----------------------各种提交------------------------#
    print(METHOD)
    if METHOD=='get' or METHOD=='GET':
        res = requests.get(url,params=paramer,headers={'Authorization':'bearer  '+token})
    #res = requests.post(url,json=paramer,headers={'Content-Type':'application/json','Authorization':'bearer  '+token})
    # res = requests.put(url,json=paramer,headers={'Content-Type':'application/json','Authorization':'bearer  '+token})
    print(res.url)
    r = res.json()
    return r,r['errmsg']=='OK',res.headers['Date']
#处理json
def get_info_js():
    global METHOD
    import pymssql
    param = {}
    server,user,password,database = '192.168.20.151','platformuser','Zx123456','PLATFORM_OUTSIDE'

    conn = pymssql.connect(server, user, password, database)
    cursor = conn.cursor()
    c = conn.cursor()
    c.execute("SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME= 'SYS_USER' ")
    rw = c.fetchall()
    names=[]
    for n in rw:
        names.append(n[3])
    cursor.execute("SELECT * FROM SYS_USER ")
    datas =cursor.fetchall()
    fdata= []
    for i in datas:
        fdata.append(list(zip(names,i)))
    # print(dict(fdata[0]))
    cursor.execute('SELECT * FROM  SYS_USER')
    row = cursor.fetchone()
    result = cursor.fetchall()
    
    # value
    with open('cast.json',encoding='utf-8') as files:
        alls = json.load(files)
        itmes = alls['item'][5]['item'][0]
        itm = itmes['item'][0]
        request = itm['request']
        METHOD = request['method']
        query = request['url']['query']
        f_param=[]
        for q in query:
            try:
                value = dict(fdata[0])[q['key'].upper()]
                if value ==None:
                    value=''
                # print('value',value)
                # print(q['key'])
                f_param.append((q['key'],value))
                # print(x)
                # param.update()
            except:
                pass
            # print (q['key'])]
    d_f_param =dict(f_param)
    print(d_f_param['status'])
    # for _ in d_f_param.items():
    #     if _[-1] ==None:
    #         _[-1]=' '
    # print(dict(f_param))
    return dict(f_param)
#写录 xls
def start(index=1,names='text'):
    global paramer
    paramer =get_info_js()
    # print(paramer)
    xls(paramer,index,names=names)
def xls(param,index=1,names ='text'):
    re_json,is_ok,date = auto()
    keys = list(param.keys())
    if index <=1:
        wbk = xlwt.Workbook()
        sheet = wbk.add_sheet('sheet 1')
        #添加表头 bt=false
        for i,d in enumerate(keys):
            sheet.write(0,i,d)
            # print('ax',re_json['content']['list'])
            #添加数据
            try:
                # sheet.write(index,i,param[d])
                sheet.write(index,i,re_json['content']['list'][0][d])
            except:
                try:
                    sheet.write(index,i,re_json['content'][d])
                except:pass
        sheet.write(0,len(keys),'结果')
        sheet.write(0,len(keys)+1,'响应时间')
        sheet.write(index,len(keys)+1,date)
        if is_ok:
            sheet.write(index,len(keys),'成功')
        else:
            sheet.write(index,len(keys),'失败')
        wbk.save(names+'.xls')
    else:
        workbook = xlrd.open_workbook(names+'.xls')
        workbooknew = copy(workbook)
        ws = workbooknew.get_sheet(0)
        for i,d in enumerate(keys):
            try:
                # ws.write(index,i,param[d])
               ws.write(index,i,re_json['content']['list'][0][d])
            except:
                try:
                    ws.write(index,i,re_json['content'][d])
                except:
                    pass
        ws.write(index,len(keys)+1,date)
        if is_ok:
            ws.write(index,len(keys),'成功')
        else: 
            ws.write(index,len(keys),'失败')

        workbooknew.save(names+'.xls')
        return 
if __name__=='__main__':
    # auto()
    start(1,'text')
    # get_info_js()