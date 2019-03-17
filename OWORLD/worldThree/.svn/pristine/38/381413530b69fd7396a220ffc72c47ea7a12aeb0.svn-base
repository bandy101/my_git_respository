# -*- coding: utf-8 -*-
# 尝试
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
from share import db,dActiveUser,g_data,TIME_OUT,ToGBK,HttpResponseCORS,fs_url,oSysInfo,m_aesKey,m_prjname,m_muti_lang

def login_func(request):
    import base64 , time
    import random
    random_no='%s'%(random.randint(0,999999))   
    source =  request.POST.get('source','web')

    if request.META.has_key('HTTP_X_FORWARDED_FOR'):  
        ip =  request.META['HTTP_X_FORWARDED_FOR']  
    else:  
        ip = request.META['REMOTE_ADDR']  
    union_id = 'or0EJv-sW7K_rmSakUfKH1ONE5hg'
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
    sql="""SELECT U.usr_id,U.usr_name,ifnull(ab.sup_id,0),ifnull(su.cname,''),IFNULL(U.headimgurl,'')
                   FROM users_gy U 
                   LEFT JOIN addr_book ab on ab.id = U.addr_id
                   LEFT JOIN suppliers su on su.id = ab.sup_id
                   WHERE U.unionid='%s' AND U.status=1 
                """ % (union_id)
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
        msg = u'用户不存在'
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

def logout_func(request):
    import base64 , time
    import random
    random_no='%s'%(random.randint(0,999999))   

    login_id =  request.GET.get('login_id','')

    errCode = 0
    msg = u'Log Out'
    try:
        del request.session['usr_id']
    except KeyError:
        pass
    print request.POST
    s = """
        {
            "errcode": %s,
            "errmsg": "%s",
            "login_id": "%s",
        }
        """ %(errCode,msg,login_id)  
    return HttpResponseCORS(request,s)

def menu_func(request):
    import base64 , time
    import random
    random_no='%s'%(random.randint(0,999999))   
    sql="""SELECT distinct WMF.menu,WMF.menu_id,WMF.menu_name,
                   WMF.sort,WMF.parent_id,WMF.status-1,WMF.url,WMF.icon
                   FROM menu_func WMF 
                   Left JOIN menu_func WMF1 on WMF.parent_id = WMF1.menu_id
                   WHERE WMF.status=2 and WMF.menu_id>0 and WMF1.status=2
                   ORDER BY WMF.parent_id,WMF.menu,WMF.sort,WMF.menu_id
                """
    #print sql
    rows,iN = db.select(sql)
    names = 'level menu_id menu_name sort parent_id status url icon'.split()
    data = [dict(zip(names, d)) for d in rows]
    s3 = json.dumps(data,ensure_ascii=False)

    s = """
        {
            "errcode": 0,
            "errmsg": "获取数据成功",
            "menu_data": %s
        }
        """ %(s3)  
    return HttpResponseCORS(request,s)
