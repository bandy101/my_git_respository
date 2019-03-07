# -*- coding: utf-8 -*-
# 登录验证
prj_name=__name__.split('.')[0]
exec ('from %s.share        import db,ToUnicode,ToGBK,HttpResponseCORS,HttpResponseJsonCORS,mValidateUser,ComplexEncoder'%prj_name)
exec ('from %s.share        import read_access_token,write_access_token,checkSession,data_url,AppId,AppSecret'%prj_name) 
import httplib
import sys  
import os
import time
import json
import random
import md5
import urllib
from django.http import HttpResponseRedirect,HttpResponse

# testid = 427
testid = 0

def putProj(request):
    usr_id = request.session.get('usr_id','') or testid
    if usr_id ==0:
        s = """
        {
        "errcode": -1,
        "errmsg": "无权访问,请先关注"
        }        """
        return HttpResponseJsonCORS(s)
    proj_id = request.POST.get('proj_id','') or 0
    work_type = request.POST.get('work_type','') or 0
    team_id = request.POST.get('team_id','') or 0
    is_partner = request.POST.get('is_partner','') or 0
    labour_proj_id = request.POST.get('labour_proj_id','')
    partner_id = request.POST.get('partner_id','')
    if str(is_partner)!='0':
        if labour_proj_id=='' or partner_id=='':
            s = """
            {
            "errcode": -1,
            "errmsg": "提交参数不足"
            }        """
            return HttpResponseJsonCORS(s)
        # sql="""SELECT LPP.id FROM labour_proj_partner LPP 
        #     LEFT JOIN labour_proj LP ON LP.id=LPP.labour_proj_id
        #     WHERE EXISTS(select 1 from labour_proj where proj_id=LP.proj_id) AND LPP.partner_id=%s 
        #     AND LP.id=%s """%(partner_id,labour_proj_id)
        sql1="""SELECT LP.id FROM labour_proj LP
            WHERE LP.partner_id=%s AND LP.parent_id=%s """%(partner_id,labour_proj_id)
        rows,iN=db.select(sql1)
        if iN>0:
            s = """
            {
            "errcode": -1,
            "errmsg": "您的伙伴已登记在该项目，不能重复"
            }        """
            return HttpResponseJsonCORS(s)
        # sql="""INSERT INTO labour_proj_partner(labour_proj_id,partner_id,work_type,ctime,cid)
        #        VALUES(%s,%s,%s,now(),%s)
        #         """%(labour_proj_id,partner_id,work_type,usr_id)
        sql2="""SELECT LP.proj_id,LP.teams_id FROM labour_proj LP WHERE LP.id=%s"""%labour_proj_id
        rows2,iN2=db.select(sql2)
        proj_id=rows2[0][0]
        teams_id=rows2[0][1]

        sql="""INSERT INTO labour_proj(parent_id,partner_id,work_type,ctime,cid,proj_id,teams_id)
               VALUES(%s,%s,%s,now(),%s,%s,%s)
                """%(labour_proj_id,partner_id,work_type,usr_id,proj_id,teams_id)
        db.executesql(sql)
        # rows1,iN1=db.select(sql1)
        # new_labour_proj_id=rows1[0][0]
        s1 = """
        {
        "errcode": 0,
        "errmsg": "提交成功",
        "is_partner":1,
        "labour_proj_id":%s,
        "partner_id":%s
        }        """%(labour_proj_id,partner_id)
        return HttpResponseJsonCORS(s1)
    else:
        if work_type==0 :
            s = """
            {
            "errcode": -1,
            "errmsg": "提交参数不足"
            }        """
            return HttpResponseJsonCORS(s)
        sql1="""SELECT id FROM labour_proj WHERE cid=%s AND proj_id=%s"""%(usr_id,proj_id)
        rows,iN=db.select(sql1)
        if iN>0:
            s = """
            {
            "errcode": -1,
            "errmsg": "您已登记该项目，不能重复。"
            }        """
            return HttpResponseJsonCORS(s)
        sql="""INSERT INTO labour_proj(proj_id,teams_id,work_type,ctime,cid)
               VALUES(%s,%s,%s,now(),%s)
                """%(proj_id,team_id,work_type,usr_id)
        db.executesql(sql)
        rows1,iN1=db.select(sql1)
        new_labour_proj_id=rows1[0][0]

        s1 = """
            {
            "errcode": 0,
            "errmsg": "提交成功",
            "is_partner":0,
            "new_labour_proj_id":%s
            }        """%(new_labour_proj_id)
        return HttpResponseJsonCORS(s1)

def getPartnerDetail(request):
    usr_id = request.session.get('usr_id','') or testid
    if usr_id ==0:
        s = """
        {
        "errcode": -1,
        "errmsg": "无权访问,请先关注"
        }        """
        return HttpResponseJsonCORS(s)
    labour_proj_id = request.POST.get('labour_proj_id','')
    if labour_proj_id =='':
        s = """
        {
        "errcode": -1,
        "errmsg": "缺少必要参数"
        }        """
        return HttpResponseJsonCORS(s)
    sql="""SELECT LP.id,OP.gc_no,OP.cname,LP.proj_id FROM labour_proj LP 
        LEFT JOIN out_proj OP ON OP.id=LP.proj_id
        WHERE LP.id=%s AND LP.cid=%s AND IFNULL(LP.parent_id,0)=0 """%(labour_proj_id,usr_id)
    rows,iN=db.select(sql)
    names = 'labour_proj_id gc_no cname'.split()
    data = [dict(zip(names, d)) for d in rows]
    L = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)

    sql="""SELECT IFNULL(P.name,''),IFNULL(P.license,''),IFNULL(P.phone,'') 
        FROM labour_proj LP
        LEFT JOIN labour_partner P ON P.id = LP.partner_id
        WHERE LP.cid=%s AND IFNULL(LP.parent_id,0)=%s """%(usr_id,labour_proj_id)
    rows,iN = db.select(sql)
    tem=[]
    for e in rows:
        e = list(e)
        license = e[1].replace(e[1][6:10],'******',1)
        mobile = e[2].replace(e[2][3:7],'****',1)
        e[1] = license
        e[2] = mobile
        tem.append(e)
    names = 'name license mobile'.split()
    data = [dict(zip(names, d)) for d in tem]
    info = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)
    s = """
        {
        "errcode": 0,
        "errmsg": "获取信息成功",
        "data":%s,
        "partner_list":%s
        }"""%(L,info)
    return HttpResponseJsonCORS(s)


def getSucessInfo(request):
    usr_id = request.session.get('usr_id','') or testid
    if usr_id ==0:
        s = """
        {
        "errcode": -1,
        "errmsg": "无权访问,请先关注"
        }        """
        return HttpResponseJsonCORS(s)
    labour_proj_id = request.POST.get('labour_proj_id','') or 0
    is_partner = request.POST.get('is_partner','') or 0
    partner_id = request.POST.get('partner_id','') or 0
    new_labour_proj_id = request.POST.get('new_labour_proj_id','') or 0
    if str(is_partner)=='1':
        sql="""SELECT U.name,AB.name,OP.gc_no,OP.cname,MT.txt1,1
            FROM labour_proj LP0 
            LEFT JOIN labour_proj LP ON LP.id=LP0.parent_id
            LEFT JOIN out_proj OP ON OP.id=LP.proj_id
            LEFT JOIN addr_book AB ON AB.id=LP.teams_id
            LEFT JOIN mtc_t MT ON MT.id=LP.work_type AND MT.type='WTRADE'
            LEFT JOIN labour_partner U ON U.id=LP.partner_id
            WHERE LP0.parent_id=%s AND LP0.partner_id=%s """%(labour_proj_id,partner_id)
        rows,iN=db.select(sql)
        names = 'name leader_name gc_no proj_name work_type_txt is_partner'.split()
        data = [dict(zip(names, d)) for d in rows]
        L = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)
        s = """
        {
        "errcode": 0,
        "errmsg": "获取信息成功",
        "data":%s
        }        """%L
        return HttpResponseJsonCORS(s)
    else:
        sql="""SELECT U.usr_name,AB.name,OP.gc_no,OP.cname,MT.txt1,0
            FROM labour_proj LP 
            LEFT JOIN users_wx U ON U.usr_id=LP.cid
            LEFT JOIN out_proj OP ON OP.id=LP.proj_id
            LEFT JOIN addr_book AB ON AB.id = LP.teams_id
            LEFT JOIN mtc_t MT ON MT.id=LP.work_type AND MT.type='WTRADE'
            WHERE LP.id=%s
            """%new_labour_proj_id
        rows,iN=db.select(sql)
        names = 'name leader_name gc_no proj_name work_type_txt is_partner'.split()
        data = [dict(zip(names, d)) for d in rows]
        L = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)
        s = """
        {
        "errcode": 0,
        "errmsg": "获取信息成功",
        "data":%s
        }        """%L
        return HttpResponseJsonCORS(s)

#考勤系统通信接口
def generateSign():
    expired = int(time.time()) + 2592000;
    current = int(time.time())
    rdm = random.randint(100000,999999)
    srcStr = 'a=%s&b=%s&k=%s&e=%s&t=%s&r=%s'%(appid,bucket,secret_id,expired,current,rdm)

    SignTmp = hmac.new(secret_key,srcStr,hashlib.sha1).digest()
    Sign = base64.b64encode(SignTmp+srcStr)
    return Sign,expired,current

def getLaborInfo(request):
    projectId = '44030120180813009'
    projectId = '44030120180906001'
    page = 0
    rows_per_page = 10
    body = getLaborInfoFunc(projectId,page,rows_per_page)
    ddata=json.loads(body)
  
    errcode = ddata.get('Ret')   
    if int(errcode) != 0:
         return 'error'
    data = ddata.get('Data')
    total = data.get('total')
    pages = int(total/rows_per_page)+1
    print "pages=%s"%(pages)
    rows = data.get('rows')
    saveRows(rows)
    if pages >= 2:
        for i in (2,pages):
            body = getLaborInfoFunc(projectId,i,rows_per_page)
            ddata=json.loads(body)
            errcode = ddata.get('Ret')   
            if int(errcode) != 0:
                continue
            data = ddata.get('Data')
            rows = data.get('rows')
            saveRows(rows)
    
    return HttpResponseJsonCORS(body)       

def saveRows(rows):
    for e in rows:
        Id = e.get('Id','')
        Name = e.get('Name','')
        MyName = e.get('MyName','')
        DeptName = e.get('DeptName','')
        DeptId = e.get('DeptId','')
        MobilePhoneNumber = e.get('MobilePhoneNumber','')
        EmailAddress = e.get('EmailAddress') or ''
        JobNo = e.get('JobNo','')
        ProjectId = e.get('ProjectId','')
        ProjectName = e.get('ProjectName','')
        IdCode = e.get('IdCode','')
        EmpNativeplace = e.get('EmpNativeplace','')
        WorkTypename = e.get('WorkTypename','')
        EmpCategory = e.get('EmpCategory','')
        JobTypeName = e.get('JobTypeName','')
        JobName = e.get('JobName','')
        EmpCardNum = e.get('EmpCardNum')
        UploadTicwrTime = e.get('UploadTicwrTime') or ''
        if UploadTicwrTime == '':
            UploadTicwrTime = 'NULL'
        else:
            UploadTicwrTime = "'%s'"%(UploadTicwrTime)
        sql = "select id from ticwr_labor_info where id = '%s'"%(Id)
        rows,iN=db.select(sql)
        if iN == 0:
            sql = """insert into ticwr_labor_info 
                    (Id,Name,MyName,DeptName,DeptId,MobilePhoneNumber,EmailAddress,JobNo,ProjectId,ProjectName,IdCode,EmpNativeplace,WorkTypename,EmpCategory,JobTypeName,JobName,EmpCardNum,UploadTicwrTime) 
                    values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',%s)
                """%(Id,Name,MyName,DeptName,DeptId,MobilePhoneNumber,EmailAddress,JobNo,ProjectId,ProjectName,IdCode,EmpNativeplace,WorkTypename,EmpCategory,JobTypeName,JobName,EmpCardNum,UploadTicwrTime) 
            #print ToGBK(sql)
            db.executesql(sql)
        else:
            sql = """update ticwr_labor_info set
                    Name='%s',MyName='%s',DeptName='%s',DeptId='%s',MobilePhoneNumber='%s',EmailAddress='%s',JobNo='%s',ProjectId='%s',ProjectName='%s',IdCode='%s',EmpNativeplace='%s',WorkTypename='%s',EmpCategory='%s',JobTypeName='%s',JobName='%s',EmpCardNum='%s',UploadTicwrTime=%s 
                    where Id = '%s'
                """%(Name,MyName,DeptName,DeptId,MobilePhoneNumber,EmailAddress,JobNo,ProjectId,ProjectName,IdCode,EmpNativeplace,WorkTypename,EmpCategory,JobTypeName,JobName,EmpCardNum,UploadTicwrTime,Id) 
            #print ToGBK(sql)
            db.executesql(sql)
    return

def getLaborInfoFunc(projectId,page=0,rows=10):
    appid = 'baoying'
    md5key = 'l79OWlji3eM7vjzJ'
    timestamp = (int(time.time()))                   
    
    para = dict()   
    para["page"] = str(page)
    para["rows"] = str(rows)
    para["projectId"] = projectId
    para["appid"] = appid
    para["timestamp"] = str(timestamp)

    sign = makeSign(para,md5key)

    para["sign"] = sign

    para_str = ''
    for key in para: 
        para_str += '&' + key+'=' + para[key]

    conn = httplib.HTTPConnection('183.57.47.114:8089')  
    url = "/Ticwr/GetPersonList?" + para_str
    #print url
    conn.request('POST', url,'')  

    res = conn.getresponse()       
    body = res.read()  
    conn.close()  
    return body

def makeSign(para,md5key):
    para1 = sorted(para.items(), key=lambda para:para[0])
    src_str = ''
    #print para1
    for e in para1:
        src_str += "%s%s"%(e[0],e[1])
    src_str += md5key
    #print src_str
    m1 = md5.new()   
    m1.update(src_str)   
    sign = m1.hexdigest() 
    #print sign
    return sign

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

def uploadSafetyEducation(request):
    se_id = 4
    sql = "select Project_ID,'' from ticwr_safety_education where id = %s"%(se_id)
    rows,iN=db.select(sql)
    L = list(rows[0])
    sql = """select person_id,edu_coursename,edu_organization,edu_teacher,edu_addr,edu_time,edu_classhour,edu_content,photo from ticwr_safety_education_list tl
             left join ticwr_safety_education t on t.id = tl.m_id
             where t.id = %s"""%(se_id)    
    rows,iN=db.select(sql)
    safetyeducation_list = "["
    for e in rows:
        safetyeducation_list += """{"person_id":%s,"edu_coursename":%s,"edu_organization":%s,"edu_teacher":%s,"edu_addr":%s,"edu_time":%s,"edu_classhour":%s,"edu_content":%s,"edu_photo":"%s"},"""%(json.dumps(e[0]),json.dumps(e[1]),json.dumps(e[2]),json.dumps(e[3]),json.dumps(e[4]),json.dumps(e[5]),json.dumps(e[6]),json.dumps(e[7]),e[8])
    safetyeducation_list = safetyeducation_list[:-1]
    safetyeducation_list += "]"
    body = """{"Project_ID":"%s","safetyeducation_list":%s}"""%(L[0],safetyeducation_list)
    print ToGBK(body)
    #body = """{"Project_ID":"44030120180906001","safetyeducation_list":[{"person_id":"441523199707057015","edu_coursename":"java","edu_organization":"达内","edu_teacher":"Tom老师","edu_addr":"广东深圳","edu_time":"2018-09-21 08:30:00","edu_classhour":"20","edu_content":"java Spring","photo":"xVmxVbXVVaGN2emswdUJiT0QxU1dienArNFozVi9URn"}]}"""
    #print ToGBK(body)
    #return HttpResponseJsonCORS(body)

    client_serial = 'PL5981E0DD85FE4D808A4097B8A907581D'

    api_secret = '6AE1697EFC774D20866EFFA9FD0A3C10'
    api_key = 'E935101F3BCA4C06AA060559B7E6C192'
    api_version = '1.0'
    timestamp = time.time()                   
    timeArray = time.localtime(timestamp)
    now = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    print now

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
    url = "/CWRService/UploadSafetyEducation?" + para_str
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