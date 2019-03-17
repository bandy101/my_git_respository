# -*- coding: utf-8 -*-
# 登录验证
prj_name=__name__.split('.')[0]
exec ('from %s.share        import db,ToGBK,HttpResponseCORS,HttpResponseJsonCORS,mValidateUser,ComplexEncoder,host_url,my_urlencode,read_access_token_lw,write_access_token_lw'%prj_name)
exec ('from %s.share        import fs_url,read_access_token,write_access_token,checkSession,data_url,m_sCorpID,m_sCorpSecret,m_sAgentId_lw,m_sCorpSecret_lw,AppId,AppSecret,template_id_msg,template_id_result'%prj_name) 
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

def getMsgList(request):    
    usr_id_qy = request.session.get('usr_id_qy','') or testid
    if usr_id_qy ==0:
        s = """
        {
        "errcode": -1,
        "errmsg": "无权访问,请先关注!"
        }        """
        return HttpResponseJsonCORS(s)
    pageNo =  request.POST.get('pageNo','') or 1
    pageNo=int(pageNo)
    typeID =  request.POST.get('typeID','')
    search =  request.POST.get('search','')
    search = MySQLdb.escape_string(search)
    users = getViewUsers()
    if usr_id_qy not in users:
        data = []
        iTotal_length,iTotal_Page,pageNo,select_size = 0,0,0,10
        L = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)
    else:
        sql="""SELECT MS.id,MS.title,MS.cid,U.usr_name,DP.cname,MT.txt1,MS.ctime
            FROM msg_send MS 
            LEFT JOIN users U ON U.usr_id=MS.cid
            LEFT JOIN dept DP ON DP.id = U.dept_id
            LEFT JOIN mtc_t MT ON MT.id = MS.mtype AND MT.type='XXLB'
            WHERE 1=1 AND MS.is_send = 1
            """
        if typeID !='':
            sql+="AND MS.mtype=%s "%typeID
        if search !='':
            sql+="AND MS.title like '%%%s%%'"%search
        sql+="AND MS.mtype=1 ORDER BY MS.ctime DESC"
        rows,iTotal_length,iTotal_Page,pageNo,select_size = db.select_for_grid(sql,pageNo,10)
        names = 'id title cid usr_name dept_name type_name ctime'.split()
        data = [dict(zip(names, d)) for d in rows]
        L = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)

    s = """
        {
        "errcode": 0,
        "errmsg": "获取信息列表成功",
        "data":%s,
        "totalLength":%s,
        "totalPage":%s,
        "pageNo":%s,
        "pageSize":%s
        }        """%(L,iTotal_length,iTotal_Page,pageNo,select_size)
    # s=ToGBK(s)
    return HttpResponseJsonCORS(s)

def msgDetail(request):  
    usr_id_qy = request.session.get('usr_id_qy','') or testid
    if usr_id_qy ==0:
        s = """
        {
        "errcode": -1,
        "errmsg": "无权访问,请先关注"
        }        """
        return HttpResponseJsonCORS(s)
    pk = request.POST.get('pk','')
    # pk = 72
    if pk =='':
        s = """
        {
        "errcode": -1,
        "errmsg": "无效请求"
        }        """
        return HttpResponseJsonCORS(s)
    
    sql="""SELECT MS.id,MS.title,MS.cid,U.usr_name,DP.cname,MT.txt1,MS.memo,MS.ctime,MS.mtype
        FROM msg_send MS 
        LEFT JOIN users U ON U.usr_id=MS.cid
        LEFT JOIN dept DP ON DP.id = U.dept_id
        LEFT JOIN mtc_t MT ON MT.id = MS.mtype AND MT.type='XXLB'
        WHERE MS.id=%s
        """%pk
    # print sql
    rows,iN=db.select(sql)

    names = 'id title cid usr_name dept_name type_name memo ctime mtype'.split()
    data = [dict(zip(names, d)) for d in rows]
    L = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)
    #L = L.replace('/fs/editor_files','%s/editor_files'%fs_url)

    sql="""SELECT MSL.id,UX.usr_id,UX.headimgurl,UX.usr_name,MSL.jointime,IFNULL(MSL.status,0)
        FROM msg_send_list MSL
        LEFT JOIN users_wx UX ON UX.usr_id = MSL.to_usr_id
        WHERE IFNULL(MSL.isjoin,0)=1 AND MSL.m_id=%s
        ORDER BY MSL.jointime 
        """%pk
    rows,iN=db.select(sql)
    unknown=[] #待审核
    isok=[] #已通过
    notok=[] #不通过
    for e in rows:
        e=list(e)
        if e[5]==0:
            unknown.append(e)
        if e[5]==1:
            isok.append(e)
        if e[5]==2:
            notok.append(e)

    names = 'msl_id usr_id headimgurl usr_name jointime status'.split()
    data0 = [dict(zip(names, d)) for d in unknown]
    L0 = json.dumps(data0,ensure_ascii=False,cls=ComplexEncoder)
    data1 = [dict(zip(names, d)) for d in isok]
    L1 = json.dumps(data1,ensure_ascii=False,cls=ComplexEncoder)
    data2 = [dict(zip(names, d)) for d in notok]
    L2 = json.dumps(data2,ensure_ascii=False,cls=ComplexEncoder)

    if str(usr_id_qy) in ['2576'] :   #固定人员可以审核
        canAudit = 1
    else:
        canAudit = 0
    #print "canAudit=%s"%(canAudit)

    s = """
        {
        "errcode": 0,
        "errmsg": "获取信息详情成功",
        "data":%s,
        "unknown":%s,
        "isok":%s,
        "notok":%s,
        "canAudit":%s
        }        """%(L,L0,L1,L2,canAudit)
    # s=ToGBK(s)

    return HttpResponseJsonCORS(s)

def getViewUsers():
    sql = """select usr_id from users where dept_id in (3,175,76)"""
    rows,iN = db.select(sql)
    users= []
    for e in rows:
        users.append(str(e[0]))

    users.append('2576')
    users.append('627')
    #users.append('2110')
    users.append('26')
    users.append('932')
    return users

def putToubiao(request):  
    usr_id_qy = request.session.get('usr_id_qy','') or testid
    if usr_id_qy ==0:
        s = """
        {
        "errcode": -1,
        "errmsg": "无权访问,请先关注"
        }        """
        return HttpResponseJsonCORS(s)
    msl_id = request.POST.get('msl_id','')
    # msl_id = 5125
    if msl_id =='':
        s = """
        {
        "errcode": -1,
        "errmsg": "无效请求"
        }        """
        return HttpResponseJsonCORS(s)
    status = request.POST.get('status','') or 0
    sql="""UPDATE msg_send_list SET status=%s,stime=now() WHERE id=%s"""%(status,msl_id)
    db.executesql(sql)
    #推送
    sql="""SELECT MS.title,UX.openid,MS.id FROM msg_send_list MSL 
        LEFT JOIN msg_send MS ON MS.id=MSL.m_id
        LEFT JOIN users_wx UX ON UX.usr_id = MSL.to_usr_id
        WHERE MSL.id = %s
        """%msl_id
    rows,iN=db.select(sql)
    errcode = mWxPushMsg_fw(rows[0][0],rows[0][2],rows[0][1])
    s = """
        {
        "errcode": 0,
        "errmsg": "审核成功。",
        "errcode1":"%s"
        }        """%errcode
    # s=ToGBK(s)
    return HttpResponseJsonCORS(s)

import httplib
def mWxPushMsg_fw(title,pk,toUser):   
    now=getToday()
    sToken =  read_access_token()
    conn = httplib.HTTPSConnection('api.weixin.qq.com')  
    sToken = read_access_token()
    if sToken == '':            
        url = "/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s"%(AppId,AppSecret)
        conn.request('GET', '%s'%url)  
        res = conn.getresponse()       
        body = res.read()  
        ddata=json.loads(body)
        sToken = ddata['access_token'] 
        conn.close()  
        write_access_token(body)
    file_id=pk
    sUrl='%s/complaint/login/default?fid=infoDetail&seq=%s&must_reply=true'%(host_url,file_id)
    description = """您参与的%s的劳务招标报名，有新审核信息啦"""%(title)
    surl = my_urlencode(sUrl)
    # print toUser
    description = json.dumps(description)
    now = json.dumps(now)
    city = json.dumps("深圳")
    url = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_base&state=wx#wechat_redirect"%(AppId,surl)

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
            "value":%s,
            "color":"#173177"
            }

            }
            }
    """%(toUser,template_id_msg,sUrl,description,city,now)
    # print sMsg
    conn = httplib.HTTPSConnection('api.weixin.qq.com')  
    url = "/cgi-bin/message/template/send?access_token=%s"%(sToken)
    #print url
    conn.request('POST', '%s'%url,sMsg)  
    res = conn.getresponse()       
    body = res.read()  
    conn.close()  
    ddata=json.loads(body)
    errcode = ddata['errcode']    
    return errcode

