# -*- coding: utf-8 -*-
# 登录验证
prj_name=__name__.split('.')[0]
exec ('from %s.share        import db,ToGBK,HttpResponseCORS,HttpResponseJsonCORS,mValidateUser,ComplexEncoder,host_url,my_urlencode,imgUrl'%prj_name)
exec ('from %s.share        import fs_url,read_access_token_common,write_access_token_common,checkSession,data_url,m_sCorpID,AppId_gy,AppSecret_gy,template_id_msg_gy'%prj_name) 
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
testid = 2110

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
    pageNo = MySQLdb.escape_string(pageNo)
    pageNo=int(pageNo)
    typeID =  request.POST.get('typeID','')
    search =  request.POST.get('search','')

    search = MySQLdb.escape_string(search)
    typeID = MySQLdb.escape_string(typeID)
    sql="""SELECT MS.id,MS.title,MS.cid,U.usr_name,DP.cname,MT.txt1,MS.ctime
        FROM complaint_sup_msg_send MS 
        LEFT JOIN users U ON U.usr_id=MS.cid
        LEFT JOIN dept DP ON DP.id = U.dept_id
        LEFT JOIN mtc_t MT ON MT.id = MS.mtype AND MT.type='XXFL'
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
    
    sql="""SELECT MS.id,MS.title,MS.cid,U.usr_name,DP.cname,MT.txt1,MS.memo,DATE_FORMAT(MS.ctime,'%%Y-%%m-%%d %%H:%%i:%%s'),MS.cantalk,MS.mtype,IFNULL(MS.has_new,0)
        FROM complaint_sup_msg_send MS 
        LEFT JOIN users U ON U.usr_id=MS.cid
        LEFT JOIN dept DP ON DP.id = U.dept_id
        LEFT JOIN mtc_t MT ON MT.id = MS.mtype AND MT.type='XXFL'
        WHERE MS.id=%s
        """%pk
    # print sql
    rows,iN=db.select(sql)
    has_new=rows[0][10]
    cid = rows[0][2]
    names = 'id title cid usr_name dept_name type_name memo ctime cantalk mtype hasNew'.split()
    data = [dict(zip(names, d)) for d in rows]
    L = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)
    #L = L.replace('/fs/editor_files','%s/editor_files'%fs_url)
    #更新已读状态
    if str(has_new)=='1' and cid==usr_id_qy:
        sql="""UPDATE complaint_sup_msg_send SET has_new=0 WHERE id=%s"""%pk
        db.executesql(sql)

    sql="""SELECT MSL.id,UX.usr_id,UX.headimgurl,UX.usr_name,tb.jointime,IFNULL(tb.status,0),su.cname,tb.memo
        FROM complaint_sup_msg_send_list MSL
        LEFT JOIN users_gy UX ON UX.usr_id = MSL.to_usr_id
        left join addr_book ab on ab.id = ux.addr_id
        left join suppliers su on su.id = ab.sup_id
        left join complaint_sup_toubiao tb on MSL.m_id = tb.m_id and tb.cid = MSL.to_usr_id
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
    sql = """SELECT MSL.id,UX.usr_id,UX.headimgurl,UX.usr_name,tb.jointime,-1,su.cname,msl.memo
        FROM complaint_sup_msg_send_list MSL
        LEFT JOIN users_gy UX ON UX.usr_id = MSL.to_usr_id
        left join addr_book ab on ab.id = ux.addr_id
        left join suppliers su on su.id = ab.sup_id
        left join complaint_sup_toubiao tb on MSL.m_id = tb.m_id and tb.cid = MSL.to_usr_id
        WHERE IFNULL(MSL.isjoin,0)=-1 AND MSL.m_id=%s
        ORDER BY MSL.jointime """%pk
    rows,iN=db.select(sql)
    for e in rows:
        notok.append(e)

    names = 'msl_id usr_id headimgurl usr_name jointime status sup_name cont'.split()
    data0 = [dict(zip(names, d)) for d in unknown]
    L0 = json.dumps(data0,ensure_ascii=False,cls=ComplexEncoder)
    data1 = [dict(zip(names, d)) for d in isok]
    L1 = json.dumps(data1,ensure_ascii=False,cls=ComplexEncoder)
    data2 = [dict(zip(names, d)) for d in notok]
    L2 = json.dumps(data2,ensure_ascii=False,cls=ComplexEncoder)
    
    sql="""SELECT FB.id
        ,CASE FB.itype WHEN 'qy' THEN U.usr_name ELSE UG.usr_name END
        ,CASE FB.itype WHEN 'qy' THEN CONCAT('%s',U.pic) ELSE UG.headimgurl END
        ,FB.memo,DATE_FORMAT(FB.ctime,'%%Y-%%m-%%d %%H:%%i:%%s')
        FROM complaint_sup_msg_feedback FB
        LEFT JOIN users U ON U.usr_id = FB.cid
        LEFT JOIN users_gy UG ON UG.usr_id = FB.cid
        WHERE FB.m_id=%s
        ORDER BY FB.ctime DESC 
        """%(imgUrl,pk)
    rows,iN=db.select(sql)
    names = 'id usr_name pic memo ctime'.split()
    data = [dict(zip(names, d)) for d in rows]
    feedback = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)
    
    users = getAuditUserIds()
    if str(usr_id_qy) in users:   #固定人员可以审核
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
        "feedback":%s,
        "canAudit":%s
        }        """%(L,L0,L1,L2,feedback,canAudit)
    #s=ToGBK(s)
    print ToGBK(s) 
    return HttpResponseJsonCORS(s)

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
    refuse_memo = request.POST.get('refuse_memo','')
    sql="""UPDATE complaint_sup_msg_send_list SET status=%s,stime=now() WHERE id=%s"""%(status,msl_id)
    db.executesql(sql)
    sql="""UPDATE complaint_sup_toubiao SET status=%s,stime=now(),memo='%s' WHERE msl_id=%s"""%(status,refuse_memo,msl_id)
    db.executesql(sql)

    #推送
    sql="""SELECT MS.title,UX.openid,MS.id FROM complaint_sup_msg_send_list MSL 
        LEFT JOIN complaint_sup_msg_send MS ON MS.id=MSL.m_id
        LEFT JOIN users_gy UX ON UX.usr_id = MSL.to_usr_id
        WHERE MSL.id = %s
        """%msl_id
    rows,iN=db.select(sql)
    errcode = mWxPushMsg_fw(rows[0][0],rows[0][2],rows[0][1])
    s = """
        {
        "errcode": 0,
        "errmsg": "审核成功!",
        "errcode1":"%s"
        }        """%errcode
    # s=ToGBK(s)
    return HttpResponseJsonCORS(s)

def otherMsgList(request):
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
    sql="""SELECT MS.id,MS.title,MS.cid,U.usr_name,DP.cname,MT.txt1,DATE_FORMAT(MS.ctime,'%Y-%m-%d %H:%i:%s'),MS.cantalk,IFNULL(MS.has_new,0)
        FROM complaint_sup_msg_send MS 
        LEFT JOIN users U ON U.usr_id=MS.cid
        LEFT JOIN dept DP ON DP.id = U.dept_id
        LEFT JOIN mtc_t MT ON MT.id = MS.mtype AND MT.type='XXFL'
        WHERE 1=1 AND MS.is_send = 1 AND MS.cantalk=1
        """
    if typeID !='':
        sql+="AND MS.mtype=%s "%typeID
    if search !='':
        sql+="AND MS.title like '%%%s%%'"%search
    sql+="ORDER BY MS.ctime DESC"
    rows,iTotal_length,iTotal_Page,pageNo,select_size = db.select_for_grid(sql,pageNo,10)
    names = 'id title cid usr_name dept_name type_name ctime cantalk hasNew'.split()
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

def otherMsgDetail(request):
    usr_id_qy = request.session.get('usr_id_qy','') or testid
    if usr_id_qy ==0:
        s = """
        {
        "errcode": -1,
        "errmsg": "无权访问,请先关注"
        }        """
        return HttpResponseJsonCORS(s)
    pk = request.POST.get('pk','')
    # pk = 5
    if pk =='':
        s = """
        {
        "errcode": -1,
        "errmsg": "无效请求"
        }        """
        return HttpResponseJsonCORS(s)
    
    sql="""SELECT MS.id,MS.title,MS.cid,U.usr_name,DP.cname,MT.txt1,MS.memo,DATE_FORMAT(MS.ctime,'%%Y-%%m-%%d %%H:%%i:%%s'),MS.cantalk,MS.mtype
        FROM complaint_sup_msg_send MS 
        LEFT JOIN users U ON U.usr_id=MS.cid
        LEFT JOIN dept DP ON DP.id = U.dept_id
        LEFT JOIN mtc_t MT ON MT.id = MS.mtype AND MT.type='XXFL'
        WHERE MS.id=%s
        """%pk
    # print sql
    rows,iN=db.select(sql)

    names = 'id title cid usr_name dept_name type_name memo ctime cantalk mtype'.split()
    data = [dict(zip(names, d)) for d in rows]
    L = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)
    #L = L.replace('/fs/editor_files','%s/editor_files'%fs_url)

    sql="""SELECT FB.id
        ,CASE FB.itype WHEN 'qy' THEN U.usr_name ELSE UG.usr_name END
        ,CASE FB.itype WHEN 'qy' THEN CONCAT('%s',U.pic) ELSE UG.headimgurl END
        ,FB.memo,DATE_FORMAT(FB.ctime,'%%Y-%%m-%%d %%H:%%i:%%s')
        FROM complaint_sup_msg_feedback FB
        LEFT JOIN users U ON U.usr_id = FB.cid
        LEFT JOIN users_gy UG ON UG.usr_id = FB.cid
        WHERE FB.m_id=%s
        ORDER BY FB.ctime DESC 
        """%(imgUrl,pk)
    rows,iN=db.select(sql)
    names = 'id usr_name pic memo ctime'.split()
    data = [dict(zip(names, d)) for d in rows]
    feedback = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)

    s = """
        {
        "errcode": 0,
        "errmsg": "获取信息详情成功",
        "data":%s,
        "feedback":%s
        }        """%(L,feedback)
    # s=ToGBK(s)

    return HttpResponseJsonCORS(s)

def putFeedback(request):
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
    memo = request.POST.get('memo','')
    memo=MySQLdb.escape_string(memo)
    sql="""INSERT INTO complaint_sup_msg_feedback(m_id,cid,ctime,memo,itype) VALUES(%s,%s,now(),'%s','qy')"""%(pk,usr_id_qy,memo)
    db.executesql(sql)
    sql="""SELECT UG.openid,MS.title FROM complaint_sup_msg_send_list MSL
          LEFT JOIN users_gy UG ON UG.usr_id = MSL.to_usr_id
          LEFT JOIN complaint_sup_msg_send MS ON MS.id=MSL.m_id
          WHERE m_id=%s"""%(pk)
    rows,iN=db.select(sql)
    for e in rows:
        mWxPushMsg_Comment_fw(request,pk,e[1],e[0])
    s = """
        {
        "errcode": 0,
        "errmsg": "提交成功"
        }        """
    return HttpResponseJsonCORS(s)

import httplib
def mWxPushMsg_fw(title,pk,toUser):   
    now=getToday()
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
    file_id=pk
    sUrl='%s/complaint/login/default_gy?fid=infoDetail&seq=%s&must_reply=true'%(host_url,file_id)
    description = """您参与的%s的供应商投标报名，有新审核信息啦"""%(title)
    surl = my_urlencode(sUrl)
    # print toUser
    description = json.dumps(description)
    now = json.dumps(now)
    city = json.dumps("深圳")
    url = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_base&state=wx#wechat_redirect"%(AppId_gy,surl)

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
    """%(toUser,template_id_msg_gy,sUrl,description,city,now)
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

def mWxPushMsg_Comment_fw(request,pk,title,toUser):   
    now=getToday()
    conn = httplib.HTTPSConnection('api.weixin.qq.com')  
    sToken =  read_access_token_common('access_token_gy')
    if sToken == '':            
        url = "/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s"%(AppId_gy,AppSecret_gy)
        conn.request('GET', '%s'%url)  
        res = conn.getresponse()       
        body = res.read()  
        ddata=json.loads(body)
        sToken = ddata['access_token'] 
        conn.close()  
        write_access_token_common(body,'access_token_gy')
    file_id=pk
    sUrl='%s/complaint/login/default_gy?fid=infoDetail&seq=%s&must_reply=true'%(host_url,file_id)
    description = """关于“%s”有新留言，请您及时查阅。"""%(title)
    surl = my_urlencode(sUrl)
    # print toUser
    description = json.dumps(description)
    now = json.dumps(now)
    city = json.dumps("深圳")
    url = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_base&state=wx#wechat_redirect"%(AppId_gy,surl)

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
    """%(toUser,template_id_msg_gy,sUrl,description,city,now)
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
    return HttpResponseCORS(request,errcode)

def getAuditUserIds():
    sql = """select u.usr_id from roles r
             left join usr_role ur  on ur.role_id = r.role_id
             left join users u on ur.usr_id = u.usr_id
             where r.role_name = '招标专员（供应商服务平台）'"""
    rows,iN = db.select(sql)
    users= []
    for e in rows:
        users.append(str(e[0]))
    users.append('2110')
    return users