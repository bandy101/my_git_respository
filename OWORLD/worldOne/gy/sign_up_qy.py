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
def getSupList(request):
    usr_id_qy = request.session.get('usr_id_qy','') or testid
    print "usr_id_qy=%s"%usr_id_qy
    search = request.POST.get('search','')
    situation = request.POST.get('situation','')
    search = MySQLdb.escape_string(search)
    users = getAuditUserIds()
    if str(usr_id_qy) not in users :
        s = """
        {
        "errcode": -1,
        "errmsg": "无权访问"
        }        """
        return HttpResponseJsonCORS(s)
    pageNo =  request.POST.get('pageNo') or 1
    pageNo=int(pageNo)
    sql="""select id,sup_name,utime,status from suppliers_sign_up where status != 0
        """
    if search !='':
        sql+="AND (IFNULL(sup_name,'') LIKE '%%%s%%' )"%(search)
    if situation !='':
        sql+="AND (status='%s' "%(situation)
        sql+=")"
    sql+="ORDER BY id DESC"
    print sql 
    rows,iTotal_length,iTotal_Page,pageNo,select_size = db.select_for_grid(sql,pageNo,10)
    dataList=[]
    for e in rows:
        e=list(e)
        dataList.append(e)
    names = 'id sup_name ctime status'.split()
    data = [dict(zip(names, d)) for d in dataList]
    L = json.dumps(data,ensure_ascii=False,cls=ComplexEncoder)

    s = """
        {
        "errcode": 0,
        "errmsg": "获取供应商报名列表成功",
        "data":%s,
        "totalLength":%s,
        "totalPage":%s,
        "pageNo":%s,
        "pageSize":%s
        }        """%(L,iTotal_length,iTotal_Page,pageNo,select_size)
    # s=ToGBK(s)
    # print s
    return HttpResponseJsonCORS(s)

def audit(request):
    usr_id_qy = request.session.get('usr_id_qy','') or testid
    if usr_id_qy ==0:
        s = """
        {
        "errcode": -1,
        "errmsg": "无权访问"
        }        """
        return HttpResponseJsonCORS(s)
    id = request.POST.get('id','')
    if id =='':
        s = """
        {
        "errcode": -1,
        "errmsg": "无效请求"
        }        """
        return HttpResponseJsonCORS(s)
    audit_ret = request.POST.get('audit_ret','') 
    audit_memo = request.POST.get('audit_memo','')
    sql = """UPDATE suppliers_sign_up SET status=%s,audit_memo='%s',audit_user_id=%s,audit_time=now() WHERE id=%s
        """%(audit_ret,audit_memo,usr_id_qy,id)
    # print sql 
    db.executesql(sql)
    mWxPushMsg_audit(request,id,audit_ret)
    s = """
        {
        "errcode": 0,
        "errmsg": "提交成功"
        }        """
    return HttpResponseJsonCORS(s)

def getAuditUserIds():
    sql = """select u.usr_id from roles r
             left join usr_role ur  on ur.role_id = r.role_id
             left join users u on ur.usr_id = u.usr_id
             where r.role_name = '供应商加入审核（供应商服务平台）'"""
    rows,iN = db.select(sql)
    users= []
    for e in rows:
        users.append(str(e[0]))
    users.append('5')
    users.append('228')
    users.append('651')
    users.append('231')
    users.append('2938')
    users.append('2110')
    users.append('2572')
    return users

import httplib
template_id_result_gy = "vCCNkMSp5PSDBYMVGVjrq3kZU_HK729oS6T8QEwkNgg"
def mWxPushMsg_audit(request,id,audit_ret):
    year=getToday()[:4]  
    L =Get_data_audit(request,id)
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
    sUrl='%s/complaint/login/default_gy?fid=apply_form_name&path=apply_gy&seq=%s'%(host_url,id)
    toUser = L[2]
    ctime = L[3]
    title = L[1]
    type = '供应商报名'
    if str(audit_ret) == '2':
        ret = u"通过"
        color = '#173177'
        reason = '您的报名已通过，请完善其他信息'
    else:
        ret = u"未通过"
        color = '#dd524d'
        reason = L[4]
    description = "感谢您的关注。"
    ret = json.dumps(ret)
    title = json.dumps(title)
    type = json.dumps(type)
    reason = json.dumps(reason)
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
            "value":%s,
            "color":"%s"
            },
            "keyword3": {
            "value":%s,
            "color":"#173177"
            },
            "remark": {
            "value":%s,
            "color":"#173177"
            }
            
            }
            }
    """%(toUser,template_id_result_gy,sUrl,title,type,ret,color,reason,description)
    print ToGBK(sMsg)
    conn = httplib.HTTPSConnection('api.weixin.qq.com')  
    url = "/cgi-bin/message/template/send?access_token=%s"%(sToken)
    #print url
    conn.request('POST', '%s'%url,sMsg)  
    res = conn.getresponse()       
    body = res.read()  
    conn.close()  
    ddata=json.loads(body)
    errcode = ddata['errcode']
    print body    
    return HttpResponseCORS(request,errcode)

def Get_data_audit(request,id):
    sql="""SELECT s.id,s.sup_name,u.openid,audit_time,audit_memo
            FROM suppliers_sign_up s
            left join users_gy u on u.usr_id = s.cid
            WHERE id = %s
            """%(id)
    rows,iN = db.select(sql)
    L=rows[0]
    return L
