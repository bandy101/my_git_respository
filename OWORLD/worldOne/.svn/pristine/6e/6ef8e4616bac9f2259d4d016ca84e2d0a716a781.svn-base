# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf8')
import os,time
import json
import httplib
from HW_DT_TOOL                 import getToday
from HW_DB   import DataBaseParent_local,DataBaseParent_byerp
sys.path.append("/home/webroot/oWorld/complaint")
from share        import template_id_msg_tj,AppId_tj,AppSecret_tj,host_url,read_access_token_common,write_access_token_common,my_urlencode
#本地mysql数据库
local=DataBaseParent_local()  
sys.setdefaultencoding('utf-8')

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

if __name__ == "__main__":
    #大于180天部分
    sql="""SELECT OP.id,OP.cname,OP.p_id,ab.name,datediff(now(),IFNULL(PT.last_ctime,OP.bbtime))
            from (select a.id,a.cname,a.p_id,a.bbtime,a.stage from out_proj a where not EXISTS (select 1 from tracking_push_log b where b.prj_id=a.id and b.status>1)) OP
            left join
            (
            select pid,MAX(ctime) as last_ctime from out_proj_tracking
            GROUP BY pid 
            ) PT ON PT.pid=OP.id
            left join addr_book ab on ab.id=OP.p_id
            where datediff(now(),IFNULL(PT.last_ctime,OP.bbtime)) >=180
            and OP.stage =1
            and OP.p_id in(106,243) 
            order by OP.p_id"""
    rows,iN=local.select(sql)
    print iN
    p_id=0
    for e in rows:
        if e[2]!=p_id:
            print e[3]
            errcode = mWxPushMsg_tracking_fw(e[0],e[1],e[2],e[3],2)
            print errcode
            if str(errcode)=='0':
                sql="""INSERT INTO tracking_push_log(prj_id,ctime,status) VALUES(%s,now(),2) """%(e[0])
                local.executesql(sql)
        p_id=e[2]

    #90天-180天部分
    sql="""SELECT OP.id,OP.cname,OP.p_id,ab.name,datediff(now(),IFNULL(PT.last_ctime,OP.bbtime))
            from (select a.id,a.cname,a.p_id,a.bbtime,a.stage from out_proj a where not EXISTS (select 1 from tracking_push_log b where b.prj_id=a.id and b.status>1)) OP
            left join
            (
            select pid,MAX(ctime) as last_ctime from out_proj_tracking
            GROUP BY pid 
            ) PT ON PT.pid=OP.id
            left join addr_book ab on ab.id=OP.p_id
            where datediff(now(),IFNULL(PT.last_ctime,OP.bbtime)) <180 and datediff(now(),IFNULL(PT.last_ctime,OP.bbtime)) >=90
            and OP.stage =1
            and OP.p_id in(106,243) 
            order by OP.p_id"""
    rows,iN=local.select(sql)
    print iN
    p_id=0
    for e in rows:
        if e[2]!=p_id:
            print e[3]
            errcode = mWxPushMsg_tracking_fw(e[0],e[1],e[2],e[3],1)
            print errcode
            if str(errcode)=='0':
                sql="""INSERT INTO tracking_push_log(prj_id,ctime,status) VALUES(%s,now(),1) """%(e[0])
                local.executesql(sql)
        p_id=e[2]
        