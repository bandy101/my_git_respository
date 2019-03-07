# -*- coding: utf-8 -*-

import sys
import os,time
import httplib
import urllib
import json
# import pymssql
# sys.path.append("/home/webroot/oWorld/complaint")
# exec ('from share        import ToGBK')
# import MySQLdb
from HW_DB   import DataBaseParent_local,DataBaseParent_byerp,DataBaseParent_bkerp
#本地mysql数据库
local=DataBaseParent_local()  
#主系统MSSQL数据库
byerp = DataBaseParent_byerp()
bkerp = DataBaseParent_bkerp()
uc=unicode(str('s'), 'eucgb2312_cn')

def ToGBK(s):
    try:
        s=str(s.decode("utf-8").encode("GBK"))
    except:
        s=s
    s = s.replace("\n","\r\n")
    return s

if __name__ == "__main__":

    sql="select isnull(max(seq_from_wx),0) from out_proj_tracking where datasource = 2 "
    rows,iN=byerp.select(sql)
    maxID = rows[0][0]
    # print maxID
    L=[]
    sql="""SELECT 
        seq
        ,pid
        ,DATE_FORMAT(stime,'%%Y-%%m-%%d %%H:%%m:%%s')
        ,memo
        ,next
        ,case istj when 1 then 3323 else cid end
        ,DATE_FORMAT(ctime,'%%Y-%%m-%%d %%H:%%m:%%s')
        ,ifnull(status,'NULL')  
        from out_proj_tracking
        where datasource=2 and seq>%s
        """%(maxID)
    # print sql
    rows,iN = local.select(sql)
    if iN>0:
        for e in rows:
            e=list(e)
            if e[3]!='':
                e[3]=ToGBK(e[3])
            if e[4]!='':
                e[4]=ToGBK(e[4])
            L.append(e)
        names = 'seq pid stime memo next cid ctime status'.split()
        data = [dict(zip(names, d)) for d in L]
        dataList = json.dumps(data)
        sToken='Ljdiu74F_A5Sf75ws5d1fE_DFs8d'
        params = urllib.urlencode({'data': dataList,'itype':'tracking','sToken':sToken})  
        headers = {"Content-type": "application/x-www-form-urlencoded" , "Accept": "text/plain"}  
        conn = httplib.HTTPConnection('ww.szby.cn:8088')  
        url = "/byerp/communication"
        conn.request('POST', '%s'%url,params,headers)  
        res = conn.getresponse()       
        body = res.read() 
        print body 
        # conn.close()  
        # ddata=json.loads(body)
        # errcode = ddata['errcode']  
        # print errcode
    else:
        print 'no new data'
    