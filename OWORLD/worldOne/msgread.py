# -*- coding: utf-8 -*-
# 登录验证
prj_name=__name__.split('.')[0]
exec ('from %s.share        import db,ToGBK,HttpResponseCORS,HttpResponseJsonCORS,mValidateUser,ComplexEncoder,m_sCorpID,m_sCorpSecret,m_sAgentId_lw,m_sCorpSecret_lw'%prj_name)
exec ('from %s.share        import read_access_token,fs_url,write_access_token,checkSession,data_url,host_url,my_urlencode,read_access_token_lw,write_access_token_lw'%prj_name) 
import httplib
import sys  
import os
import time
import json
import random
from django.http import HttpResponseRedirect,HttpResponse
from HW_DT_TOOL                 import getToday

testid = 0
def getMsgList(request):	
    usr_id = request.session.get('usr_id','') or testid
    if usr_id ==0:
        s = """
        {
        "errcode": -1,
        "errmsg": "无权访问,请先关注。"
        }        """
        return HttpResponseJsonCORS(s)
    pageNo =  request.POST.get('pageNo','') or 1
    pageNo=int(pageNo)
    typeID =  request.POST.get('typeID','')

    # sql="""SELECT MS.id,MS.title,MS.cid,U.usr_name,DP.cname,MT.txt1,MS.ctime,0 AS isread
    #     FROM msg_send MS 
    #     LEFT JOIN users U ON U.usr_id=MS.cid
    #     LEFT JOIN dept DP ON DP.id = U.dept_id
    #     LEFT JOIN mtc_t MT ON MT.id = MS.mtype AND MT.type='XXLB'
    #     WHERE 1=1
    #     """
    sql="""SELECT MS.id,MS.title,MS.cid,U.usr_name,DP.cname,MT.txt1,MS.ctime,IFNULL(MSL.isread,0)
        FROM msg_send_list MSL 
        LEFT JOIN msg_send MS ON MS.id = MSL.m_id
        LEFT JOIN users U ON U.usr_id=MS.cid
        LEFT JOIN dept DP ON DP.id = U.dept_id
        LEFT JOIN mtc_t MT ON MT.id = MS.mtype AND MT.type='XXLB'
        WHERE MSL.to_usr_id = %s AND MS.is_send = 1
        """%(usr_id)
    if typeID !='':
        sql+="AND MS.mtype=%s "%typeID
    sql+="ORDER BY MSL.ctime DESC"
    rows,iTotal_length,iTotal_Page,pageNo,select_size = db.select_for_grid(sql,pageNo,10)
    names = 'id title cid usr_name dept_name type_name ctime isread'.split()
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
    usr_id = request.session.get('usr_id','') or testid
    if usr_id ==0:
        s = """
        {
        "errcode": -1,
        "errmsg": "无权访问,请先关注"
        }        """
        return HttpResponseJsonCORS(s)
    dept = 0
    pk = request.POST.get('pk','')
    # pk = 72
    if pk =='':
        s = """
        {
        "errcode": -1,
        "errmsg": "无效请求"
        }        """
        return HttpResponseJsonCORS(s)
    
    sql="""SELECT MS.id,MS.title,MS.cid,U.usr_name,DP.cname,MT.txt1,MS.memo,MS.ctime,IFNULL(MSL.status,0),IFNULL(MSL.isjoin,0),MS.mtype,ux.is_labor
        FROM msg_send MS 
        LEFT JOIN users U ON U.usr_id=MS.cid
        LEFT JOIN dept DP ON DP.id = U.dept_id
        LEFT JOIN mtc_t MT ON MT.id = MS.mtype AND MT.type='XXLB'
        LEFT JOIN msg_send_list MSL ON MSL.m_id = MS.id
        LEFT JOIN users_wx ux ON ux.usr_id = MSL.to_usr_id
        WHERE MS.id=%s AND MSL.to_usr_id=%s
        """%(pk,usr_id) 
    #print sql
    rows,iN=db.select(sql)

    names = 'id title cid usr_name dept_name type_name memo ctime status isjoin mtype is_labor'.split()

    data = [dict(zip(names, d)) for d in rows]
    L = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)
    s = """
        {
        "errcode": 0,
        "errmsg": "获取信息详情成功",
        "data":%s
        }        """%(L)
    #print ToGBK(s)
    # 
    #阅读记录
    sql="""UPDATE msg_send_list SET readtime=now(),isread = 1 WHERE m_id=%s AND to_usr_id = %s AND IFNULL(isread,0)=0"""%(pk,usr_id)
    db.executesql(sql)
    return HttpResponseJsonCORS(s)

def joinToubiao(request):  
    usr_id = request.session.get('usr_id','') or testid
    if usr_id ==0:
        s = """
        {
        "errcode": -1,
        "errmsg": "无权访问,请先关注"
        }        """
        return HttpResponseJsonCORS(s)
    pk = request.POST.get('pk','')
    if pk =='':
        s = """
        {
        "errcode": -1,
        "errmsg": "无效请求"
        }        """
        return HttpResponseJsonCORS(s)
    sql="""SELECT status FROM users_wx WHERE usr_id = %s """%usr_id
    rows,iN=db.select(sql)
    if rows[0][0] !=1:
        s = """
        {
        "errcode": -2,
        "errmsg": "未绑定，不能参与投标"
        }        """
        return HttpResponseJsonCORS(s)

    sql="""UPDATE msg_send_list SET isjoin=1,jointime=now() WHERE m_id=%s AND to_usr_id=%s """%(pk,usr_id)
    db.executesql(sql)
    mWxPushMsg_NewJoin(request,pk)
    s = """
        {
        "errcode": 0,
        "errmsg": "提交投标申请成功"
        }        """
    return HttpResponseJsonCORS(s)

import httplib

def mWxPushMsg_NewJoin(request,pk):   
    year=getToday()[:4]  
    sql="""SELECT title FROM msg_send WHERE id = %s"""%pk
    rows,iN=db.select(sql)
    msgTitle=rows[0][0]

    sToken =  read_access_token_lw()
    if sToken == '':
        conn = httplib.HTTPSConnection('qyapi.weixin.qq.com')  
        url = "/cgi-bin/gettoken?corpid=%s&corpsecret=%s"%(m_sCorpID,m_sCorpSecret_lw)
        conn.request('GET', '%s'%url)  
        res = conn.getresponse()       
        body = res.read()  
        ddata=json.loads(body)
        sToken = ddata['access_token'] 
        conn.close()  
        write_access_token_lw(body)
    toUser = 'wuxx'
    sUrl='%s/complaint/login/login_qy?fid=infoDetail&seq=%s&must_reply=true'%(host_url,pk)
    stitle = """劳务招标新投标信息"""
    surl = my_urlencode(sUrl)
    description = """您发布的%s，有新投标报名信息啦。"""%(msgTitle)
    stitle=json.dumps(stitle)
    description = json.dumps(description)
    url = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_base&state=wx#wechat_redirect"%(m_sCorpID,surl)
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

    """%(m_sAgentId_lw,stitle,url,description)
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
    return HttpResponseCORS(request,errcode)
