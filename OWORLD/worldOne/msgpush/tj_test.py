# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf8')
import os,time
import json
import httplib
import urllib
from HW_DB   import DataBaseParent_local
sys.path.append("/home/webroot/oWorld")
from common.HW_FILE_TOOL           import make_sub_path,writeTXT,openTXT,writeLOG
# from share        import read_access_token_common,write_access_token_common
#本地mysql数据库
local=DataBaseParent_local()  
template_id_msg_tj = "iI6VBtxMz3Jt_CgkLH0OKenZYnxBLJDnF8pu3UeJpVQ"
AppId_tj = 'wx88c1d3c813d448dc'
host_url = 'http://lw.szby.cn'
AppSecret_tj = 'a33a6924ec99e7129efd7a69cf7611f5'

def my_urlencode(str) :
    str = urllib.quote(str)
    str = str.replace('/', '%2F')
    return str

def getToday(format=3):
    """返回今天的日期字串"""
    #format=1   yyyymmdd
    #format=2   hh:mm
    #format=3   yyyy/mm/dd
    #format=4   yyyy/mm/dd  hh:mm
    #format=5   yymmdd
    t=time.time()
    date_ary=time.localtime(t)
    if format==1:
        x=time.strftime("%Y%m%d",date_ary)
    elif format==2:
        x=time.strftime("%H:%M",date_ary)
    elif format==3:
        x=time.strftime("%Y/%m/%d",date_ary)
    elif format==4:
        x=time.strftime("%Y/%m/%d %H:%M",date_ary)
    elif format==5:
        x=time.strftime("%y%m%d",date_ary)
    elif format==6:
        x=time.strftime("%Y-%m-%d",date_ary)
    elif format==7:
        x=time.strftime("%Y/%m/%d %H:%M:%S",date_ary)
        print x
    elif format==8:
        x=time.strftime("%Y-%m-%d %H:%M",date_ary)
    elif format==9:
        x=time.strftime("%Y-%m-%d %H:%M:%S",date_ary)
    elif format==10:
        x=time.strftime("%Y年%m月%d日 %H:%M",date_ary)
    return x

def write_access_token_common(access_token,itype):
    data = {'access_token':'','expires_in':7200,'time':''}
    log_file=os.path.join('/home/webroot/oWorld/complaint/%s'%itype)
    ddata=json.loads(access_token)
    t=time.time()
    data['access_token'] = ddata['access_token'] 
    data['expires_in'] = ddata['expires_in'] 
    data['time'] = t
    writeTXT(log_file,json.dumps(data))
    return

def read_access_token_common(itype):
    log_file=os.path.join('/home/webroot/oWorld/complaint/%s'%itype)
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

def mWxPushMsg_tracking_fw(pk,prj_name,usr_id_tj,usr_name,status):   
    now=getToday()
    toUser = get_toUser(usr_id_tj)
    conn = httplib.HTTPSConnection('api.weixin.qq.com')  
    sToken = read_access_token_common('access_token_tj')
    if sToken == '':            
        url = "/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s"%(AppId_tj,AppSecret_tj)
        conn.request('GET', '%s'%url)  
        res = conn.getresponse()       
        body = res.read()  
        ddata=json.loads(body)
        sToken = ddata['access_token'] 
        conn.close()  
        write_access_token_common(body,'access_token_tj')
    file_id=pk
    sUrl='%s/complaint/login/default_tj?fid=projDetail&seq=%s&must_reply=true'%(host_url,file_id)
    stitle ="""新消息"""
    description=''
    if status==1:
        description = """尊敬的%s,您在深圳宝鹰建设集团推荐的"%s"需要反馈跟进信息。"""%(usr_name,prj_name)
    if status==2:
        description = """尊敬的%s,您在深圳宝鹰建设集团推荐的"%s"已半年未反馈信息，请及时反馈跟进信息，否则该项目推荐将会立即失效。"""%(usr_name,prj_name)
    surl = my_urlencode(sUrl)
    # print toUser
    stitle=json.dumps(stitle)
    description = json.dumps(description)
    now = json.dumps(now)
    city = json.dumps("深圳")
    url = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_base&state=wx#wechat_redirect"%(AppId_tj,surl)

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
    """%(toUser,template_id_msg_tj,sUrl,description,city,now)
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

def get_toUser(usr_id_tj):
    L=''
    sql="""SELECT openid FROM users_tj WHERE addr_id=%s"""%usr_id_tj
    rows,iN=local.select(sql)
    if iN>0:
        L=rows[0][0]
    return L

def push():
    #大于180天部分
    sql="""SELECT OP.id,OP.cname,OP.p_id,ab.name,datediff(now(),IFNULL(PT.last_ctime,OP.bbtime))
            from (select a.id,a.cname,a.p_id,a.bbtime,a.stage from out_proj a where not EXISTS (select 1 from tracking_push_log b where b.prj_id=a.id and b.status>1)) OP
            left join
            (
            select pid,MAX(ctime) as last_ctime from out_proj_tracking
            GROUP BY pid 
            ) PT ON PT.pid=OP.id
            left join addr_book ab on ab.id=OP.p_id
            where OP.id=16631
            order by OP.p_id"""
    rows,iN=local.select(sql)
    print iN
    p_id=0
    for e in rows:
        if e[2]!=p_id:
            print e[3]
            errcode = mWxPushMsg_tracking_fw(e[0],e[1],e[2],e[3],2)
            print errcode
            # if str(errcode)=='0':
            #     sql="""INSERT INTO tracking_push_log(prj_id,ctime,status) VALUES(%s,now(),2) """%(e[0])
            #     local.executesql(sql)
        p_id=e[2]

    #90天-180天部分
    # sql="""SELECT OP.id,OP.cname,OP.p_id,ab.name,datediff(now(),IFNULL(PT.last_ctime,OP.bbtime))
    #         from (select a.id,a.cname,a.p_id,a.bbtime,a.stage from out_proj a where not EXISTS (select 1 from tracking_push_log b where b.prj_id=a.id and b.status>1)) OP
    #         left join
    #         (
    #         select pid,MAX(ctime) as last_ctime from out_proj_tracking
    #         GROUP BY pid 
    #         ) PT ON PT.pid=OP.id
    #         left join addr_book ab on ab.id=OP.p_id
    #         where OP.stage =1
    #         and OP.id=16631
    #         order by OP.p_id"""
    # rows,iN=local.select(sql)
    # print iN
    # p_id=0
    # for e in rows:
    #     if e[2]!=p_id:
    #         print e[3]
    #         errcode = mWxPushMsg_tracking_fw(e[0],e[1],e[2],e[3],1)
    #         print errcode
    #         if str(errcode)=='0':
    #             sql="""INSERT INTO tracking_push_log(prj_id,ctime,status) VALUES(%s,now(),1) """%(e[0])
    #             local.executesql(sql)
    #     p_id=e[2]

if __name__ == "__main__":
    print 'Push start.......'
    push()  
        