# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf8')
import os,time
import json
import urllib
from HW_DB   import DataBaseParent_local
#本地mysql数据库
db=DataBaseParent_local()  
# uc=unicode(str('s'), 'eucgb2312_cn')
sys.path.append("/home/webroot/oWorld")
from common.HW_FILE_TOOL           import make_sub_path,writeTXT,openTXT,writeLOG
#供应商服务号
AppId_gy = 'wxe703baaad2a1c9dc'
Token_gy = 'Fgfdg1F_W45Ed155w7wrfw'
EncodingAESKey_gy = 'MOTN3tKdlg8rTbcYtK32MW6IK9QG4oQbZH5ZzQUQSk6'
AppSecret_gy = '780065948cba96c5831c6b047a0ff7f8'
template_id_msg_gy = "7J5iK9tBv3xqwjHRo6r9j6Baq_VOPuxqDDbJPoACK5w"
template_id_result_gy = "NwwwjuHfSg1mOvN1oHObizd8VjllYy1Yh9lYOkia5Uk"
host_url = 'http://lw.szby.cn'

def pushDeal():
    sql="""SELECT PMP.id,UG.openid,PMP.pjname,now(),PMP.Sup_id,UG.usr_id
        FROM (SELECT a.* FROM prj_mat_pay a WHERE NOT EXISTS(SELECT 1 FROM complaint_sup_payinfo_push b WHERE a.id=b.m_id) )PMP 
        LEFT JOIN addr_book AB ON AB.sup_id=PMP.Sup_id AND AB.sup_id is not null
        LEFT JOIN users_gy UG ON UG.addr_id=AB.id
        WHERE PMP.pay_stat=1 AND UG.status=1 AND PMP.is_push=0
        AND IFNULL(UG.openid,'')!=''
        #AND EXISTS(SELECT 1 FROM users_gy C WHERE C.addr_id = AB.id)
        LIMIT 100"""
    rows,iN=db.select(sql)
    for e in rows:
        pk=e[0]
        openid=e[1]
        pjname=e[2]
        pushTime=e[3]
        sup_id=e[4]
        usr_id=e[5]
        errcode = mWxPushMsg_fw_gy(pjname,pk,openid)
        if str(errcode)=='0':
            sql="""INSERT INTO complaint_sup_payinfo_push(ctime,m_id,to_usr_id,sup_id) VALUES(now(),%s,%s,%s)"""%(pk,usr_id,sup_id)
            db.executesql(sql)
            sql="""UPDATE prj_mat_pay SET is_push=1 WHERE id=%s"""%(pk)
            db.executesql(sql)
        print pjname
    # sql="""UPDATE prj_mat_pay SET is_push=1 where is_push=0 and pay_stat=1"""
    # db.executesql(sql)

import httplib
def mWxPushMsg_fw_gy(pjname,pk,toUser):  
    #获取当前日期
    t=time.time()
    date_ary=time.localtime(t)
    y=time.strftime("%Y-%m-%d %T",date_ary)     
    now=y
    conn = httplib.HTTPSConnection('api.weixin.qq.com')  
    sToken =  read_access_token_gy()
    if sToken == '':            
        url = "/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s"%(AppId_gy,AppSecret_gy)
        conn.request('GET', '%s'%url)  
        res = conn.getresponse()       
        body = res.read()  
        ddata=json.loads(body)
        sToken = ddata['access_token'] 
        conn.close()  
        write_access_token_gy(body)
    file_id=pk
    sUrl='%s/complaint/login/default_gy?fid=payInfoDetail&seq=%s&must_reply=true'%(host_url,file_id)
    description = """关于“%s”有付款信息，请查阅。"""%(pjname)
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

def write_access_token_gy(access_token):
    data = {'access_token':'','expires_in':7200,'time':''}
    log_file=os.path.join('/home/webroot/oWorld/complaint/access_token_gy')
    ddata=json.loads(access_token)
    t=time.time()
    data['access_token'] = ddata['access_token'] 
    data['expires_in'] = ddata['expires_in'] 
    data['time'] = t
    writeTXT(log_file,json.dumps(data))
    return

def read_access_token_gy():
    log_file=os.path.join('/home/webroot/oWorld/complaint/access_token_gy')
    access_token = openTXT(log_file)
    if access_token=='':
        return ''

    ddata=json.loads(access_token)
    token =  ddata['access_token'] 
    if  token !='' :  
        t1 = ddata['time'] 
        t=time.time() 
        if (t - t1)<7000:
            return token
    return ''

def my_urlencode(str) :
    str = urllib.quote(str)
    str = str.replace('/', '%2F')
    return str

if __name__ == "__main__":
    print 'Push start.......'
    #pushDeal()  #受理前

