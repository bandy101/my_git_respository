# -*- coding: utf-8 -*-
# 保存列表数据
prj_name=__name__.split('.')[0]
exec ('from %s.share        import db,ToGBK,m_prjname,HttpResponseCORS'%prj_name) 
import MySQLdb
import httplib
import sys  
import os
import time
import json
import random
import md5
import urllib
from multiprocessing import Process

def uploadSE(request):
    data =  request.POST.get('data','')
    data_list = json.loads(data)
    #print data_list
    pk =  data_list.get('pk','')
    sql = "select count(1) from ticwr_safety_education_list where m_id = %s"%(pk)
    rows,iN=db.select(sql)
    users = rows[0][0]
    sql = "update ticwr_safety_education set user_count=%s where id=%s"%(users,pk)
    db.executesql(sql)

    sql = """select ifnull(op.ticwr_proj_no,''),ifnull(op.ticwr_id,'') from ticwr_safety_education se
             left join out_proj op on op.id = se.proj_id
             where se.id = %s"""%(pk)
    rows,iN=db.select(sql)
    if iN ==0 or rows[0][0]=='' or rows[0][1]=='' :
        s = """
        {
        "errcode": 0,
        "errmsg": "项目未设置两制平台同步信息，无法上传！",
        "pk":%s
        }
        """%(pk)
        return HttpResponseCORS(request,s)
         

    p1=Process(target=uploadSafetyEducation,kwargs={'pk':pk,})
    p1.start()

    s = """
        {
        "errcode": 0,
        "errmsg": "后台上传中，上传结果请刷新页面查看！",
        "pk":%s
        }
        """%(pk)
    return HttpResponseCORS(request,s)

def uploadHT(request):
    print request.POST
    data =  request.POST.get('data','')
    data_list = json.loads(data)
    #print data_list
    pk =  data_list.get('pk','')

    s = """
        {
        "errcode": 0,
        "errmsg": "后台上传中，上传结果请刷新页面查看！",
        "pk":%s
        }
        """%(pk)
    return HttpResponseCORS(request,s)

#实名制平台接口
def getCompanyType(request):
    client_serial = 'PL5981E0DD85FE4D808A4097B8A907581D'

    api_secret = '6AE1697EFC774D20866EFFA9FD0A3C10'
    api_key = 'E935101F3BCA4C06AA060559B7E6C192'
    api_version = '1.0'
    timestamp = time.time()                   
    timeArray = time.localtime(timestamp)
    now = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    print now

    body = '{}'

    para = dict()   
    para["api_key"] = api_key
    para["api_version"] = api_version
    para["client_serial"] = client_serial
    para["timestamp"] = now
    para["body"] = body

    sign = makeSignCwr(para,api_secret)

    para["signature"] = sign

    para_str = 'api_key=%s'%(api_key)
    para_str += '&api_version=' + api_version
    para_str += '&client_serial=' + client_serial
    para_str += '&timestamp=' + urllib.quote(now)
    para_str += '&signature=' + sign

    conn = httplib.HTTPConnection('139.159.225.45:7040')  
    url = "/CWRService/GetCompanyType?" + para_str
    print url
    conn.request('POST', url,body)  

    res = conn.getresponse()       
    body = res.read()  
    conn.close()  

    print body
    ddata=json.loads(body)
    errcode = ddata.get('code')   
    data = ddata.get('result_data')
    #for e in rows:
    #    print e
    return HttpResponseJsonCORS(body)

def uploadSafetyEducation(pk):
    local=DataBaseParent_local()  

    sql = """select tp.url,op.api_key,op.api_secret,op.client_serial from ticwr_safety_education se
             left join out_proj op on op.id = se.proj_id
             left join ticwr_platform tp on tp.id = op.ticwr_id
             where se.id = %s"""%(pk)
    rows,iN=local.select(sql)

    client_serial = rows[0][3]
    api_secret = rows[0][2]
    api_key = rows[0][1]
    http_addr = rows[0][0]
    api_version = '1.0'

    sql = """select person_id,edu_coursename,edu_organization,edu_teacher,edu_addr,edu_time,edu_classhour,edu_content,photo,Project_ID from ticwr_safety_education_list tl
             left join ticwr_safety_education t on t.id = tl.m_id
             where t.id = %s"""%(pk)    
    rows,iN=local.select(sql)
    for e in rows:
        safetyeducation_list = "["
        safetyeducation_list += """{"person_id":%s,"edu_coursename":%s,"edu_organization":%s,"edu_teacher":%s,"edu_addr":%s,"edu_time":%s,"edu_classhour":%s,"edu_content":%s,"edu_photo":"%s"}]"""%(json.dumps(e[0]),json.dumps(e[1]),json.dumps(e[2]),json.dumps(e[3]),json.dumps(e[4]),json.dumps(e[5]),json.dumps(e[6]),json.dumps(e[7]),e[8])
        body = """{"Project_ID":"%s","safetyeducation_list":%s}"""%(e[-1],safetyeducation_list)
        print ToGBK(body)
        timestamp = time.time()                   
        timeArray = time.localtime(timestamp)
        now = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)

        para = dict()   
        para["api_key"] = api_key
        para["api_version"] = api_version
        para["client_serial"] = client_serial
        para["timestamp"] = now
        para["body"] = body

        sign = makeSignCwr(para,api_secret)

        para["signature"] = sign
    
        para_str = 'api_key=%s'%(api_key)
        para_str += '&api_version=' + api_version
        para_str += '&client_serial=' + client_serial
        para_str += '&timestamp=' + urllib.quote(now)
        para_str += '&signature=' + sign
    
        print http_addr
        conn = httplib.HTTPConnection(http_addr)  
        url = "/CWRService/UploadSafetyEducation?" + para_str
        conn.request('POST',url,body)  
    
        res = conn.getresponse()       
        body = res.read()  
        conn.close()  
    
        print body
        ddata=json.loads(body)
        errcode = ddata.get('code')   
        data = ddata.get('result_data')
    sys.exit(0)
    return 

def makeSignCwr(para,md5key):
    para1 = sorted(para.items(), key=lambda para:para[0])
    src_str = md5key
    #print para1
    for e in para1:
        src_str += "%s%s"%(e[0],e[1])
    src_str += md5key
    m1 = md5.new()   
    m1.update(src_str)   
    sign = m1.hexdigest() 
    #print sign
    sign = sign.upper()
    return sign

db_local = MySQLdb.connect(host="127.0.0.1",user="root",passwd="24ea8194",db="complaint",charset="utf8")
class DataBaseParent_local:
    def __init__(self):
        self.cursor="Initial Status"
        self.cursor=db_local.cursor()
        if self.cursor=="Initial Status":
            raise Exception("Can't connect to Database server!")

    def select(self,sqlstr):
        cur=db_local.cursor()
        cur.execute(sqlstr)
        List=cur.fetchall()
        iTotal_length=len(List)
        self.description=cur.description
        cur.close()
        return List,iTotal_length

    def select_include_name(self,sqlstr):
        #选择结果包含List,iTotal_length,lFieldName
        #return list(self.select(sqlstr))+[self.description]
        cur=db_local.cursor()
        cur.execute(sqlstr)
        index = cur.description
        List=cur.fetchall()
        iTotal_length=len(List)
        result = []
        for res in List:
            row = {}
            for i in range(len(index)-1):
                row[index[i][0]] = res[i]
            result.append(row)
        cur.close()
        return result,iTotal_length

    def select_for_grid(self,sqlstr,pageNo=1,select_size=10):
        List,iTotal_length=self.select(sqlstr)
        if iTotal_length%select_size==0:
            iTotal_Page=iTotal_length/select_size
        else:
            iTotal_Page=iTotal_length/select_size+1

        start,end=(pageNo-1)*select_size,pageNo*select_size
        if end>=iTotal_length:end=iTotal_length        
        if iTotal_length==0 or start>iTotal_length or start<0:
            return [],iTotal_length,iTotal_Page,pageNo,select_size
        
        return List[start:end],iTotal_length,iTotal_Page,pageNo,select_size

    def executesql(self,sqlstr):
        cur=db_local.cursor()
        r = cur.execute(sqlstr)
        db_local.commit()
        cur.close()        
        return r
        
    def insert(self,sql,param):
        cur=self.cursor
        n = cur.execute(sql,param) 
        db_local.commit()
        cur.close()        
        return n

    def release(self):
        
        return 0
