# -*- coding: utf-8 -*-
# 保存列表数据
prj_name=__name__.split('.')[0]
exec ('from %s.share        import db,ToGBK,HttpResponseCORS,HttpResponseJsonCORS,mValidateUser,ComplexEncoder'%prj_name) 
import sys
import os
import json
import time
from HW_DT_TOOL                 import getToday
sys.path.append("/home/webroot/oWorld/complaint")
from share        import template_id_msg,AppId,AppSecret,host_url,read_access_token,write_access_token,my_urlencode
from share        import template_id_msg_gy,AppId_gy,AppSecret_gy,read_access_token_common,write_access_token_common
from multiprocessing import Process


def saveMsg(request):
    menu_id = request.POST.get('menu_id', 0)
    mode =  request.POST.get('mode','')
    is_send =  request.GET.get('is_send','')
    is_send = is_send.replace('/','')

    # if str(is_send)=='0':
    #     time.sleep(3)
    ret,errmsg,d_value = mValidateUser(request,mode,menu_id)
    if ret!=0:
        return HttpResponseCORS(request,errmsg)
    usr_id = d_value[0]
    usr_name = d_value[1]
    dept_id = d_value[2]
    
    data =  request.POST.get('data','')
    data_list = json.loads(data)
    pk =  data_list.get('pk','')
    title = data_list.get('title','')
    read_people = data_list.get('read_people','')
    mtype = data_list.get('mtype','')
    memo = data_list.get('memo','')
    to_type = data_list.get('to_type','') or 0

    if pk=='':
        sql="""INSERT INTO msg_send(cid,ctime,title,read_people,mtype,cusrname,memo,is_send,to_type)
            VALUES(%s,now(),'%s','%s',%s,'%s','%s',%s,%s)
            """%(usr_id,title,read_people,mtype,usr_name,memo,is_send,to_type)
        db.executesql(sql)
        sql = "select last_insert_id();"
        rows,iN = db.select(sql)
        pk = rows[0][0]
    else:
        sql="""UPDATE msg_send 
            SET uid=%s,utime=now(),title='%s',read_people='%s',mtype=%s,uusrname='%s',memo='%s',is_send='%s',to_type=%s WHERE id = %s 
            """%(usr_id,title,read_people,mtype,usr_name,memo,is_send,to_type,pk)
        # print sql
        db.executesql(sql)
    if str(is_send)=='1':
        #自定义选人
        if read_people !='' and str(to_type)=='0' :
            msgDeal(request,pk,read_people,title)
        #全体人员
        if str(to_type)=='1':
            msgDealOther(request,pk,'all',title)
        #已绑定
        if str(to_type)=='2':
            msgDealOther(request,pk,'bound',title)
        #未绑定
        if str(to_type)=='3':
            msgDealOther(request,pk,'unbound',title)

    s = """
        {
        "errcode": 0,
        "errmsg": "操作成功",
        "pk":%s
        }
        """%(pk)
    return HttpResponseCORS(request,s)

def msgDeal(requset,pk,read_people,title): 
    read_people = read_people.split(',')
    id_list='0'
    for e in read_people:
        # print e
        id_list+=','+str(e)
    # id_list+=''
    sql="""SELECT usr_id,openid FROM users_wx WHERE usr_id in (%s)"""%id_list
    rows,iN = db.select(sql)
    mWxPushMsg_fw(rows,title,pk)
    return

def msgDealOther(requset,pk,stype,title): 
    where = ''
    if stype=='all':
        where =''
    if stype=='bound':
        where = 'AND status=1 and is_labor = 0'
    if stype=='unbound':
        where = 'AND (IFNULL(status,0)=0 or is_labor = 1)'
    sql="""SELECT usr_id,openid FROM users_wx WHERE 1=1 %s """%where
    rows,iN = db.select(sql)
    mWxPushMsg_fw(rows,title,pk)
    return

def saveMsgSup(request):
    menu_id = request.POST.get('menu_id', 0)
    mode =  request.POST.get('mode','')
    is_send =  request.GET.get('is_send','')
    is_send = is_send.replace('/','')

    # if str(is_send)=='0':
    #     time.sleep(3)
    ret,errmsg,d_value = mValidateUser(request,mode,menu_id)
    if ret!=0:
        return HttpResponseCORS(request,errmsg)
    usr_id = d_value[0]
    usr_name = d_value[1]
    dept_id = d_value[2]
    
    data =  request.POST.get('data','')
    data_list = json.loads(data)
    pk =  data_list.get('pk','')
    title = data_list.get('title','')
    read_people = data_list.get('read_people','')
    mtype = data_list.get('mtype','')
    memo = data_list.get('memo','')
    to_type = data_list.get('to_type','') or 0
    cantalk = data_list.get('cantalk','') or 0

    if pk=='':
        sql="""INSERT INTO complaint_sup_msg_send(cid,ctime,title,read_people,mtype,cusrname,memo,is_send,to_type,cantalk)
            VALUES(%s,now(),'%s','%s',%s,'%s','%s',%s,%s,%s)
            """%(usr_id,title,read_people,mtype,usr_name,memo,is_send,to_type,cantalk)
        db.executesql(sql)
        sql = "select last_insert_id();"
        rows,iN = db.select(sql)
        pk = rows[0][0]
    else:
        sql="""UPDATE complaint_sup_msg_send 
            SET uid=%s,utime=now(),title='%s',read_people='%s',mtype=%s,uusrname='%s',memo='%s',is_send='%s',to_type=%s,cantalk=%s WHERE id = %s 
            """%(usr_id,title,read_people,mtype,usr_name,memo,is_send,to_type,cantalk,pk)
        # print sql
        db.executesql(sql)
    if str(is_send)=='1':
        #自定义选人
        if read_people !='' and str(to_type)=='0' :
            msgDeal_gy(request,pk,read_people,title)
        #全体人员
        if str(to_type)=='1':
            msgDealOther_gy(request,pk,'all',title)
        #已绑定
        if str(to_type)=='2':
            msgDealOther_gy(request,pk,'bound',title)
        #未绑定
        if str(to_type)=='3':
            msgDealOther_gy(request,pk,'unbound',title)

    s = """
        {
        "errcode": 0,
        "errmsg": "操作成功!",
        "pk":%s
        }
        """%(pk)
    return HttpResponseCORS(request,s)

def msgDeal_gy(requset,pk,read_people,title): 
    read_people = read_people.split(',')
    id_list='0'
    for e in read_people:
        # print e
        id_list+=','+str(e)
    # id_list+=''
    sql="""SELECT usr_id,openid FROM users_gy WHERE usr_id in (%s)"""%id_list
    rows,iN = db.select(sql)
    mWxPushMsg_fw_gy(rows,title,pk)
    return

def msgDealOther_gy(requset,pk,stype,title): 
    where = ''
    if stype=='all':
        where =''
    if stype=='bound':
        where = 'AND status=1'
    if stype=='unbound':
        where = 'AND IFNULL(status,0)=0'
    sql="""SELECT usr_id,openid FROM users_gy WHERE 1=1 %s """%where
    rows,iN = db.select(sql)
    mWxPushMsg_fw_gy(rows,title,pk)
    return

def feedback_gy(request):
    menu_id = request.POST.get('menu_id', 0)
    mode =  request.POST.get('mode','')
    ret,errmsg,d_value = mValidateUser(request,mode,menu_id)
    if ret!=0:
        return HttpResponseCORS(request,errmsg)
    usr_id = d_value[0]
    usr_name = d_value[1]

    data =  request.POST.get('data','')
    data_list = json.loads(data)
    pk =  data_list.get('pk','')
    title =  data_list.get('title','')
    fb_pass =  data_list.get('fb_pass','')
    fb_money =  data_list.get('fb_money') or 'NULL'
    fb_reject =  data_list.get('fb_reject','')

    sql = """update complaint_sup_msg_send set fb_pass='%s',fb_money=%s,fb_reject='%s',fb_status=1,fb_usr_id=%s,fb_usr_name='%s',fb_time=now() where id=%s
          """%(fb_pass,fb_money,fb_reject,usr_id,usr_name,pk)
    db.executesql(sql)

    if fb_pass != '':
        mWxPushMsg_gy_feedback(pk,title,fb_pass,1)
    if fb_reject != '':
        mWxPushMsg_gy_feedback(pk,title,fb_reject,0)
    s = """
        {
        "errcode": 0,
        "errmsg": "发送发聩结果成功!",
        "pk":%s
        }
        """%(pk)
    return HttpResponseCORS(request,s)

import httplib
def mWxPushMsg_gy_feedback(pk,title,users,type):   
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
    if type == 1:
        template_id = '_7E2obSKsMDG9Qav0iXqwYpxgv5VZ8amzWaAbHz7IbU'
        stitle ="""恭喜您中标！"""
    else:
        stitle ="""很遗憾，您未能中得此标！"""
        template_id = 'dGeSPIZWmIvtuTBbwkds8ygpKi1FA-IGG0hKl8Z-ARc'
    stitle=json.dumps(stitle)
    keyword1 = json.dumps("宝鹰集团材料采购部")
    keyword2 = json.dumps(title)

    sql = """select u.openid,ab.sup_id from users_gy u
             left join addr_book ab on u.addr_id = ab.id
             where FIND_IN_SET(ab.sup_id,'%s') and u.status=1"""%(users)
    rows,iN = db.select(sql)
    for e in rows:
        sUrl='%s/complaint/login/default_gy?fid=bidResult&path=bid_feedBack&seq=%s'%(host_url,pk)
        sMsg ="""{
            "touser":"%s",
            "template_id":"%s",
            "topcolor":"#FF0000",
            "url":"%s",
            "data":{
            "first": {
            "value":%s,
            "color":"#ff0000"
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
        """%(e[0],template_id,sUrl,stitle,keyword1,keyword2)

        conn = httplib.HTTPSConnection('api.weixin.qq.com')  
        url = "/cgi-bin/message/template/send?access_token=%s"%(sToken)
        #print url
        conn.request('POST', '%s'%url,sMsg)  
        res = conn.getresponse()       
        body = res.read()  
        print body
        conn.close()  
        ddata=json.loads(body)
        errcode = ddata['errcode']
        errmsg = ddata['errmsg']

    return 

def mWxPushMsg_fw(rows,title,pk):   
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
    stitle ="""新消息"""
    description = """%s"""%(title)
    surl = my_urlencode(sUrl)
    # print toUser
    stitle=json.dumps(stitle)
    description = json.dumps(description)
    now = json.dumps(now)
    city = json.dumps("深圳")
    url = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_base&state=wx#wechat_redirect"%(AppId,surl)

    sMsg ="""{
            "touser":"{toUser}",
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
    """%(template_id_msg,sUrl,description,city,now)

    p1=Process(target=push,kwargs={'rows':rows,'token':sToken,'msg':sMsg,'id':pk,'table_name':'msg_send_list',})
    p1.start()
    print('main process:',os.getpid(),os.getppid())

    return

def mWxPushMsg_fw_gy(rows,title,pk):   
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
    stitle ="""新消息"""
    description = """%s"""%(title)
    surl = my_urlencode(sUrl)
    # print toUser
    stitle=json.dumps(stitle)
    description = json.dumps(description)
    now = json.dumps(now)
    city = json.dumps("深圳")
    url = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_base&state=wx#wechat_redirect"%(AppId_gy,surl)

    sMsg ="""{
            "touser":"{toUser}",
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
    """%(template_id_msg_gy,sUrl,description,city,now)

    p1=Process(target=push,kwargs={'rows':rows,'token':sToken,'msg':sMsg,'id':pk,'table_name':'complaint_sup_msg_send_list',})
    p1.start()
    #print('main process:',os.getpid(),os.getppid())

    return 

import MySQLdb
def push(rows,token,msg,id,table_name):
    db1 = MySQLdb.connect(host="127.0.0.1",user="root",passwd="24ea8194",db="complaint",charset="utf8")
    cur=db1.cursor()
    for e in rows:
        msg1 = msg.replace('{toUser}',e[1])
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
        sql = "insert into %s (m_id,to_usr_id,ctime,errcode,errmsg) values (%s,%s,now(),%s,'%s')"%(table_name,id,e[0],errcode,errmsg)
        r = cur.execute(sql)
        db1.commit()
        #print body    
    cur.close()      
    sys.exit(0)
    return
