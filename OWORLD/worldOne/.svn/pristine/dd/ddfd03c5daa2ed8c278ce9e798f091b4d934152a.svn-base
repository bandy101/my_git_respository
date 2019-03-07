# -*- coding: utf-8 -*-
# 登录验证
prj_name=__name__.split('.')[0]
exec ('from %s.share        import db,ToGBK,HttpResponseCORS,HttpResponseJsonCORS,mValidateUser,ComplexEncoder,host_url,my_urlencode,read_access_token_common,write_access_token_common'%prj_name)
exec ('from %s.share        import read_access_token,write_access_token,checkSession,data_url,m_sCorpID,m_sCorpSecret,m_sAgentId_gy,m_sCorpSecret_gy,AppId_gy,AppSecret_gy,template_id_msg_gy,template_id_result_gy'%prj_name) 
import httplib
import sys  
import os
import time
import json
import random
from django.http import HttpResponseRedirect,HttpResponse
import datetime
from HW_DT_TOOL                 import getToday
import MySQLdb
testid = 0
from multiprocessing import Process

data_url = 'https://lw.szby.cn/complaint/gy'
front_url = 'https://lw.szby.cn/attach/mat_souring'

def getAuditor(request):
    usr_id_qy = request.session.get('usr_id_qy','') or testid
    if usr_id_qy ==0 :
        s = """
        {
        "errcode": -1,
        "errmsg": "无权访问"
        }        """
        return HttpResponseJsonCORS(s)
    sql="""select usr_id,usr_name from mat_souring_auditor
        """
    # print sql 
    rows,iN = db.select(sql)
    names = 'usr_id usr_name'.split()
    data = [dict(zip(names, d)) for d in rows]
    L = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)

    s = """
        {
        "errcode": 0,
        "errmsg": "获取审核人员成功",
        "data":%s
        }        """%(L)
    # s=ToGBK(s)
    # print s
    return HttpResponseJsonCORS(s)

def getMyProjList(request):
    usr_id_qy = request.session.get('usr_id_qy','') or testid
    search = request.POST.get('search','')
    situation = request.POST.get('situation','')
    search = MySQLdb.escape_string(search)
    if usr_id_qy ==0 :
        s = """
        {
        "errcode": -1,
        "errmsg": "无权访问"
        }        """
        return HttpResponseJsonCORS(s)
    pageNo =  request.POST.get('pageNo') or 1
    pageNo=int(pageNo)
    sql="""select distinct op.id,op.cname,op.gc_no,op.addr from out_proj op
           left join proj_user pu on op.id = pu.proj_id
           where pu.usr_id = %s
        """%(usr_id_qy)
    if search !='':
        sql+="AND (concat(IFNULL(OP.cname,''),' ',IFNULL(OP.gc_no,'')) LIKE '%%%s%%' )"%(search)
    sql+="ORDER BY OP.id DESC"
    # print sql 
    rows,iTotal_length,iTotal_Page,pageNo,select_size = db.select_for_grid(sql,pageNo,10)
    dataList=[]
    for e in rows:
        e=list(e)
        dataList.append(e)
    names = 'proj_id cname gc_no proj_addr'.split()
    data = [dict(zip(names, d)) for d in dataList]
    L = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)

    s = """
        {
        "errcode": 0,
        "errmsg": "获取项目列表成功",
        "data":%s,
        "totalLength":%s,
        "totalPage":%s,
        "pageNo":%s,
        "pageSize":%s
        }        """%(L,iTotal_length,iTotal_Page,pageNo,select_size)
    # s=ToGBK(s)
    # print s
    return HttpResponseJsonCORS(s)

def getMatSouring(request):
    usr_id_qy = request.session.get('usr_id_qy','') or testid
    mode = request.POST.get('mode','add') 
    if usr_id_qy ==0 and mode != 'view_fw':
        s = """
        {
        "errcode": -1,
        "errmsg": "无权访问"
        }        """
        return HttpResponseJsonCORS(s)
    id = request.POST.get('id','')

    if mode == 'add':
        L3 = ['cid','random_no']
        names = 'cid random_no'.split()
        random_no = "%s_%s"%(time.time(),usr_id_qy)
        L3[0] = usr_id_qy
        L3[1] = random_no
        data = dict(zip(names, L3))
        L = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)
    elif mode == 'view_fw':
        sql="""select id,mat_name,audit_usr_id,audit_usr_name,proj_id,proj_name,proj_no,proj_addr
                 ,quantity,supply_date,suppliers,contacts,tel,memo,cid,cusrname,date_format(audit_time,'%%Y-%%m-%%d %%T')
                 ,status,random_no,(audit_usr_id = %s and status=1),30 - DATEDIFF(now(),audit_time),''
               from mat_souring
               where id = %s
            """%(usr_id_qy,id)
        print sql 
        rows,iN = db.select(sql)
        L3 = list(rows[0])
        id = L3[0]
        random_no = L3[-4]
        sql="SELECT ifnull(fname,''),'','',file_size,ctime,is_pic,title,cid  FROM suppliers_pic WHERE random_no = '%s' and file_type=7"%(random_no)
        print sql
        lT1,iN1=db.select(sql)
        L2 = []
        for e1 in lT1:
            L1=list(e1)
            fname = e1[0]
            cid = e1[7]
            L1[0] = os.path.join(front_url,str(cid),fname)
            L1[1] = os.path.join(front_url,str(cid),'thumbnail',fname)
            L1[2] = "%s/sign_up/del_attach_file/?fname=%s"%(data_url,fname)
            L2.append(L1)
        names = "url thumbnail delete_url file_size ctime is_pic title".split()
        L3[-1] = [dict(zip(names, d)) for d in L2]
        names = "id mat_name audit_usr_id audit_usr_name proj_id proj_name proj_no proj_addr quantity supply_date suppliers contacts tel memo cid cusrname ctime status random_no btn remaining_days attach".split()
        data = dict(zip(names, L3))
        L = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)
    else:
        sql="""select id,mat_name,audit_usr_id,audit_usr_name,proj_id,proj_name,proj_no,proj_addr 
                 ,quantity,supply_date,suppliers,contacts,tel,memo,cid,cusrname,date_format(ifnull(utime,ctime),'%%Y-%%m-%%d %%T')
                 ,status,random_no,(audit_usr_id = %s and status=1),30 - DATEDIFF(now(),audit_time),''
               from mat_souring
               where id = %s
            """%(usr_id_qy,id)
        print sql 
        rows,iN = db.select(sql)
        L3 = list(rows[0])
        id = L3[0]
        random_no = L3[-4]
        sql="SELECT ifnull(fname,''),'','',file_size,ctime,is_pic,title,cid  FROM suppliers_pic WHERE random_no = '%s' and file_type=7"%(random_no)
        print sql
        lT1,iN1=db.select(sql)
        L2 = []
        for e1 in lT1:
            L1=list(e1)
            fname = e1[0]
            cid = e1[7]
            L1[0] = os.path.join(front_url,str(cid),fname)
            L1[1] = os.path.join(front_url,str(cid),'thumbnail',fname)
            L1[2] = "%s/sign_up/del_attach_file/?fname=%s"%(data_url,fname)
            L2.append(L1)
        names = "url thumbnail delete_url file_size ctime is_pic title".split()
        L3[-1] = [dict(zip(names, d)) for d in L2]
        names = "id mat_name audit_usr_id audit_usr_name proj_id proj_name proj_no proj_addr quantity supply_date suppliers contacts tel memo cid cusrname ctime status random_no btn remaining_days attach".split()
        data = dict(zip(names, L3))
        L = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)

    s = """
        {
        "errcode": 0,
        "errmsg": "获取材料寻源信息成功",
        "data":%s
        }        """%(L)
    # s=ToGBK(s)
    # print s
    return HttpResponseJsonCORS(s)

def saveMatSouring(request):
    print request.POST
    usr_id_qy = request.session.get('usr_id_qy','') or testid
    if usr_id_qy ==0 :
        s = """
        {
        "errcode": -1,
        "errmsg": "无权访问"
        }        """
        return HttpResponseJsonCORS(s)

    id = request.POST.get('id','')
    status = request.POST.get('status','')
    proj_id = request.POST.get('projectName[value]','')
    proj_name = request.POST.get('projectName[text]','')
    proj_no = request.POST.get('projectName[projNo]','')
    proj_addr = request.POST.get('proj_addr','')
    audit_usr_id = request.POST.get('managerResult[value]','')
    audit_usr_name = request.POST.get('managerResult[text]','')
    memo = request.POST.get('memo','')
    linkman = request.POST.get('linkman','')
    linkphone = request.POST.get('linkphone','')
    supply_date = request.POST.get('m_date','')
    quantity = request.POST.get('m_amount','')
    gy_limit = request.POST.get('gy_limit','')
    random_no = request.POST.get('random_no','')
    m_name = request.POST.get('m_name','')

    if id != '':        
        sql = """update mat_souring set proj_id=%s, proj_name='%s', proj_no='%s', proj_addr='%s',audit_usr_id='%s', audit_usr_name='%s', mat_name='%s'
                    ,quantity='%s', supply_date='%s', suppliers='%s', contacts='%s', tel='%s', memo='%s', utime=now(), status=%s
                 where id = %s
              """%(proj_id,proj_name,proj_no,proj_addr,audit_usr_id,audit_usr_name,m_name
                    ,quantity,supply_date,gy_limit,linkman,linkphone,memo,status,id)
        print ToGBK(sql)
        db.executesql(sql)
    else:
        sql = """INSERT INTO mat_souring (proj_id, proj_name, proj_no,proj_addr, audit_usr_id, audit_usr_name, mat_name
                    ,quantity, supply_date, suppliers, contacts, tel, memo, cid, ctime, status, random_no) 
                 VALUES (%s, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', now(), %s, '%s');
              """%(proj_id,proj_name,proj_no,proj_addr,audit_usr_id,audit_usr_name,m_name
                    ,quantity,supply_date,gy_limit,linkman,linkphone,memo,usr_id_qy,status,random_no)
        print ToGBK(sql)
        db.executesql(sql)
        sql = "select id from mat_souring where random_no='%s'"%(random_no)
        lT,iN=db.select(sql)
        id = lT[0][0]

    sql = "update suppliers_pic set m_id=%s where random_no='%s' and file_type=7"%(id,random_no)
    db.executesql(sql)

    sql = "update mat_souring m,users u set m.cusrname=u.usr_name where m.cid=u.usr_id and m.random_no='%s'"%(random_no)
    db.executesql(sql)

    if int(status) == 1:
        mWxPushMsg_audit(request,id)
    s = """
        {
        "errcode": 0,
        "errmsg": "保存材料寻源信息成功"
        }        """
    # s=ToGBK(s)
    # print s
    return HttpResponseJsonCORS(s)

def auditMatSouring(request):
    print request.POST
    usr_id_qy = request.session.get('usr_id_qy','') or testid
    if usr_id_qy ==0 :
        s = """
        {
        "errcode": -1,
        "errmsg": "无权访问"
        }        """
        return HttpResponseJsonCORS(s)
    id = request.POST.get('id','')
    status = request.POST.get('status','')
    audit_memo = request.POST.get('memo','')

    sql = """update mat_souring set audit_memo='%s', audit_time=now(), status=%s
                 where id = %s
              """%(audit_memo,status,id)
    print ToGBK(sql)
    db.executesql(sql)

    if int(status) == -1:
        mWxPushMsg_cancel(request,id)
    if int(status) == 2:
        mWxPushMsg_gzh(request,id)

    s = """
        {
        "errcode": 0,
        "errmsg": "保存材料寻源信息成功"
        }        """
    # s=ToGBK(s)
    # print s
    return HttpResponseJsonCORS(s)

def deleteMatSouring(request):
    usr_id_qy = request.session.get('usr_id_qy','') or testid
    if usr_id_qy ==0 :
        s = """
        {
        "errcode": -1,
        "errmsg": "无权访问"
        }        """
        return HttpResponseJsonCORS(s)
    id = request.POST.get('id','')

    sql = """delete from mat_souring where id = %s
              """%(id)
    db.executesql(sql)

    s = """
        {
        "errcode": 0,
        "errmsg": "删除材料寻源信息成功"
        }        """
    # s=ToGBK(s)
    # print s
    return HttpResponseJsonCORS(s)

def getMatSouringList(request):
    usr_id_qy = request.session.get('usr_id_qy','') or testid
    print usr_id_qy
    search = request.POST.get('search','')
    situation = request.POST.get('situation','')
    search = MySQLdb.escape_string(search)
    type = request.POST.get('type','my')
    if type in ['my','audit']: 
        if usr_id_qy ==0 :
            s = """
            {
            "errcode": -1,
            "errmsg": "无权访问"
            }        """
            return HttpResponseJsonCORS(s)
    pageNo =  request.POST.get('pageNo') or 1
    pageNo=int(pageNo)
    names = 'id mat_name proj_name proj_no ctime cusrname pic status'.split()
    if type == 'my':
        sql="""select m.id,m.mat_name,m.proj_name,m.proj_no,date_format(ifnull(m.utime,m.ctime),'%%Y-%%m-%%d %%T'),m.cusrname,u.pic,m.status
           from mat_souring m
           left join users u on u.usr_id = m.cid
           where m.cid = %s     
        """%(usr_id_qy)
        if search !='':
            sql+="AND (concat(m.mat_name,'||',m.proj_name,'||',m.proj_no) LIKE '%%%s%%' )"%(search)
        if situation !='':
            sql+="AND (m.status='%s' "%(situation)
            sql+=")"
        sql+="ORDER BY m.id DESC"
    elif type == 'audit':
        sql="""select m.id,m.mat_name,m.proj_name,m.proj_no,date_format(ifnull(m.utime,m.ctime),'%%Y-%%m-%%d %%T'),m.cusrname,u.pic,m.status
           from mat_souring m
           left join users u on u.usr_id = m.cid
           where m.audit_usr_id = %s  and m.status != 0    
        """%(usr_id_qy)
        if search !='':
            sql+="AND (concat(m.mat_name,'||',m.proj_name,'||',m.proj_no) LIKE '%%%s%%' )"%(search)
        if situation !='':
            sql+="AND (m.status='%s' "%(situation)
            sql+=")"
        sql+="ORDER BY m.id DESC"
    else:
        sql="""select m.id,m.mat_name,date_format(m.audit_time,'%Y-%m-%d %T'),m.cusrname,u.pic,DATEDIFF(now(),m.audit_time)<=30
           from mat_souring m
           left join users u on u.usr_id = m.cid
           where m.status=2  
        """
        if search !='':
            sql+="AND (m.mat_name LIKE '%%%s%%' )"%(search)
        if situation !='':
            sql+="AND (DATEDIFF(now(),m.audit_time)<=30)=%s "%(situation)
        sql+="ORDER BY m.id DESC"

        names = 'id mat_name ctime cusrname pic status'.split()
    print sql 
    rows,iTotal_length,iTotal_Page,pageNo,select_size = db.select_for_grid(sql,pageNo,10)
    dataList=[]
    for e in rows:
        e=list(e)
        dataList.append(e)
    data = [dict(zip(names, d)) for d in dataList]
    L = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)

    s = """
        {
        "errcode": 0,
        "errmsg": "获取材料寻源信息列表成功",
        "data":%s,
        "totalLength":%s,
        "totalPage":%s,
        "pageNo":%s,
        "pageSize":%s
        }        """%(L,iTotal_length,iTotal_Page,pageNo,select_size)
    print ToGBK(s)
    return HttpResponseJsonCORS(s)

#企业号信息推送
import httplib
def mWxPushMsg_audit(request,id):   
    L =Get_data_audit(id)
    sToken =  read_access_token_common('access_token_gy_qy')
    if sToken == '':
        conn = httplib.HTTPSConnection('qyapi.weixin.qq.com')  
        url = "/cgi-bin/gettoken?corpid=%s&corpsecret=%s"%(m_sCorpID,m_sCorpSecret_gy)
        conn.request('GET', '%s'%url)  
        res = conn.getresponse()       
        body = res.read()  
        ddata=json.loads(body)
        sToken = ddata['access_token'] 
        conn.close()  
        write_access_token_common(body,'access_token_gy_qy')
    toUser = L[0]
    toUser += '|liusq'   
    sUrl='%s/complaint/login/login_qy?fid=materialDetail_qy&path=material&func_id=1000004&seq=%s'%(host_url,id)
    stitle = """材料寻源审核提醒"""
    description = """材料名称:%s\r\n寻源项目:%s\r\n发送人:%s\r\n发送时间:%s"""%(L[1],L[2],L[3],L[4])
    # print toUser
    stitle=json.dumps(stitle)
    description = json.dumps(description)
    sMsg ="""{
              "touser": "%s",
                     """%(toUser)
    sMsg +="""       "msgtype": "news",
       "agentid": "%s",
       "news": {
           "articles":[
               {
                   "title": %s,
                   "url": "%s",
                   "description":%s
               }
           ]
       }
    }

    """%(m_sAgentId_gy,stitle,sUrl,description)
    # print sMsg

    conn = httplib.HTTPSConnection('qyapi.weixin.qq.com')  
    url = "/cgi-bin/message/send?access_token=%s"%(sToken)
    #print url
    conn.request('POST', '%s'%url,sMsg)  

    res = conn.getresponse()       
    body = res.read()  
    conn.close()  

    ddata=json.loads(body)
    errcode = ddata['errcode'] 
    
    return errcode

def Get_data_audit(id):
    sql="""SELECT u.login_id, m.mat_name, m.proj_name, m.cusrname, ifnull(m.utime,m.ctime)
            FROM mat_souring m 
            LEFT JOIN users u on u.usr_id = m.audit_usr_id
            WHERE m.id = %s
            """%(id)
    rows,iN = db.select(sql)
    L=rows[0]
    return L

def mWxPushMsg_cancel(request,id):   
    L =Get_data_cancel(id)
    sToken =  read_access_token_common('access_token_gy_qy')
    if sToken == '':
        conn = httplib.HTTPSConnection('qyapi.weixin.qq.com')  
        url = "/cgi-bin/gettoken?corpid=%s&corpsecret=%s"%(m_sCorpID,m_sCorpSecret_gy)
        conn.request('GET', '%s'%url)  
        res = conn.getresponse()       
        body = res.read()  
        ddata=json.loads(body)
        sToken = ddata['access_token'] 
        conn.close()  
        write_access_token_common(body,'access_token_gy_qy')
    toUser= L[0]
    toUser += '|lishijie|liusq'   
    sUrl='%s/complaint/login/login_qy?fid=materialDetail_qy&path=material&func_id=1000004&seq=%s'%(host_url,id)
    stitle = """材料寻源作废提醒"""
    description = """材料名称:%s\r\n寻源项目:%s\r\n备注:%s,所以此条寻源信息作废。\r\n审核人:%s\r\n审核时间:%s"""%(L[1],L[2],L[3],L[4],L[5])
    # print toUser
    stitle=json.dumps(stitle)
    description = json.dumps(description)
    sMsg ="""{
              "touser": "%s",
                     """%(toUser)
    sMsg +="""       "msgtype": "news",
       "agentid": "%s",
       "news": {
           "articles":[
               {
                   "title": %s,
                   "url": "%s",
                   "description":%s
               }
           ]
       }
    }

    """%(m_sAgentId_gy,stitle,sUrl,description)
    # print sMsg

    conn = httplib.HTTPSConnection('qyapi.weixin.qq.com')  
    url = "/cgi-bin/message/send?access_token=%s"%(sToken)
    #print url
    conn.request('POST', '%s'%url,sMsg)  

    res = conn.getresponse()       
    body = res.read()  
    conn.close()  

    ddata=json.loads(body)
    errcode = ddata['errcode'] 
    
    return errcode

def Get_data_cancel(id):
    sql="""SELECT u.login_id, m.mat_name, m.proj_name, m.audit_memo, m.audit_usr_name, m.audit_time
            FROM mat_souring m 
            LEFT JOIN users u on u.usr_id = m.cid
            WHERE m.id =  %s
            """%(id)
    rows,iN = db.select(sql)
    L=rows[0]
    return L

template_id_result_gy = "7J5iK9tBv3xqwjHRo6r9j6Baq_VOPuxqDDbJPoACK5w"
def mWxPushMsg_gzh(request,id):
    year=getToday()[:4]  
    L =Get_data_gzh(request,id)
    sToken =  read_access_token()
    conn = httplib.HTTPSConnection('api.weixin.qq.com')  
    sToken = read_access_token_common('access_token_gy')
    if sToken == '':            
        url = "/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s"%(AppId_gy,AppSecret_gy)
        conn.request('GET', '%s'%url)  
        res = conn.getresponse()       
        body = res.read()  
        ddata=json.loads(body)
        sToken = ddata['access_token'] 
        conn.close()  
        write_access_token_common(body,'access_token_gy')
    sUrl='%s/lwerp/lw/src/html/material/materialDetail_fw.html?id=%s'%(host_url,id)
    ctime = L[1]
    city = '深圳'
    title = '本次寻源材料:%s'%L[0]
    description = "感谢您的关注,点击查看详情。"
    title = json.dumps(title)
    city = json.dumps(city)
    description = json.dumps(description)

    sMsg ="""{
            "touser":"%s",
            "template_id":"%s",
            "url":"%s",
            "topcolor":"#FF0000",
            "data":{
            "first": {
            "value":%s,
            "color":"#173177"
            },
            "keyword1": {
            "value":%s,
            "color":"#173177"
            },
            "keyword2": {
            "value":"%s",
            "color":"#173177"
            },
            "remark": {
            "value":%s,
            "color":"#173177"
            }            
            }
            }
        """%("JSHnSMSGWQLJD",template_id_result_gy,sUrl,title,city,ctime,description)
    #print ToGBK(sMsg)
    sql = """select u.usr_id,u.openid,ifnull(u.usr_name,'') from users_gy u
             left join mat_souring_push_log p on u.usr_id = p.usr_id and p.m_id = %s
             where ifnull(p.errcode,-1) != 0 
             order by usr_id asc"""%(id)
    rows,iN = db.select(sql)   
    msg1 = sMsg.replace('JSHnSMSGWQLJD',rows[0][1])
    
    p1=Process(target=push,kwargs={'rows':rows,'token':sToken,'msg':sMsg,'id':id,})
    p1.start()
    print(u'主进程',os.getpid(),os.getppid())
    return 


def Get_data_gzh(request,id):
    sql="""SELECT mat_name,audit_time
            FROM mat_souring
            WHERE id = %s
            """%(id)
    rows,iN = db.select(sql)
    L=rows[0]
    return L

from HW_FILE_TOOL           import writeTXT,openTXT
import MySQLdb
def push(rows,token,msg,id):
    log_file=os.path.join('/home/webroot/oWorld/complaint/test1.txt')
    db1 = MySQLdb.connect(host="127.0.0.1",user="root",passwd="24ea8194",db="complaint",charset="utf8")
    for e in rows:
        msg1 = msg.replace('JSHnSMSGWQLJD',e[1])
        conn = httplib.HTTPSConnection('api.weixin.qq.com')  
        url = "/cgi-bin/message/template/send?access_token=%s"%(token)
        #print url
        conn.request('POST', '%s'%url,msg1)  
        res = conn.getresponse()       
        body = res.read()  
        conn.close()  
        ddata=json.loads(body)
        errcode = ddata['errcode']
        errmsg = ddata['errmsg']
        sql = "insert into mat_souring_push_log (m_id,usr_id,usr_name,push_time,errcode,errmsg) values (%s,%s,'%s',now(),%s,'%s')"%(id,e[0],e[2],errcode,errmsg)
        #writeTXT(log_file,sql)
        cur=db1.cursor()
        r = cur.execute(sql)
        db1.commit()
        cur.close()      
        #print body    
    sys.exit(0)
    return

