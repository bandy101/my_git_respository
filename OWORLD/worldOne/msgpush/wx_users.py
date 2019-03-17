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
# from complaint.share           import write_access_token,read_access_token
#微信服务号变量
AppId = 'wxec7aef65a74af367'   #APPID
Token = 'HIvEmG8dVTIIJR6220E'
EncodingAESKey = 'I7RMkwauatKQXUBFRmpCkuwwIAEOdJv1GW1UOKMwSIP'
AppSecret = '1ceffffb488d0f7f59e21c39c6afccc1'
host_url = 'http://lw.szby.cn'

def getWxUsers():
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

    openids = mWxGetUser()
    for e in openids:
        openid = e
        url = "/cgi-bin/user/info?access_token=%s&openid=%s&lang=zh_CN"%(sToken,openid)
        conn.request('GET', '%s'%url)  
        res = conn.getresponse()       
        body = res.read()  
        ddata=json.loads(body)
        nickname = ddata['nickname']
        sex = ddata['sex']
        city = ddata['city']
        province = ddata['province']
        country = ddata['country']
        headimgurl = ddata['headimgurl']
        subscribe_time = ddata['subscribe_time']
        print ToGBK(nickname)
        print '--------'
        sql="select usr_id from users_wx where openid='%s'"%openid
        rows,iN = db.select(sql)
        if iN>0:
            sql ="""UPDATE users_wx SET 
                nickname='%s',
                sex = '%s',
                city = '%s',
                province = '%s',
                country = '%s',
                headimgurl = '%s',
                subscribe_time = '%s'
                WHERE usr_id = %s
            """%(nickname,sex,city,province,country,headimgurl,subscribe_time,rows[0][0])
            db.executesql(sql)
        else:
            sql="""INSERT INTO users_wx(ctime,status,openid,nickname,sex,city,province,country,headimgurl,subscribe_time)
                VALUES(now(),0,'%s','%s','%s','%s','%s','%s','%s','%s')
            """%(openid,nickname,sex,city,province,country,headimgurl,subscribe_time)
            print sql
            db.executesql(sql)

import httplib
#通知领导
def mWxGetUser():
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
    url = "/cgi-bin/user/get?access_token=%s"%(sToken)
    #print url
    conn.request('GET', '%s'%url)  
    res = conn.getresponse()       
    body = res.read()  
    conn.close()  
    ddata=json.loads(body)
    # errcode = ddata['errcode'] 
    # print ddata['openid']
    return ddata['data']['openid']

def write_access_token(access_token):
    data = {'access_token':'','expires_in':7200,'time':''}
    log_file=os.path.join('/home/webroot/oWorld/complaint/access_token')
    ddata=json.loads(access_token)
    t=time.time()
    data['access_token'] = ddata['access_token'] 
    data['expires_in'] = ddata['expires_in'] 
    data['time'] = t
    writeTXT(log_file,json.dumps(data))
    return

def read_access_token():
    log_file=os.path.join('/home/webroot/oWorld/complaint/access_token')
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

def ToGBK(s):
    try:
        s=str(s.decode("utf-8").encode("GBK"))
    except:
        s=s
    s = s.replace("\n","\r\n")
    return s

if __name__ == "__main__":
    print 'GET users start.......'
    getWxUsers()  


