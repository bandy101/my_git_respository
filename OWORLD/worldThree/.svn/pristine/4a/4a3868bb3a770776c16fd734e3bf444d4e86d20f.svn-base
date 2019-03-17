# -*- coding: utf-8 -*-
# 尝试
prj_name=__name__.split('.')[0]
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import md5
import json
import time
import datetime
from HW_DT_TOOL                 import getToday
from aesMsgCrypt                import WXBizMsgCrypt
import httplib
import urllib
from django.db import connection
from share import db,dActiveUser,g_data,TIME_OUT,ToGBK,HttpResponseCORS,front_url,fs_url,m_aesKey,m_corp_wxid,my_urlencode,write_access_token_common,read_access_token_common
from django.http import HttpResponseRedirect  
exec ('from %s.common.wx_data        import *'%prj_name) 

AppId_web = 'wx24ec0d3dbf61d3ee'
AppSecret_web = '08cf823c5c6921e6a0b339b4521889a3'
def login_wx_func(request):
    import base64 , time 
    import random
    random_no='%s'%(random.randint(0,999999))   
    usr_id,usr_name,dept_id,dept_name='','','',''
    source =  'wx'
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):  
        ip =  request.META['HTTP_X_FORWARDED_FOR']  
    else:  
        ip = request.META['REMOTE_ADDR']  

    code = request.GET.get('code','')
    union_id = ''
    if code!='':
        conn = httplib.HTTPSConnection('api.weixin.qq.com')  
        sToken = read_access_token_common('access_token_web')
        if sToken == '':            
            url = "/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s"%(AppId_web,AppSecret_web)
            conn.request('GET', '%s'%url)  
            res = conn.getresponse()       
            body = res.read()  
            ddata=json.loads(body)
            sToken = ddata['access_token'] 
            conn.close()  
            write_access_token_common(body,'access_token_web')
        url = "/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code"%(AppId_web,AppSecret_web,code)
        conn.request('GET', '%s'%url)  
        res = conn.getresponse()       
        body = res.read()  
        print body
        ddata=json.loads(body)
        access_token = ddata['access_token']
        openid = ddata['openid']
        union_id = ddata.get('unionid','')
    if union_id=='':
        errCode = 1
        msg = u'用户未注册供应商服务平台'
        s = """
            {
            "errcode": %s,
            "errmsg": "%s",
            }
            """ %(errCode,msg)  
        response = HttpResponseCORS(request,s)
        return response
    s1 =''

    if union_id == 'or0EJv-sW7K_rmSakUfKH1ONE5hg': union_id = 'or0EJvw-Y-E7k7zPTdR6vX0OdRlI'
    sql="""SELECT U.usr_id,U.usr_name,ifnull(ab.sup_id,0),ifnull(su.cname,''),IFNULL(U.headimgurl,'')
                   FROM users_gy U 
                   LEFT JOIN addr_book ab on ab.id = U.addr_id
                   LEFT JOIN suppliers su on su.id = ab.sup_id
                   WHERE U.unionid='%s' AND U.status=1 
                """ % (union_id)
    print sql
    lT,iN = db.select(sql)
    if iN>0:
        usr_id=lT[0][0]
              
        request.session['usr_id'] = usr_id
        request.session['usr_name'] = lT[0][1]
        request.session['sup_id'] = lT[0][2]
        request.session['sup_name'] = lT[0][3]
        d_value = ['','','','','']
        d_value[0] = usr_id
        d_value[1] = lT[0][1]
        d_value[2] = lT[0][2]
        d_value[3] = lT[0][3]
        d_value[4] = 0
        g_data.set_value(d_value)
        errCode = 0
        msg = 'OK'
        pic = lT[0][4]

        sTimeStamp = str(time.time())
        wxcpt=WXBizMsgCrypt('szoworld_gy',m_aesKey)
        ret,token = wxcpt.EncryptMsg(str(usr_id),random_no,sTimeStamp)            
        
        sql="""SELECT distinct WMF.menu,WMF.menu_id,WMF.menu_name,
               WMF.sort,WMF.parent_id,WMF.status-1,WMF.url,WMF.icon
               FROM menu_func WMF 
               Left JOIN menu_func WMF1 on WMF.parent_id = WMF1.menu_id
               WHERE WMF.status=2 and WMF.menu_id>0 and WMF1.status=2
               ORDER BY WMF.parent_id,WMF.menu,WMF.sort,WMF.menu_id
            """

        #print sql
        rows,iN = db.select(sql)
        L1=[2]
        L2=[]
        #L = formatData(rows,L1,L2)
        names = 'level menu_id menu_name sort parent_id status url icon'.split()
        data = [dict(zip(names, d)) for d in rows]

        s3 = json.dumps(data,ensure_ascii=False)

        s1 = """"userid":%s,
                "username":"%s",
                "sup_id":%s,
                "sup_name":"%s",
                "pic_url":"%s",
                "AccessToken":"%s",
                "menu_data":%s"""%(lT[0][0],(lT[0][1]),lT[0][2],(lT[0][3]),pic,token,s3)
        sql = """insert into users_login_gy (usr_id,source,token,login_ip,login_time,refresh_time,expire_time)
                     values (%s,'%s','%s','%s',now(),now(),%s) 
                    """%(lT[0][0],source,token,ip,int(TIME_OUT)*60)
        #print ToGBK(sql)
            
        db.executesql(sql)
    else:
        errCode = 1
        msg = u'用户未注册供应商服务平台'
    s = """
        {
            "errcode": %s,
            "errmsg": "%s",
            %s
        }
        """ %(errCode,msg,s1)  
    #print ToGBK(s)
    response = HttpResponseCORS(request,s)
    return response
