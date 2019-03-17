# -*- coding: utf-8 -*-
#########################################################################
# Author: jonyqin
# Created Time: Thu 11 Sep 2014 03:55:41 PM CST
# File Name: Sample.py
# Description: WXBizMsgCrypt 浣跨敤demo鏂囦欢
#########################################################################
prj_name=__name__.split('.')[0]
import sys  
import os
import time
import json
import httplib
from WXBizMsgCrypt import WXBizMsgCrypt
from django.http import HttpResponse,JsonResponse
import xml.etree.cElementTree as ET
exec ('from %s.share        import HttpResponseCORS,db,ToGBK,data_url,my_urlencode'%prj_name) 

def callback(request):
    wxcpt=WXBizMsgCrypt(m_sToken,m_sEncodingAESKey,m_sCorpID)
    sVerifyMsgSig=request.GET.get('msg_signature','')
    sVerifyTimeStamp=request.GET.get('timestamp','')
    sVerifyNonce=request.GET.get('nonce','')
    sVerifyEchoStr=request.GET.get('echostr','')
    ret,sEchoStr=wxcpt.VerifyURL(sVerifyMsgSig, sVerifyTimeStamp,sVerifyNonce,sVerifyEchoStr)
    if(ret!=0):
        #write_sql("ERR: VerifyURL ret: " + str(ret))
        return HttpResponse("ERR: VerifyURL ret: " + str(ret))
    return HttpResponse(sEchoStr)

def getInfoFromWx():
    uL = []
    dL = []
    sql = """select id,`corp_id`,`corpsecret`,`agentid` from `wx_corp_agent` where name='通讯录'"""
    lT,iN = db.select(sql)
    if iN ==0 :
        return dL,uL
    
    aid = lT[0][0] 
    corp_id = lT[0][1] 
    corpsecret = lT[0][2] 
    agentid = lT[0][3] 
    sToken =  read_access_token(aid)
    if sToken == '':
        sToken = write_access_token(aid,corp_id,corpsecret)

    dL = getDepts(1,sToken)
    uL = getUsers(1,sToken)
    return dL,uL

def getUsers(dpet_id,sToken):
    url = "/cgi-bin/user/list?access_token=%s&department_id=%s&fetch_child=1&status=0"%(sToken,dpet_id)
    conn = httplib.HTTPSConnection('qyapi.weixin.qq.com')  
    conn.request('GET', url)  

    res = conn.getresponse()       
    body = res.read()  
    conn.close()  
    ddata=json.loads(body)
    userlist = ddata['userlist'] 
    #print len(userlist)
    return userlist

def getDepts(dpet_id,sToken):
    url = "/cgi-bin/department/list?access_token=%s&id=%s"%(sToken,dpet_id)
    conn = httplib.HTTPSConnection('qyapi.weixin.qq.com')  
    conn.request('GET', url)  

    res = conn.getresponse()       
    body = res.read()  
    conn.close()  
    ddata=json.loads(body)
    deptlist = ddata['department'] 
    #print len(deptlist)
    return deptlist

def update_wx_dept(dept_id,name,parentid,sort,wx_status):
    sql = """select id,`corp_id`,`corpsecret`,`agentid` from `wx_corp_agent` where name='通讯录'"""
    lT,iN = db.select(sql)
    if iN ==0 :
        return dL,uL
    
    aid = lT[0][0] 
    corp_id = lT[0][1] 
    corpsecret = lT[0][2] 
    agentid = lT[0][3] 
    sToken =  read_access_token(aid)
    if sToken == '':
        sToken = write_access_token(aid,corp_id,corpsecret)

    if parentid == 0:
        sMsg = """{
                "id": %s,
                "name": "%s",
                "order": %s
                }
                """%(dept_id,name,sort)
    else:
        sMsg = """{
                "id": %s,
                "name": "%s",
                "parentid": %s,
                "order": %s
                }
                """%(dept_id,name,parentid,sort)

    if wx_status == 1:
        return createDept(sToken,sMsg) 
    elif wx_status == 2:
        return updateDept(sToken,sMsg) 
    elif wx_status == 3:
        return deleteDept(sToken,dept_id) 
    return -1,'未知错误'

def createDept(sToken,sMsg):
    url = "/cgi-bin/department/create?access_token=%s"%(sToken)
    conn = httplib.HTTPSConnection('qyapi.weixin.qq.com')  
        
    conn.request('POST', '%s'%url,sMsg)  
        
    res = conn.getresponse()       
    body = res.read()  
    conn.close()  
        
    ddata=json.loads(body)
    errcode = ddata.get('errcode','')
    errmsg = ddata.get('errmsg','')
    return errcode,errmsg

def updateDept(sToken,sMsg):
    url = "/cgi-bin/department/update?access_token=%s"%(sToken)
    conn = httplib.HTTPSConnection('qyapi.weixin.qq.com')  
    #print ToGBK(sMsg)
    conn.request('POST', '%s'%url,sMsg)  
        
    res = conn.getresponse()       
    body = res.read()  
    conn.close()  
    #print body
    ddata=json.loads(body)
    errcode = ddata.get('errcode','')
    errmsg = ddata.get('errmsg','')
    return errcode,errmsg

def deleteDept(sToken,dept_id):
    url = "/cgi-bin/department/delete?access_token=%s&id=%s"%(sToken,dept_id)
    conn = httplib.HTTPSConnection('qyapi.weixin.qq.com')  
        
    conn.request('GET', '%s'%url)  
        
    res = conn.getresponse()       
    body = res.read()  
    conn.close()  
        
    ddata=json.loads(body)
    print body
    errcode = ddata.get('errcode','')
    errmsg = ddata.get('errmsg','')
    return errcode,errmsg

def getuserinfo(code,agentname):
    sql = """select id,`corp_id`,`corpsecret`,`agentid` from `wx_corp_agent` where name='%s'"""%agentname
    lT,iN = db.select(sql)
    if iN ==0 :
        return dL,uL
    
    aid = lT[0][0] 
    corp_id = lT[0][1] 
    corpsecret = lT[0][2] 
    agentid = lT[0][3] 
    sToken =  read_access_token(aid)
    if sToken == '':
        sToken = write_access_token(aid,corp_id,corpsecret)

    conn = httplib.HTTPSConnection('qyapi.weixin.qq.com')  
    url = "/cgi-bin/user/getuserinfo?access_token=%s&code=%s"%(sToken,code)
    conn.request('GET', '%s'%url)  
    res = conn.getresponse()       
    body = res.read()  
    conn.close()   
    ddata=json.loads(body)
    return ddata

def update_wx_user(wx_id,usr_name,dept_id,sort,mobile,gender,email,enable,wx_status):
    sql = """select id,`corp_id`,`corpsecret`,`agentid` from `wx_corp_agent` where name='通讯录'"""
    lT,iN = db.select(sql)
    if iN ==0 :
        return dL,uL
    
    aid = lT[0][0] 
    corp_id = lT[0][1] 
    corpsecret = lT[0][2] 
    agentid = lT[0][3] 
    sToken =  read_access_token(aid)
    if sToken == '':
        sToken = write_access_token(aid,corp_id,corpsecret)

    sMsg = """{
               "userid": "%s",
               "name": "%s",
               "department": [%s],
               "mobile": "%s","""%(wx_id,usr_name,dept_id,mobile)
    if gender == 0:
        sMsg += """
               "gender": "2","""
    elif gender == 1:
        sMsg += """
               "gender": "1","""
    sMsg += """
               "email": "%s",
               "enable": %s
               }
                """%(email,enable)
    #print ToGBK(sMsg)
    if wx_status == 1:
        return createUser(sToken,sMsg) 
    elif wx_status == 2:
        return updateUser(sToken,sMsg) 
    elif wx_status == 3:
        return deleteUser(sToken,wx_id) 
    return -1,'未知错误'

def createUser(sToken,sMsg):
    url = "/cgi-bin/user/create?access_token=%s"%(sToken)
    conn = httplib.HTTPSConnection('qyapi.weixin.qq.com')  
        
    conn.request('POST', '%s'%url,sMsg)  
        
    res = conn.getresponse()       
    body = res.read()  
    conn.close()  
        
    ddata=json.loads(body)
    errcode = ddata.get('errcode','')
    errmsg = ddata.get('errmsg','')
    return errcode,errmsg

def updateUser(sToken,sMsg):
    url = "/cgi-bin/user/update?access_token=%s"%(sToken)
    conn = httplib.HTTPSConnection('qyapi.weixin.qq.com')  
        
    conn.request('POST', '%s'%url,sMsg)  
        
    res = conn.getresponse()       
    body = res.read()  
    conn.close()  
        
    ddata=json.loads(body)
    errcode = ddata.get('errcode','')
    errmsg = ddata.get('errmsg','')
    return errcode,errmsg

def deleteUser(sToken,wx_id):
    url = "/cgi-bin/user/delete?access_token=%s&userid=%s"%(sToken,wx_id)
    conn = httplib.HTTPSConnection('qyapi.weixin.qq.com')  
        
    conn.request('GET', '%s'%url)  
        
    res = conn.getresponse()       
    body = res.read()  
    conn.close()  
        
    ddata=json.loads(body)
    errcode = ddata.get('errcode','')
    errmsg = ddata.get('errmsg','')
    return errcode,errmsg

def mWxPushMsg(sToken,sMsg,usr_id,usr_name):   
    conn = httplib.HTTPSConnection('qyapi.weixin.qq.com')  
    url = "/cgi-bin/message/send?access_token=%s"%(sToken)
    #print url
    conn.request('POST', '%s'%url,sMsg)  

    res = conn.getresponse()       
    body = res.read()  
    conn.close()  

    #保存推送LOG
    try:
        ddata=json.loads(body)
        #print ddata
        sdata=json.loads(sMsg)
        touser = sdata.get('touser','')
        toparty = sdata.get('toparty','')
        totag = sdata.get('totag','')
        agentid = sdata.get('agentid','')
        errcode = ddata.get('errcode','')
        errmsg = ddata.get('errmsg','')
        invaliduser = ddata.get('invaliduser','')
        invalidparty = ddata.get('invalidparty','')
        invalidtag = ddata.get('invalidtag','')
        sql = """insert into `wx_pushmsg_log` (`cid`,`cusrname`,`ctime`,`msg`,`touser`,`toparty`,`totag`,`agentid`,`errcode`,`errmsg`,`invaliduser`,`invalidparty`,`invalidtag`)
                 values(%s,'%s',now(),'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s');
              """%(usr_id,usr_name,sMsg,touser,toparty,totag,agentid,errcode,errmsg,invaliduser,invalidparty,invalidtag)
        db.executesql(sql)
    except:
        pass   
    return ddata

def mWxPushMsg_Audit(menu_id,pk,title,toUser,state,usr_id,usr_name):   
    sql = """select id,`corp_id`,`corpsecret`,`agentid` from `wx_corp_agent` where name='公文审批'"""
    lT,iN = db.select(sql)
    if iN ==0 :
        return dL,uL
    
    aid = lT[0][0] 
    corp_id = lT[0][1] 
    corpsecret = lT[0][2] 
    agentid = lT[0][3] 
    sToken =  read_access_token(aid)
    if sToken == '':
        sToken = write_access_token(aid,corp_id,corpsecret)
    sUrl='%s/index_wx/?menu_id=%s&pk=%s&func=%s'%(data_url,menu_id,pk,state)
    surl = my_urlencode(sUrl)
    url = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_base&agentid=%s&state=%s#wechat_redirect"%(corp_id,surl,agentid,state)

    sMsg ="""{
              "touser": "%s",
                     """%(toUser)
    sMsg +="""       "msgtype": "news",
              "agentid": "%s",
              "news": {
                  "articles":[
                        {
                        "title": "%s",
                        "url": "%s"
                        }
                  ]
                }
             }
             """%(agentid,title,sUrl)
    #print ToGBK(sMsg)
    return mWxPushMsg(sToken,sMsg,usr_id,usr_name)

def mWxPushMsg_Info(pk,title,description,must_reply,toUser,func,usr_id,usr_name):   
    sql = """select id,`corp_id`,`corpsecret`,`agentid` from `wx_corp_agent` where name='信息交换'"""
    lT,iN = db.select(sql)
    if iN ==0 :
        return dL,uL
    
    aid = lT[0][0] 
    corp_id = lT[0][1] 
    corpsecret = lT[0][2] 
    agentid = lT[0][3] 
    sToken =  read_access_token(aid)
    if sToken == '':
        sToken = write_access_token(aid,corp_id,corpsecret)

    sUrl='%s/index_wx/?pk=%s&must_reply=%s&func=%s'%(data_url,pk,must_reply,func)
    surl = my_urlencode(sUrl)
    url = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_base&agentid=%s&state=%s#wechat_redirect"%(corp_id,surl,agentid,func)
    #print sUrl
    sMsg ="""{
              "touser": "%s",
                     """%(toUser)
    sMsg +="""       "msgtype": "news",
              "agentid": "%s",
              "news": {
                  "articles":[
                        {
                        "title": "%s",
                        "url": "%s",
                        "description":"%s"
                        }
                  ]
                }
             }
             """%(agentid,title,sUrl,description)
    #print ToGBK(sMsg) 
    return mWxPushMsg(sToken,sMsg,usr_id,usr_name)

def mWxPushMsg_Log(id,title,description,toUser,func,usr_id,usr_name):   
    sql = """select id,`corp_id`,`corpsecret`,`agentid` from `wx_corp_agent` where name='工作日志'"""
    lT,iN = db.select(sql)
    if iN ==0 :
        return dL,uL
    
    aid = lT[0][0] 
    corp_id = lT[0][1] 
    corpsecret = lT[0][2] 
    agentid = lT[0][3] 
    sToken =  read_access_token(aid)
    if sToken == '':
        sToken = write_access_token(aid,corp_id,corpsecret)

    sUrl='%s/index_wx/?id=%s&func=%s'%(data_url,id,func)
    sMsg ="""{
              "touser": "%s",
                     """%(toUser)
    sMsg +="""       "msgtype": "news",
              "agentid": "%s",
              "news": {
                  "articles":[
                        {
                        "title": "%s",
                        "url": "%s",
                        "description":"%s"
                        }
                  ]
                }
             }
             """%(agentid,title,sUrl,description)
    print ToGBK(sMsg) 
    return mWxPushMsg(sToken,sMsg,usr_id,usr_name)

def getLoginID(code):
    sql = """select id,`corp_id`,`corpsecret`,`agentid` from `wx_corp_agent` where name='授权登录'"""
    lT,iN = db.select(sql)
    if iN ==0 :
        return ''
    
    aid = lT[0][0] 
    corp_id = lT[0][1] 
    corpsecret = lT[0][2] 
    agentid = lT[0][3] 
    sToken =  read_access_token(aid)
    if sToken == '':
        sToken = write_access_token(aid,corp_id,corpsecret)

    url = "/cgi-bin/user/getuserinfo?access_token=%s&code=%s "%(sToken,code)
    conn = httplib.HTTPSConnection('qyapi.weixin.qq.com')  
         
    conn.request('GET', '%s'%url)  
        
    res = conn.getresponse()       
    body = res.read()  
    conn.close()  
    #print body
    ddata=json.loads(body)
    UserId = ddata.get('UserId','')
    return UserId


def read_access_token(aid):
    sql = """select ifnull(access_token,'') from `wx_corp_agent` 
                 where expires_in - time_to_sec(timediff(now(),token_utime))>30 and id='%s'"""%(aid)
    lT,iN = db.select(sql)
    if iN ==0 :
        token = ''  
    else:
        token = lT[0][0] 
    return token

def write_access_token(aid,corp_id,corpsecret):
    conn = httplib.HTTPSConnection('qyapi.weixin.qq.com')  
    url = "/cgi-bin/gettoken?corpid=%s&corpsecret=%s"%(corp_id,corpsecret)
    #print url
    conn.request('GET', '%s'%url)  
    res = conn.getresponse()       
    body = res.read()  
    #print body
    ddata=json.loads(body)
    sToken = ddata['access_token'] 
    expires_in = ddata['expires_in'] 
    conn.close()  
    sql = "update wx_corp_agent set access_token='%s',expires_in='%s',token_utime=now() where id='%s'"%(sToken,expires_in,aid)
    db.executesql(sql)
    return sToken
